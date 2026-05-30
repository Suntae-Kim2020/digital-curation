# -*- coding: utf-8 -*-
r"""
Ch.9 산출물 생성기 — 미니 프로젝트 팀 자산

본 챕터의 산출물은 데이터가 아니라 팀이 자기 기관 자료로 챗봇을 만들 때 쓸:
- 평가 루브릭 (4기준 × 4단계, JSON)
- 시험 질의 템플릿 (JSON)
- 사전 조건·실행 안내 출력
"""
import io
import os
import sys
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# =============================================================================
# 평가 루브릭 — 책 §9.3.2
# =============================================================================
RUBRIC = {
    "name": "Ch.9 미니 프로젝트 평가 루브릭",
    "max_score_per_criterion": 4,
    "total_max": 16,
    "pass_threshold": 12,
    "criteria": [
        {
            "key":  "data_quality",
            "name": "데이터 품질",
            "levels": {
                1: "본문 추출 깨짐 다수, 메타데이터 부실",
                2: "추출은 되나 노이즈 자주, 일부 필드 누락",
                3: "대체로 깨끗, 일부 정제 필요",
                4: "본문 깨끗, 메타데이터 충실, 스키마 22필드 모두 채움",
            },
        },
        {
            "key":  "search_relevance",
            "name": "검색 정확도",
            "levels": {
                1: "관련 없는 청크가 자주 나옴",
                2: "관련 있으나 정확히 맞는 것이 끼지 않을 때 잦음",
                3: "대체로 관련, 가장 좋은 것은 1·2위 사이",
                4: "상위 청크 3개가 모두 명확히 관련",
            },
        },
        {
            "key":  "answer_faithfulness",
            "name": "답변 충실성",
            "levels": {
                1: "자료에 없는 사실·이름·통계 자주 발생",
                2: "추측이 종종 섞임",
                3: "대체로 자료 기반, 가끔 추측",
                4: "자료 기반 일관, 모르는 것은 솔직히 인정",
            },
        },
        {
            "key":  "citation",
            "name": "출처 표시",
            "levels": {
                1: "출처 표시 자주 빠짐",
                2: "출처는 있으나 잘못된 ID 섞임",
                3: "대체로 정확, 가끔 누락",
                4: "모든 답변에 정확한 청크 ID, 출처 추적 가능",
            },
        },
    ],
    "self_check_8": [
        "PDF 추출에서 본문 깨짐이 5건 이하인가",
        "본서 스키마 22필드가 자관 자료에 모두 채워졌는가",
        "ChromaDB 컬렉션의 청크 수가 예상값과 일치하는가",
        "Ch.7 LLM 요약이 자료에 실제로 있는 내용을 짚는가",
        "시험 질의 3~4건이 만족스럽게 답하는가",
        "환각 방어 시험에서 챗봇이 '확인되지 않습니다'라고 답하는가",
        "답변마다 [출처: 청크ID] 표시가 들어가는가",
        "시연 화면 캡처를 챕터 폴더에 저장했는가",
    ],
}


# =============================================================================
# 시험 질의 템플릿 — 책 §9.2.4
# =============================================================================
DEMO_QUERIES_TEMPLATE = {
    "instructions": (
        "각 팀은 다음 5개 자리에 자기 기관 자료에 맞춘 실제 질의를 채워 넣는다. "
        "1~4번은 답이 자료에 분명히 있는 검증 가능 질의로. "
        "5번은 반드시 '자료에 없는 주제'로 두어 환각 방어 시험을 한다 (책 §8.5 참조)."
    ),
    "queries": [
        {
            "n": 1,
            "type": "fact_lookup",
            "description": "기본 사실 확인 — 자료에서 직접 찾을 수 있는 정보",
            "example_for_thesis": "최근 5년간 가장 자주 쓰인 데이터 증강 기법은?",
            "example_for_archive": "1990년대 행정 개혁의 주요 정책 변화는?",
            "your_query": "(여기에 팀 질의 작성)",
        },
        {
            "n": 2,
            "type": "comparison",
            "description": "두 항목 비교 — 자료에서 양쪽 근거를 찾아야 함",
            "example_for_thesis": "BERT와 GPT 계열을 사용한 학위논문 수 비교는?",
            "example_for_archive": "정책 A와 정책 B의 도입 배경 차이는?",
            "your_query": "(여기에 팀 질의 작성)",
        },
        {
            "n": 3,
            "type": "explanation",
            "description": "원리·과정 설명 — 자료에서 메커니즘을 추출",
            "example_for_thesis": "한국어 BERT를 fine-tuning할 때 자주 쓰이는 절차는?",
            "example_for_archive": "OO 사업의 의사결정 절차를 단계별로 설명",
            "your_query": "(여기에 팀 질의 작성)",
        },
        {
            "n": 4,
            "type": "recommendation",
            "description": "추천·매칭 — 자료 안에서 적합한 것을 골라야 함",
            "example_for_thesis": "데이터 증강을 처음 공부하는 학생에게 어느 논문을 추천?",
            "example_for_archive": "이 주제에 관심 있는 연구자가 먼저 봐야 할 자료는?",
            "your_query": "(여기에 팀 질의 작성)",
        },
        {
            "n": 5,
            "type": "out_of_scope",
            "description": "⚠️ 환각 방어 시험 — 자료에 없는 주제를 일부러 질문",
            "example_for_thesis": "양자 컴퓨팅 분야 학위논문이 몇 편 있나요? (자료에 없음)",
            "example_for_archive": "최근 인공지능 정책의 영향은? (자료가 1990년대만 다룸)",
            "your_query": "(여기에 팀 질의 작성 — '확인되지 않습니다' 답을 기대)",
        },
    ],
}


def main():
    print("=" * 60)
    print(" Chapter 9. 미니 프로젝트 — 팀 자산 생성")
    print("=" * 60)

    # 루브릭 저장
    with open("ch09_rubric.json", "w", encoding="utf-8") as f:
        json.dump(RUBRIC, f, ensure_ascii=False, indent=2)
    print("\n[OK] ch09_rubric.json  (4기준 × 4단계 평가 루브릭)")

    # 질의 템플릿 저장
    with open("ch09_demo_queries_template.json", "w", encoding="utf-8") as f:
        json.dump(DEMO_QUERIES_TEMPLATE, f, ensure_ascii=False, indent=2)
    print("[OK] ch09_demo_queries_template.json  (5개 시험 질의 템플릿)")

    # 템플릿 파일 안내
    print("\n[팀 템플릿]")
    print("  templates/build_my_data.py  — 자기 기관 PDF → 본서 스키마")
    print("  templates/my_rag.py         — ch08_rag 복사본 (컬렉션 이름 변경 자리)")

    # 사전 조건
    print("\n[사전 조건]")
    needed = [
        ("Ch.5 ~ Ch.8 코드 자산", "../ch05/build_ch05_files.py 등"),
        ("GEMINI_API_KEY",       "Ch.6 §6.2.4"),
        ("ChromaDB 라이브러리",   "Ch.6 §6.3.2 (pip install chromadb)"),
        ("Gemini API 패키지",    "Ch.6 §6.3.2 (pip install google-genai)"),
    ]
    for name, where in needed:
        print(f"  [필요] {name:<22} ({where})")

    # 워크숍 시간 배분
    print("\n[90분 워크숍 시간 배분]")
    schedule = [
        ("0~15분",  "단계 1 — 자료 준비 (PDF 10~20건 → data/)"),
        ("15~35분", "단계 2 — 본문 추출·스키마 매핑 → my_collected.jsonl"),
        ("35~65분", "단계 3 — 청킹·임베딩·요약 (Ch.5~Ch.7 코드 재사용)"),
        ("65~90분", "단계 4 — RAG 조립·테스트 + 시험 질의 작성"),
    ]
    for time, task in schedule:
        print(f"  {time:<10} {task}")

    print("\n[8분 시연 형식 — 팀당]")
    print("  1분  소개 (자관·자료·건수)")
    print("  3분  시연 (시험 질의 3~4건, 마지막은 환각 방어)")
    print("  1분  회고 (어디가 어려웠는지)")
    print("  3분  Q&A")


if __name__ == "__main__":
    main()
