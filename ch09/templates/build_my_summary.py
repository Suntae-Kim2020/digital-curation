# -*- coding: utf-8 -*-
r"""
build_my_summary.py — 미니 프로젝트용 LLM 요약 생성기 (Ch.7 코드 기반)

입력 : my_collected_embedded.jsonl   (build_my_embed.py 산출물)
출력 : my_collected_complete.jsonl    (summary까지 채운 최종 — AI 6필드 완성)

- 경로는 이 파일 위치(my_project) 기준이라 어느 폴더에서 실행해도 동작한다.
- GEMINI_API_KEY가 있으면 실제 요약 생성, 없으면 자리표시 문구를 넣는다.

실행:  python build_my_summary.py
[교재 Ch.9 §9.2.3 단계 3 — LLM 요약]
"""
import io
import os
import sys
import time
import json
from pathlib import Path

import pandas as pd

# line_buffering=True: 진행 메시지가 끝에 몰리지 않고 한 줄씩 즉시 출력되게 한다
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True)

HERE = Path(__file__).resolve().parent
INPUT = HERE / "my_collected_embedded.jsonl"
OUTPUT = HERE / "my_collected_complete.jsonl"

LLM_MODEL = "gemini-2.5-flash"


def make_live_generator():
    """API 키가 있으면 실제 요약 함수를, 없으면 None을 반환."""
    if not os.getenv("GEMINI_API_KEY"):
        return None
    try:
        from google import genai
    except ImportError:
        return None

    client = genai.Client()
    SYS = (
        "당신은 도서관 사서입니다. 주어진 자료의 본문을 읽고 "
        "200~300자 분량의 한국어 요약을 만듭니다. 다음 규칙을 따릅니다. "
        "(1) 본문에 없는 사실은 만들어 내지 않습니다. "
        "(2) 자료의 주된 내용과 활용 맥락을 함께 담습니다. "
        "(3) 평서체로 작성합니다."
    )

    def generate(title: str, description: str) -> str:
        prompt = (
            "다음 자료를 요약해 주세요.\n\n"
            f"제목: {title}\n\n"
            f"본문:\n{description}\n\n"
            "아래 JSON 형식으로 응답하세요:\n"
            '{"summary": "200~300자 요약"}'
        )
        resp = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
            config={
                "system_instruction": SYS,
                "temperature": 0.2,
                "max_output_tokens": 600,
                "response_mime_type": "application/json",
                "thinking_config": {"thinking_budget": 0},  # 생각 끄기(책 §7.2.2)
            },
        )
        try:
            return json.loads(resp.text)["summary"]
        except Exception as ex:
            return f"[요약 생성 실패: {ex}]"

    return generate


def main():
    if not INPUT.exists():
        print(f"[ERR] {INPUT} 없음 — 먼저 'python build_my_embed.py'를 실행하세요.")
        sys.exit(1)

    print(f"[입력] {INPUT}")
    collected = pd.read_json(INPUT, lines=True)
    print(f"  → {len(collected)} 레코드")

    live = make_live_generator()
    if live:
        print("\n[LIVE 모드] GEMINI_API_KEY 감지 — 실제 Gemini API 호출")
    else:
        print("\n[자리표시 모드] API 키 없음 — summary에 자리표시 문구를 넣습니다")
        print("            (키 등록 후 다시 실행하면 실제 요약으로 채워집니다)")

    # 요약이 비어 있는 레코드만 처리 (이미 채워진 자료는 건너뜀 — 재실행 안전)
    todo = [idx for idx, row in collected.iterrows() if not row.get("summary")]
    print(f"요약 생성 대상: {len(todo)}건")

    for n, idx in enumerate(todo, start=1):
        row = collected.loc[idx]
        if live:
            print(f"  [{n}/{len(todo)}] {row['id']} 요약 생성 중…")
            summary = live(row["title"], row.get("description", ""))
            time.sleep(5)  # rate limit 방어
        else:
            summary = "[요약 자리 — GEMINI_API_KEY 등록 후 다시 실행하세요]"

        collected.at[idx, "summary"] = summary
        print(f"  → {summary[:80]}…")

    collected.to_json(OUTPUT, orient="records", lines=True,
                      force_ascii=False, date_format="iso")
    print(f"\n[OK] {OUTPUT.name} ({len(collected)} 레코드)")

    # AI 확장 6필드 진행률
    print("\n[AI 확장 6필드 최종 채움 상태]")
    ext_fields = ["summary", "keywords", "chunk_ids",
                  "embedding_flag", "source_url", "license_code"]
    for f in ext_fields:
        if f not in collected.columns:
            print(f"  {f:<15}: 0/{len(collected)} (없음)")
            continue
        filled = sum(
            1 for v in collected[f]
            if (isinstance(v, list) and v) or
               (isinstance(v, str) and v.strip()) or
               (isinstance(v, bool) and v)
        )
        bar = "█" * filled + "░" * (len(collected) - filled)
        print(f"  {f:<15}: {filled}/{len(collected)}  {bar}")

    if all(
        sum(1 for v in collected[f] if (isinstance(v, list) and v) or (isinstance(v, str) and v.strip()) or (isinstance(v, bool) and v)) == len(collected)
        for f in ext_fields
    ):
        print("\n✅ 스키마 AI 확장 6필드 모두 채워졌습니다. 이제 my_rag.py로 챗봇을 띄우세요.")


if __name__ == "__main__":
    main()
