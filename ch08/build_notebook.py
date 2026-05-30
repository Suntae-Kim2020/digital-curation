# -*- coding: utf-8 -*-
r"""ch08_rag_chatbot.ipynb 생성기"""
import io, sys
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

nb = new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12"},
}

cells = []

cells.append(new_markdown_cell(
    "# Chapter 8 §8.2~§8.5 실습 — 작동하는 RAG 챗봇\n"
    "\n"
    "> 『AI 레디 데이터와 디지털 큐레이션』 Chapter 8의 §8.2부터 §8.5까지 실습 노트북.\n"
    "> 본 챕터는 본서 본격 학습의 클라이맥스 — Ch.6 의미 검색 + Ch.7 LLM 호출을 결합한다.\n"
    "\n"
    "## 학습 목표\n"
    "- RAG의 4단계(질의·검색·증강·생성)를 실제 코드로 통합한다\n"
    "- 검색 결과를 컨텍스트로 주입하는 프롬프트를 작성한다\n"
    "- 답변에 출처(citation)가 자동으로 따라붙도록 만든다\n"
    "- 환각·관련성·완전성 세 관점에서 답변 품질을 점검한다\n"
    "- 자료에 없는 질문에 챗봇이 어떻게 안전하게 답하는지 확인한다\n"
    "\n"
    "## 산출물\n"
    "- 같은 폴더의 `ch08_rag.py` 모듈을 import해서 사용\n"
    "- 다섯 시연 질의에 대한 답변과 출처\n"
    "\n"
    "## 사전 조건\n"
    "- Ch.6 §6.3 실행으로 ChromaDB 컬렉션 `ai_ready_chunks` 적재 완료\n"
    "- Ch.7 §7.4 실행으로 스키마 22필드 완성 (`../ch07/ch07_collected_complete.jsonl`)\n"
    "- 환경변수 `GEMINI_API_KEY` 등록"
))

cells.append(new_markdown_cell(
    "## 0단계 · 환경 점검\n"
    "\n"
    "필요한 모든 도구는 Ch.6·Ch.7에서 이미 설치돼 있다. 추가 설치는 없다.\n"
    "환경변수와 ChromaDB 컬렉션만 점검한다."
))

cells.append(new_code_cell(
    "import os\n"
    "\n"
    "assert os.getenv('GEMINI_API_KEY'), (\n"
    "    'GEMINI_API_KEY가 설정되지 않았습니다. 책 §6.2.4를 참조해 등록 후 다시 실행하세요.'\n"
    ")\n"
    "\n"
    "import chromadb\n"
    "db = chromadb.PersistentClient(path='./chroma_db')\n"
    "try:\n"
    "    col = db.get_collection('ai_ready_chunks')\n"
    "    print(f'ChromaDB 컬렉션 OK — 청크 {col.count()}개 적재됨')\n"
    "except Exception as ex:\n"
    "    raise RuntimeError(\n"
    "        '컬렉션을 찾을 수 없습니다. 먼저 ch06_vector_search.ipynb를 실행해 컬렉션을 만드세요.'\n"
    "    ) from ex"
))

cells.append(new_markdown_cell(
    "## 1단계 · ch08_rag 모듈 import\n"
    "\n"
    "본 챕터의 핵심 함수들(`retrieve`, `build_prompt`, `generate`, `ask_rag`)은 \n"
    "같은 폴더의 `ch08_rag.py` 모듈에 들어 있다. 책 §8.2~§8.3의 내용을 정리한 것이다."
))

cells.append(new_code_cell(
    "from ch08_rag import ask_rag, print_rag_result, ask_rag_verbose\n"
    "\n"
    "print('ch08_rag 모듈 로드 완료')"
))

cells.append(new_markdown_cell(
    "## 2단계 · §8.2.4 첫 RAG 호출\n"
    "\n"
    "한 줄짜리 질의를 던지고 답변·출처·거리값을 함께 출력한다."
))

cells.append(new_code_cell(
    "r = ask_rag('RAG가 환각을 줄이는 원리는?')\n"
    "print_rag_result(r)"
))

cells.append(new_markdown_cell(
    "## 3단계 · §8.3.3 자세한 출력 — 원본 청크까지\n"
    "\n"
    "답변과 함께 검색된 원본 청크의 앞부분 200자까지 함께 본다. 답변과 자료를 즉시 대조 가능."
))

cells.append(new_code_cell(
    "ask_rag_verbose('DPR과 BM25의 차이는?', k=3)"
))

cells.append(new_markdown_cell(
    "## 4단계 · §8.2.2 메타데이터 필터로 범위 좁히기\n"
    "\n"
    "특정 자료의 청크 안에서만 검색하고 싶을 때."
))

cells.append(new_code_cell(
    "# RAG 논문(arxiv:2005.11401v4)의 청크 안에서만\n"
    "r = ask_rag(\n"
    "    'augmentation 기법의 효과는 어떻게 측정되었나?',\n"
    "    k=3,\n"
    "    where={'doc_id': 'arxiv:2005.11401v4'},\n"
    ")\n"
    "print_rag_result(r)"
))

cells.append(new_markdown_cell(
    "## 5단계 · 시연 질의 5건 — 마지막은 환각 방어 시험\n"
    "\n"
    "다섯 번째 질문은 본서 자료(arXiv RAG 논문 5건)에 없는 주제다. \n"
    "RAG가 \"제공된 자료에서는 확인되지 않습니다\"라고 답하면 환각 방어 작동.\n"
    "그럴듯한 답변을 만들어 내면 §8.2.3의 제약 규칙을 더 강화해야 한다는 신호."
))

cells.append(new_code_cell(
    "import json\n"
    "with open('ch08_demo_queries.json', 'r', encoding='utf-8') as f:\n"
    "    queries = json.load(f)\n"
    "\n"
    "for q in queries:\n"
    "    print_rag_result(ask_rag(q))\n"
    "    print()  # 구분"
))

cells.append(new_markdown_cell(
    "## 6단계 · §8.4 답변 품질 직접 점검\n"
    "\n"
    "다음 세 가지를 손수 점검해 보세요.\n"
    "\n"
    "1. **환각 (Hallucination)** — 5단계 답변에 자료에 없는 사실·이름·통계가 보이는가?\n"
    "2. **관련성 (Relevance)** — 검색된 청크 3개가 질문과 정말 관련 있는가?\n"
    "3. **완전성 (Completeness)** — 자료에 있는데 답변이 빠뜨린 내용이 있는가?\n"
    "\n"
    "문제가 발견되면 §8.4.1 표를 참조해 어디를 튜닝할지 결정한다."
))

cells.append(new_markdown_cell(
    "## 7단계 · 본인 질문 던져 보기\n"
    "\n"
    "아래 셀의 `MY_QUERY`를 자유롭게 바꿔 가며 챗봇과 대화해 보세요."
))

cells.append(new_code_cell(
    "MY_QUERY = '본 챗봇이 다루는 자료가 무엇인지 알려 주세요'\n"
    "print_rag_result(ask_rag(MY_QUERY))"
))

cells.append(new_markdown_cell(
    "## 다음 단계\n"
    "\n"
    "- Ch.9 §9.1~§9.3 : 본 챕터의 RAG 챗봇을 **자기 기관 자료**로 확장하는 팀 미니 프로젝트\n"
    "- Ch.10 §10.1~§10.4 : 저작권·개인정보·운영 비용·거버넌스"
))

nb["cells"] = cells

with open("ch08_rag_chatbot.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[OK] ch08_rag_chatbot.ipynb ({len(cells)} cells)")
