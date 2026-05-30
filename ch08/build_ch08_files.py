# -*- coding: utf-8 -*-
r"""
Ch.8 산출물 점검기

본 챕터의 핵심 산출물은 데이터 파일이 아니라 작동하는 RAG 모듈(ch08_rag.py)이다.
빌드 스크립트는 사전 조건을 점검하고 시연 질의 목록을 안내한다.

실제 RAG 호출은 GEMINI_API_KEY + ChromaDB 컬렉션이 필요하므로
저장소 빌드 단계에서는 호출하지 않고, 본인 PC에서 노트북 또는
ch08_rag.py 직접 실행으로 시연한다.
"""
import io
import os
import sys
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def main():
    print("=" * 60)
    print(" Chapter 8. RAG 챗봇 구축 — 산출물 점검")
    print("=" * 60)

    # 사전 조건 점검
    print("\n[1] 사전 조건")

    # Ch.7 산출물 (스키마 완성)
    ch07_file = os.path.join("..", "ch07", "ch07_collected_complete.jsonl")
    if os.path.exists(ch07_file):
        print(f"  [OK]  Ch.7 산출물: {ch07_file}")
    else:
        print(f"  [WARN] Ch.7 산출물 없음: {ch07_file}")
        print("         → Ch.7 실습을 먼저 진행하세요.")

    # ch08_rag.py 모듈
    rag_module = "ch08_rag.py"
    if os.path.exists(rag_module):
        print(f"  [OK]  RAG 통합 모듈: {rag_module}")
    else:
        print(f"  [ERR] {rag_module} 없음 — 저장소 동기화 필요")

    # 노트북
    nb = "ch08_rag_chatbot.ipynb"
    if os.path.exists(nb):
        print(f"  [OK]  실습 노트북: {nb}")
    else:
        print(f"  [ERR] {nb} 없음 — 저장소 동기화 필요")

    # 런타임 의존성 (사용자 PC 기준)
    print("\n[2] 런타임 점검 (본인 PC에서 실행 시)")
    print("  [필요] 환경변수 GEMINI_API_KEY (책 §6.2.4)")
    print("  [필요] Ch.6 ChromaDB 컬렉션 'ai_ready_chunks' (책 §6.3)")
    print("         확인: python -c \"import chromadb; "
          "print(chromadb.PersistentClient('./chroma_db').get_collection('ai_ready_chunks').count())\"")

    # 시연 질의 5건 — 양자컴퓨팅 환각 시험 포함
    DEMO_QUERIES = [
        "RAG가 환각을 줄이는 원리는?",
        "DPR과 BM25의 차이는?",
        "Active RAG는 일반 RAG와 무엇이 다른가?",
        "RAFT는 어떤 환경에 효과적인가?",
        "본서가 다루지 않는 주제 — 양자 컴퓨팅에 대해 알려 줘",
    ]

    print("\n[3] 본 챕터의 시연 질의 5건")
    for i, q in enumerate(DEMO_QUERIES, start=1):
        marker = "⚠️ (환각 방어 시험)" if "양자 컴퓨팅" in q else ""
        print(f"  {i}. {q}  {marker}")

    # 시연 질의 목록을 파일로도 저장 (학습자가 노트북에서 그대로 불러쓸 수 있게)
    with open("ch08_demo_queries.json", "w", encoding="utf-8") as f:
        json.dump(DEMO_QUERIES, f, ensure_ascii=False, indent=2)
    print(f"\n[저장] ch08_demo_queries.json ({len(DEMO_QUERIES)}건)")

    # 실행 방법
    print("\n[4] 실행")
    print("  옵션 A — 노트북: jupyter notebook ch08_rag_chatbot.ipynb")
    print("  옵션 B — 모듈 직접 실행: python ch08_rag.py")
    print("  옵션 C — Python 셸에서:")
    print("            from ch08_rag import ask_rag, print_rag_result")
    print("            print_rag_result(ask_rag('RAG가 무엇인가?'))")

    print()


if __name__ == "__main__":
    main()
