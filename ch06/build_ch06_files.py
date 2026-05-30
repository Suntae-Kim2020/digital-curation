# -*- coding: utf-8 -*-
r"""
Ch.6 산출물 생성기

Ch.5의 ch05_collected_filled.jsonl을 읽어 다음을 생성한다.

- ch06_collected_embedded.jsonl
    Ch.3 스키마의 마지막 필드 embedding_id까지 채운 완성형.
    embedding_id 값은 chunk_ids의 첫 번째 ID(자료 1건의 대표)다.

ChromaDB 컬렉션 자체는 GEMINI_API_KEY가 필요하므로
사용자 PC에서 ch06_vector_search.ipynb 노트북을 실행해 생성한다.

[교재 §6.5 통합 산출물의 실제 구현]
"""
import io
import os
import sys
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

INPUT = os.path.join("..", "ch05", "ch05_collected_filled.jsonl")


def main():
    if not os.path.exists(INPUT):
        print(f"[ERR] {INPUT} 없음 — 먼저 Ch.5 자료를 만드세요.")
        sys.exit(1)

    print(f"[입력] {INPUT}")
    collected = pd.read_json(INPUT, lines=True)
    print(f"  → {len(collected)} 레코드")

    # embedding_id 채우기 (자료당 첫 청크 ID를 대표로)
    filled_count = 0
    for idx, row in collected.iterrows():
        chunk_ids = row.get("chunk_ids") or []
        if isinstance(chunk_ids, list) and chunk_ids:
            collected.at[idx, "embedding_id"] = chunk_ids[0]
            filled_count += 1

    collected.to_json(
        "ch06_collected_embedded.jsonl",
        orient="records", lines=True, force_ascii=False,
    )

    print(f"\n[OK] ch06_collected_embedded.jsonl ({len(collected)} 레코드)")
    print(f"  → embedding_id 채워진 레코드: {filled_count}")

    # Ch.3 스키마 AI 6확장 필드 진행률 점검
    print("\n[Ch.3 §3.3 AI 확장 6필드 채움 상태]")
    ext_fields = ["summary", "keywords", "chunk_ids",
                  "embedding_id", "source_url", "license_code"]
    for f in ext_fields:
        if f not in collected.columns:
            print(f"  {f:<15}: 0/{len(collected)} (필드 없음)")
            continue
        filled = sum(
            1 for v in collected[f]
            if (isinstance(v, list) and v) or
               (isinstance(v, str) and v.strip())
        )
        bar = "█" * filled + "░" * (len(collected) - filled)
        print(f"  {f:<15}: {filled}/{len(collected)}  {bar}")

    print()
    print("[다음 단계]")
    print("  ChromaDB 컬렉션 자체는 GEMINI_API_KEY가 필요합니다.")
    print("  본인 PC에서 ch06_vector_search.ipynb를 열어 실행하면")
    print("  ./chroma_db 폴더에 컬렉션이 저장됩니다.")


if __name__ == "__main__":
    main()
