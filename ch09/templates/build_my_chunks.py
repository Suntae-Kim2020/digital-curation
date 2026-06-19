# -*- coding: utf-8 -*-
r"""
build_my_chunks.py — 미니 프로젝트용 청킹·키워드 생성기 (Ch.5 코드 기반)

입력 : my_collected.jsonl        (build_my_data.py 산출물)
출력 : my_chunks.jsonl           (청크 1개 = 1행)
       my_collected_filled.jsonl (keywords·chunk_ids 두 필드 채운 완성형)

- 경로는 이 파일 위치(my_project) 기준이라 어느 폴더에서 실행해도 동작한다.
- Kiwi(kiwipiepy)가 있으면 한국어 명사 키워드, 없으면 영문 토큰화로 대체.

실행:  python build_my_chunks.py
[교재 Ch.9 §9.2.3 단계 3 — 청킹]
"""
import io
import re
import sys
import json
from pathlib import Path
from collections import Counter

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 이 파일이 있는 폴더(my_project) 기준 경로
HERE = Path(__file__).resolve().parent
INPUT = HERE / "my_collected.jsonl"
OUT_CHUNKS = HERE / "my_chunks.jsonl"
OUT_FILLED = HERE / "my_collected_filled.jsonl"

# =============================================================================
# Kiwi (선택) — 한국어 형태소 분석
# =============================================================================
try:
    import kiwipiepy
    from kiwipiepy import Kiwi
    kiwi = Kiwi()
    HAS_KIWI = True
    print(f"[Kiwi] 로드 성공 — 한국어 형태소 분석 사용 (v{kiwipiepy.__version__})")
except Exception:
    HAS_KIWI = False
    print("[Kiwi] 미설치 — 간단한 영문 토큰화로 대체")
    print("       (한국어 자료에서 키워드 정확도를 높이려면 'pip install kiwipiepy')")


def split_sentences(text: str) -> list:
    """텍스트를 문장 리스트로. Kiwi가 있으면 한국어·영문 모두 정확."""
    if HAS_KIWI:
        return [s.text for s in kiwi.split_into_sents(text)]
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sents if s]


def chunk_sentence_overlap(text: str, max_chars: int = 800, overlap_sents: int = 1) -> list:
    """문장 단위 + 끝 N문장을 다음 청크 앞에 다시 포함."""
    sents = split_sentences(text)
    chunks, buf_sents, buf = [], [], ""
    for s in sents:
        if len(buf) + len(s) > max_chars and buf:
            chunks.append(buf)
            overlap = buf_sents[-overlap_sents:] if overlap_sents else []
            buf_sents = overlap + [s]
            buf = " ".join(buf_sents)
        else:
            buf_sents.append(s)
            buf = (buf + " " + s).strip() if buf else s
    if buf:
        chunks.append(buf)
    return chunks


STOPWORDS_EN = {
    "the", "a", "an", "of", "in", "on", "and", "or", "but", "if", "with",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "this", "that", "these", "those", "we", "they", "it", "its", "their",
    "such", "from", "to", "for", "as", "by", "at", "into", "out", "over",
    "can", "may", "will", "would", "should", "could", "than", "then", "also",
    "however", "while", "where", "when", "which", "who", "whose", "what",
    "our", "your", "his", "her", "them", "us", "you", "do", "does", "did",
    "not", "no", "very", "more", "most", "some", "any", "all", "each", "every",
    "show", "shown", "showing", "use", "used", "using", "uses", "based",
}


def extract_keywords(text: str, top_k: int = 10) -> list:
    """본문에서 키워드 top_k개를 빈도순으로 반환."""
    if HAS_KIWI:
        tokens = kiwi.tokenize(text)
        NOUN_TAGS = {"NNG", "NNP"}
        words = [t.form for t in tokens
                 if t.tag in NOUN_TAGS and len(t.form) >= 2]
        if words:
            return [w for w, _ in Counter(words).most_common(top_k)]
    words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", text.lower())
    words = [w for w in words if w not in STOPWORDS_EN]
    return [w for w, _ in Counter(words).most_common(top_k)]


def main():
    if not INPUT.exists():
        print(f"[ERR] {INPUT} 없음 — 먼저 'python build_my_data.py'를 실행하세요.")
        sys.exit(1)

    print(f"[입력] {INPUT}")
    collected = pd.read_json(INPUT, lines=True)
    print(f"  → {len(collected)} 레코드")

    all_chunks = []
    for idx, row in collected.iterrows():
        doc_id = row["id"]
        text = row.get("description", "") or ""
        if not text:
            continue

        collected.at[idx, "keywords"] = extract_keywords(text, top_k=10)

        chunks = chunk_sentence_overlap(text, max_chars=800, overlap_sents=1)
        chunk_ids = []
        for i, ctext in enumerate(chunks):
            cid = f"{doc_id}-c{i+1:03d}"
            chunk_ids.append(cid)
            all_chunks.append({
                "chunk_id":    cid,
                "doc_id":      doc_id,
                "chunk_index": i,
                "method":      "sentence_overlap_1",
                "char_count":  len(ctext),
                "text":        ctext,
            })
        collected.at[idx, "chunk_ids"] = chunk_ids

    collected.to_json(OUT_FILLED, orient="records", lines=True,
                      force_ascii=False, date_format="iso")
    pd.DataFrame(all_chunks).to_json(OUT_CHUNKS, orient="records", lines=True,
                                     force_ascii=False, date_format="iso")

    print()
    print(f"[OK] {OUT_FILLED.name} ({len(collected)} 레코드)")
    print(f"[OK] {OUT_CHUNKS.name} ({len(all_chunks)} 청크)")
    print()
    print("[요약 — 자료별 청크 수]")
    summary = pd.DataFrame(all_chunks).groupby("doc_id").size().reset_index(name="chunks")
    print(summary.to_string(index=False))
    print()
    print("[다음 단계]  python build_my_embed.py")


if __name__ == "__main__":
    main()
