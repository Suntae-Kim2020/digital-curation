"""[실습 보조 스크립트 · 선택] Gemini 검색 그라운딩(Google Search Grounding)

────────────────────────────────────────────────────────────────────
이 스크립트는 교재의 핵심 실습(Ch.6 임베딩·검색 → Ch.8 RAG 챗봇)에
'필수'가 아니다. "내 자료가 아니라 웹의 최신 정보가 필요할 때 LLM에
검색을 붙이는 또 다른 방법"을 맛보는 선택용 보조 자료다.
────────────────────────────────────────────────────────────────────

■ 검색 그라운딩이란
  LLM이 답을 만들기 '전에' 실시간으로 Google 검색을 수행하고, 그 검색
  결과(웹 페이지)를 근거(grounding)로 삼아 답하는 기능이다. 답변과 함께
  '어떤 검색어로 찾았고, 어떤 페이지를 참고했는지'(출처)를 돌려준다.

■ 왜 쓰나 — 세 가지 효과
  (1) 최신성   : LLM은 학습 시점 이후를 모른다(지식 컷오프). 검색으로 보완.
  (2) 환각 감소 : 모르는 것을 그럴듯하게 지어내는 대신 실제 웹 근거에 묶는다.
  (3) 출처 제시 : 답의 근거 URL을 함께 받아 사실 확인이 가능하다.
                 (교재 Ch.8 §8.3 '답변에 출처 표시'와 같은 철학)

■ 동작 4단계
  ① 모델이 질문을 보고 '검색이 필요한가'를 스스로 판단
  ② 검색 질의(web_search_queries)를 만들어 Google 검색 수행
  ③ 상위 결과 페이지 내용을 컨텍스트로 가져와 답변 생성
  ④ 답변 + 출처(grounding_chunks: 제목·URL)를 함께 반환

■ '진실의 출처'는 공개 웹이다 — 내 자료가 아니다
  그라운딩은 인터넷(구글 색인)만 검색한다. 내가 구축한 ChromaDB(내 기관
  자료)는 전혀 보지 않는다. 그래서 이 스크립트는 '내 데이터 검색'이 아니다.

■ 교재의 RAG(내 데이터)와의 차이
  ┌───────────┬───────────────────────┬───────────────────────────┐
  │ 구분      │ 검색 그라운딩(이 파일) │ 교재 RAG(Ch.6+Ch.8)        │
  ├───────────┼───────────────────────┼───────────────────────────┤
  │ 검색원    │ 공개 웹(Google)        │ 내 ChromaDB(내 자료)       │
  │ 누가 검색 │ LLM이 알아서           │ 내 코드가 직접             │
  │ 내 자료?  │ 사용 안 함             │ 사용함                     │
  │ 용도      │ 최신·외부 사실         │ 내 기관 자료에 대한 질문   │
  └───────────┴───────────────────────┴───────────────────────────┘
  · 내 기관 자료로 답하게 하려면 → 교재 RAG(Ch.8). (그라운딩 아님)
  · 웹 최신 정보로 답하게 하려면 → 그라운딩(이 스크립트)
  · 둘 다 쓰려면 → 내 ChromaDB 청크를 프롬프트에 넣고 google_search 도구를
    함께 켜는 '하이브리드'를 직접 구성해야 한다(교재 표준 범위 밖).

■ 주의·한계
  · 출처가 항상 붙지는 않는다 — 모델이 검색을 안 쓰면 grounding_metadata가 빈다.
  · 웹 결과의 신뢰도는 보장되지 않으니 출처 URL을 직접 확인하는 습관이 필요하다.
  · 그라운딩 호출은 별도 쿼터·요금이 있을 수 있다(교재 Ch.10 비용 관점과 연결).
    무료 한도·가격은 https://ai.google.dev 와 AI Studio에서 확인.

────────────────────────────────────────────────────────────────────
■ 준비 (교재 Ch.6 §6.2.4)
  1) pip install google-genai
  2) 환경변수 GEMINI_API_KEY 등록
     🪟 PowerShell:  $env:GEMINI_API_KEY = 'AIza...실제 키...'
     🍎 zsh:         export GEMINI_API_KEY='AIza...실제 키...'
  ※ 키는 https://aistudio.google.com/apikey 에서 무료 발급
■ 실행
  python genAPI_grounding.py
────────────────────────────────────────────────────────────────────
"""

import io
import os
import sys

from google import genai
from google.genai import types

# Windows cp949 콘솔에서 한글 출력이 깨지지 않도록 stdout을 UTF-8로 (교재 함정 #1)
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
except Exception:
    pass

# API 키 점검 — 없으면 친절한 메시지로 즉시 중단 (교재 §6.4.1 · 함정 #5)
if not os.environ.get("GEMINI_API_KEY"):
    raise SystemExit(
        "GEMINI_API_KEY가 설정되지 않았습니다. "
        "교재 Ch.6 §6.2.4를 참고해 환경변수를 등록한 뒤 다시 실행하세요."
    )


def generate_with_search(question: str):
    client = genai.Client()  # 환경변수 GEMINI_API_KEY 를 자동으로 사용

    # Google 검색 그라운딩 도구
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools=[grounding_tool])

    response = client.models.generate_content(
        model="gemini-2.5-flash",  # 교재 표준 LLM (검색 그라운딩 지원)
        contents=question,
        config=config,
    )

    print("【질문】", question)
    print("\n【답변】")
    print(response.text)

    # 그라운딩 메타데이터 — 검색 질의와 출처(없을 수도 있으니 방어적으로 접근)
    meta = response.candidates[0].grounding_metadata if response.candidates else None

    if meta and getattr(meta, "web_search_queries", None):
        print("\n【검색에 사용된 질의】")
        for q in meta.web_search_queries:
            print("  -", q)

    chunks = getattr(meta, "grounding_chunks", None) if meta else None
    if chunks:
        print("\n【출처】")
        for i, chunk in enumerate(chunks, 1):
            web = getattr(chunk, "web", None)
            if web:
                print(f"  [{i}] {web.title} — {web.uri}")
    else:
        print("\n(이번 응답에는 검색 그라운딩 출처가 붙지 않았습니다.)")


if __name__ == "__main__":
    generate_with_search(
        "공공데이터를 활용한 생성형 AI 서비스에 대한 "
        "최근 한국 정부의 정책이나 가이드라인을 한두 가지 알려 줘."
    )
