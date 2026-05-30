# -*- coding: utf-8 -*-
r"""
Ch.7 산출물 생성기

Ch.6의 ch06_collected_embedded.jsonl을 읽어 LLM이 생성한 한국어 summary를
채운 ch07_collected_complete.jsonl을 만든다.

[두 가지 모드]
- LIVE: GEMINI_API_KEY가 설정돼 있고 google-genai가 설치돼 있으면 실제 Gemini API 호출
- DEMO: 그 외에는 사전 작성된 데모 요약을 사용 (저장소 빌드 시 기본값)

저장소에 커밋되는 파일은 DEMO 모드 결과로, '완성된 스키마의 모양'을 보여 주는 용도다.
학습자가 본인 PC에서 노트북 ch07_prompt_patterns.ipynb를 실행하면
GEMINI_API_KEY로 실제 LLM 요약을 생성해 같은 파일을 덮어쓴다.

[교재 §7.4 통합 산출물의 실제 구현]
"""
import io
import os
import sys
import time
import json
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# =============================================================================
# 데모 요약 (저장소 빌드용 — 학습자가 노트북 실행하면 실제 LLM이 덮어씀)
# =============================================================================
DEMO_SUMMARIES = {
    "arxiv:2005.11401v4": (
        "본 논문은 대규모 언어 모델이 학습 시점의 사실 지식에만 의존해 답하는 한계를 보완하기 위해, "
        "외부 지식 출처를 검색해 답변 생성에 함께 활용하는 RAG(Retrieval-Augmented Generation) 기법을 제안한다. "
        "지식 집약적 NLP 과제 전반에서 기존 모델 대비 성능을 크게 향상시켰음을 실험으로 보였다."
    ),
    "arxiv:2312.10997v5": (
        "본 서베이 논문은 RAG 분야의 최근 연구 동향을 정리한다. "
        "환각·낡은 지식·불투명한 추론이라는 LLM의 세 가지 한계를 보완하는 검색 기반 접근들을 "
        "수집·검색·생성 단계별로 분류하고, 평가 지표와 응용 사례를 폭넓게 다룬다."
    ),
    "arxiv:2401.18059v1": (
        "RAFT(Retrieval Aware Fine-Tuning)는 RAG 환경에서 검색된 자료 중 관련 자료와 무관 자료를 함께 "
        "주면서 LLM이 무관 자료를 무시하도록 미세조정하는 기법이다. 특정 도메인 RAG에서 답변 정확도가 "
        "현저히 향상되었음을 실험으로 입증한다."
    ),
    "arxiv:2104.07567v3": (
        "DPR(Dense Passage Retrieval)은 BM25 같은 희소 벡터 기반 전통 검색을 넘어, "
        "단답 질문 응답 과제에서 후보 단락을 임베딩 기반 밀집 벡터로 검색하는 방식이다. "
        "기존 IR 시스템 대비 검색 품질과 후속 QA 정확도를 모두 끌어올렸다."
    ),
    "arxiv:2305.06983v1": (
        "Active RAG는 LLM이 답변을 생성하는 도중에도 필요한 시점에 추가 검색을 능동적으로 트리거하도록 "
        "설계된 RAG 변형이다. 한 번의 사전 검색만으로 부족한 다단계 질의에서 환각을 크게 줄이고 답변의 "
        "사실성을 개선한다."
    ),
}


# =============================================================================
# LIVE 모드 — Gemini API 호출
# =============================================================================
def make_live_generator():
    """API 키가 있으면 실제 호출 함수를, 없으면 None을 반환."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
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
        "(2) 자료의 주된 주장과 활용 맥락을 함께 담습니다. "
        "(3) 존댓말이 아닌 평서체로 작성합니다."
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
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "system_instruction": SYS,
                "temperature": 0.2,
                "max_output_tokens": 600,
                "response_mime_type": "application/json",
            },
        )
        try:
            return json.loads(resp.text)["summary"]
        except Exception as ex:
            return f"[요약 생성 실패: {ex}]"

    return generate


# =============================================================================
# 메인
# =============================================================================
def main():
    INPUT = os.path.join("..", "ch06", "ch06_collected_embedded.jsonl")
    if not os.path.exists(INPUT):
        print(f"[ERR] {INPUT} 없음 — 먼저 Ch.6 자료를 만드세요.")
        sys.exit(1)

    print(f"[입력] {INPUT}")
    collected = pd.read_json(INPUT, lines=True)
    print(f"  → {len(collected)} 레코드")

    # 모드 결정
    live = make_live_generator()
    if live:
        print("\n[LIVE 모드] GEMINI_API_KEY 감지 — 실제 Gemini API 호출")
    else:
        print("\n[DEMO 모드] API 키 없음 — 사전 작성된 데모 요약 사용")
        print("            (본인 PC에서 노트북 실행 시 실제 LLM 요약으로 갱신됩니다)")

    # summary 채우기
    for idx, row in collected.iterrows():
        doc_id = row["id"]
        if row.get("summary"):
            continue  # 이미 채워진 자료는 건너뜀 (재실행 안전)

        if live:
            print(f"  [{idx+1}/{len(collected)}] {doc_id} 요약 생성 중…")
            summary = live(row["title"], row.get("description", ""))
            time.sleep(5)  # rate limit 방어
        else:
            summary = DEMO_SUMMARIES.get(
                doc_id,
                "[요약 자리 — 본인 PC에서 노트북을 실행해 LLM이 생성하도록 하세요]",
            )

        collected.at[idx, "summary"] = summary
        print(f"  → {summary[:80]}…")

    # 저장
    collected.to_json(
        "ch07_collected_complete.jsonl",
        orient="records", lines=True, force_ascii=False,
    )
    print(f"\n[OK] ch07_collected_complete.jsonl ({len(collected)} 레코드)")

    # Ch.3 AI 확장 6필드 진행률
    print("\n[Ch.3 §3.3 AI 확장 6필드 최종 채움 상태]")
    ext_fields = ["summary", "keywords", "chunk_ids",
                  "embedding_id", "source_url", "license_code"]
    for f in ext_fields:
        if f not in collected.columns:
            print(f"  {f:<15}: 0/{len(collected)} (없음)")
            continue
        filled = sum(
            1 for v in collected[f]
            if (isinstance(v, list) and v) or
               (isinstance(v, str) and v.strip())
        )
        bar = "█" * filled + "░" * (len(collected) - filled)
        print(f"  {f:<15}: {filled}/{len(collected)}  {bar}")

    if all(
        sum(1 for v in collected[f] if (isinstance(v, list) and v) or (isinstance(v, str) and v.strip())) == len(collected)
        for f in ext_fields
    ):
        print("\n✅ 본서 스키마 22필드 모두 채워졌습니다. Ch.8 RAG 챗봇 준비 완료.")


if __name__ == "__main__":
    main()
