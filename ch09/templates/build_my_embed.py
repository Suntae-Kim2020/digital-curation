# -*- coding: utf-8 -*-
r"""
build_my_embed.py — 미니 프로젝트용 임베딩·벡터 적재기 (Ch.6 코드 기반)

입력 : my_chunks.jsonl            (build_my_chunks.py 산출물)
       my_collected_filled.jsonl
출력 : ./chroma_db/ 컬렉션 'my_thesis_chunks'  (의미 검색용 벡터 DB)
       my_collected_embedded.jsonl            (embedding_flag 채운 완성형)

- 경로는 이 파일 위치(my_project) 기준이라 어느 폴더에서 실행해도 동작한다.
- GEMINI_API_KEY 환경변수가 필요하다(책 §6.2.4).

실행:  python build_my_embed.py
[교재 Ch.9 §9.2.3 단계 3 — 임베딩]
"""
import io
import os
import sys
import time
from pathlib import Path

import pandas as pd
import chromadb
from google import genai
from google.genai import errors

# line_buffering=True: 진행 메시지가 끝에 몰리지 않고 한 줄씩 즉시 출력되게 한다
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True)

# 이 파일이 있는 폴더(my_project) 기준 경로
HERE = Path(__file__).resolve().parent
IN_CHUNKS = HERE / "my_chunks.jsonl"
IN_FILLED = HERE / "my_collected_filled.jsonl"
OUT_EMBEDDED = HERE / "my_collected_embedded.jsonl"
CHROMA_DB_PATH = str(HERE / "chroma_db")

# 자관용 컬렉션 이름 (본서 예제의 'ai_ready_chunks'와 다르게)
COLLECTION_NAME = "my_thesis_chunks"
EMB_MODEL = "gemini-embedding-001"
EMBED_BATCH = 20   # 배치 상한은 100이지만, 한 요청의 토큰이 분당 한도(TPM)를 넘으면
                   # 429가 나므로 20개 정도로 작게(긴 청크가 많으면 더 줄인다)


def embed_batch_with_retry(ai, texts, max_retries=5):
    """한 배치를 임베딩한다. 429(쿼터)·5xx(혼잡)면 점점 더 오래 기다렸다 재시도."""
    for attempt in range(1, max_retries + 1):
        try:
            resp = ai.models.embed_content(
                model=EMB_MODEL,
                contents=texts,
                config={"output_dimensionality": 768},
            )
            return [e.values for e in resp.embeddings]
        except errors.APIError as e:
            code = getattr(e, "code", None)
            if attempt == max_retries or code not in (429, 500, 503):
                raise
            wait = 10 * (2 ** (attempt - 1))  # 10·20·40·80초
            print(f"  [{code}] 쿼터/혼잡 — {wait}초 후 재시도 ({attempt}/{max_retries})…")
            time.sleep(wait)


def main():
    if not IN_CHUNKS.exists():
        print(f"[ERR] {IN_CHUNKS} 없음 — 먼저 'python build_my_chunks.py'를 실행하세요.")
        sys.exit(1)
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "GEMINI_API_KEY가 설정되지 않았습니다. 책 §6.2.4 절차로 등록 후 다시 실행하세요.")

    ai = genai.Client()  # 환경변수에서 키 자동 로드

    # --- ChromaDB 컬렉션 ---
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"[컬렉션] {COLLECTION_NAME}: 현재 {collection.count()}개")

    # --- 청크 로드 ---
    chunks = pd.read_json(IN_CHUNKS, lines=True)
    print(f"[입력] {IN_CHUNKS.name} — {len(chunks)}개 청크")

    # 이미 적재된 ID는 건너뜀 (재실행 안전)
    existing = set(collection.get()["ids"]) if collection.count() else set()
    new_chunks = chunks[~chunks["chunk_id"].isin(existing)]
    print(f"  → 적재할 신규 청크: {len(new_chunks)}개")

    if len(new_chunks) > 0:
        texts = new_chunks["text"].tolist()
        ids = new_chunks["chunk_id"].tolist()
        metas = [{"doc_id": r["doc_id"], "chunk_index": int(r["chunk_index"])}
                 for _, r in new_chunks.iterrows()]

        # EMBED_BATCH개씩 나눠서 임베딩·적재
        total = len(texts)
        n_batches = (total + EMBED_BATCH - 1) // EMBED_BATCH
        for bi, i in enumerate(range(0, total, EMBED_BATCH), start=1):
            b_texts = texts[i:i + EMBED_BATCH]
            b_ids = ids[i:i + EMBED_BATCH]
            b_metas = metas[i:i + EMBED_BATCH]

            # 임베딩 호출은 수 초 걸리므로, 시작할 때 먼저 알린다(멈춘 게 아님)
            print(f"  [배치 {bi}/{n_batches}] {len(b_texts)}개 임베딩 요청 중…")
            embeddings = embed_batch_with_retry(ai, b_texts)

            collection.add(ids=b_ids, documents=b_texts,
                           embeddings=embeddings, metadatas=b_metas)
            print(f"    → 적재 {min(i + EMBED_BATCH, total)}/{total} 완료")
            if i + EMBED_BATCH < total:
                time.sleep(4)  # 분당 토큰 한도(TPM) 여유 — 배치 간 간격

    print(f"[OK] 컬렉션 적재 완료 — 총 {collection.count()}개 청크")

    # --- embedding_flag 채우기 ---
    if IN_FILLED.exists():
        collected = pd.read_json(IN_FILLED, lines=True)
        for idx, row in collected.iterrows():
            cids = row.get("chunk_ids") or []
            if isinstance(cids, list) and cids:
                collected.at[idx, "embedding_flag"] = True
        collected.to_json(OUT_EMBEDDED, orient="records", lines=True,
                          force_ascii=False, date_format="iso")
        print(f"[OK] {OUT_EMBEDDED.name} ({len(collected)} 레코드, embedding_flag 채움)")

    print()
    print("[다음 단계]  python build_my_summary.py")


if __name__ == "__main__":
    main()
