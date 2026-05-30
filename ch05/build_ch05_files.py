# -*- coding: utf-8 -*-
r"""
Ch.5 산출물 생성기

Ch.4의 ch04_collected.jsonl을 읽어 다음 두 파일을 생성한다.

- ch05_chunks.jsonl
    본문(description)을 sentence_overlap 전략으로 청킹한 결과.
    각 행 = 청크 1개 (chunk_id, doc_id, chunk_index, method, char_count, text)

- ch05_collected_filled.jsonl
    Ch.3 스키마의 keywords·chunk_ids 두 필드를 채운 ch04_collected의 완성형.

Kiwi(kiwipiepy)가 설치돼 있으면 한국어 형태소 분석으로 명사 키워드 추출.
설치돼 있지 않으면 간단한 영문 토큰화로 대체(다국어 자료에서도 작동).

[교재 §5.5 통합 산출물의 실제 구현]
"""
import io
import os
import re
import sys
import json
from collections import Counter

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# =============================================================================
# Kiwi (선택) — 한국어 형태소 분석
# =============================================================================
try:
    from kiwipiepy import Kiwi
    kiwi = Kiwi()
    HAS_KIWI = True
    print(f"[Kiwi] 로드 성공 — 한국어 형태소 분석 사용 (v{kiwi.version})")
except Exception:
    HAS_KIWI = False
    print("[Kiwi] 미설치 — 간단한 영문 토큰화로 대체")
    print("       (한국어 자료에서 키워드 정확도를 높이려면 'pip install kiwipiepy')")

# =============================================================================
# 문장 분할
# =============================================================================
def split_sentences(text: str) -> list:
    """텍스트를 문장 리스트로. Kiwi가 있으면 한국어·영문 모두 정확."""
    if HAS_KIWI:
        return [s.text for s in kiwi.split_into_sents(text)]
    # 단순 영문/공통 분할
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sents if s]


# =============================================================================
# 청킹 — sentence_overlap (본서 권장)
# =============================================================================
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


# =============================================================================
# 키워드 추출
# =============================================================================
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
        # Kiwi가 한국어 명사를 못 잡으면(=영문 자료) 영문 fallback
    # 영문 단순 빈도
    words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", text.lower())
    words = [w for w in words if w not in STOPWORDS_EN]
    return [w for w, _ in Counter(words).most_common(top_k)]


# =============================================================================
# 메인
# =============================================================================
def main():
    INPUT = os.path.join("..", "ch04", "ch04_collected.jsonl")
    if not os.path.exists(INPUT):
        print(f"[ERR] {INPUT} 없음 — 먼저 Ch.4의 ch04_collected.jsonl을 만드세요.")
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

        # (1) 키워드
        collected.at[idx, "keywords"] = extract_keywords(text, top_k=10)

        # (2) 청크
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

    # 저장
    collected.to_json(
        "ch05_collected_filled.jsonl",
        orient="records", lines=True, force_ascii=False,
    )
    pd.DataFrame(all_chunks).to_json(
        "ch05_chunks.jsonl",
        orient="records", lines=True, force_ascii=False,
    )

    print()
    print(f"[OK] ch05_collected_filled.jsonl ({len(collected)} 레코드)")
    print(f"[OK] ch05_chunks.jsonl ({len(all_chunks)} 청크)")
    print()
    print("[요약 — 자료별 청크 수]")
    summary = pd.DataFrame(all_chunks).groupby("doc_id").size().reset_index(name="chunks")
    print(summary.to_string(index=False))
    print()
    print("[첫 청크 미리보기]")
    if all_chunks:
        print(json.dumps(all_chunks[0], ensure_ascii=False, indent=2)[:600] + " ...")


if __name__ == "__main__":
    main()
