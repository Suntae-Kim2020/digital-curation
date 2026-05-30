# -*- coding: utf-8 -*-
r"""ch06_vector_search.ipynb 생성기"""
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
    "# Chapter 6 §6.3~§6.5 실습 — 임베딩과 벡터 검색\n"
    "\n"
    "> 『AI 레디 데이터와 디지털 큐레이션』 Chapter 6의 §6.3부터 §6.5까지 실습 노트북.\n"
    "> 본인 PC의 가상환경(.venv)에서 실행한다.\n"
    "\n"
    "## 학습 목표\n"
    "- Gemini Embedding으로 Ch.5의 청크를 768차원 임베딩으로 변환한다\n"
    "- ChromaDB의 PersistentClient로 영구 저장 가능한 컬렉션을 만든다\n"
    "- 사용자 질의에 의미적으로 가까운 청크 상위 N개를 찾아낸다\n"
    "- 메타데이터(자료 ID)로 검색 범위를 좁힌다\n"
    "- Ch.3 스키마의 embedding_id 필드를 채운다\n"
    "\n"
    "## 산출물\n"
    "1. `./chroma_db/` — PC에 저장된 ChromaDB 컬렉션 (다음 실행 때 재사용 가능)\n"
    "2. `ch06_collected_embedded.jsonl` — Ch.3 스키마 AI 확장 6필드 중 5개 채워진 완성형\n"
    "\n"
    "## 선행\n"
    "- Ch.5 §5.5 청크 결과 (`../ch05/ch05_chunks.jsonl`)\n"
    "- Ch.6 §6.2.4 Gemini API 키 발급 (GEMINI_API_KEY 환경변수)"
))

cells.append(new_markdown_cell(
    "## 0단계 · 환경 점검\n"
    "\n"
    "본 챕터에서 새로 쓸 두 라이브러리를 가상환경에 설치한다.\n"
    "\n"
    "- **chromadb** — 영구 저장 가능한 벡터 데이터베이스. 별도 서버 없이 Python 한 줄로 시작.\n"
    "- **google-genai** — Gemini API 호출 공식 Python 패키지. 임베딩·LLM 호출 모두 이 패키지 하나로.\n"
    "\n"
    "**🪟 Windows (PowerShell)** · **🍎 Mac (zsh/bash)** 모두:\n"
    "```\n"
    "pip install chromadb google-genai pandas\n"
    "```\n"
    "\n"
    "API 키는 환경변수 `GEMINI_API_KEY`에 미리 설정돼 있어야 한다. 책 §6.2.4 참조."
))

cells.append(new_code_cell(
    "import os, pandas as pd\n"
    "import chromadb\n"
    "from google import genai\n"
    "\n"
    "API_KEY = os.getenv('GEMINI_API_KEY')\n"
    "if not API_KEY:\n"
    "    raise RuntimeError(\n"
    "        'GEMINI_API_KEY가 설정되지 않았습니다. '\n"
    "        'https://aistudio.google.com 에서 발급 후 환경변수로 등록하세요. '\n"
    "        '(책 §6.2.4)')\n"
    "\n"
    "ai = genai.Client()  # 환경변수에서 키 자동 로드\n"
    "print('Gemini Client 준비 완료')\n"
    "print('ChromaDB', chromadb.__version__)"
))

cells.append(new_markdown_cell(
    "## 1단계 · §6.3.2 ChromaDB 클라이언트와 컬렉션 만들기\n"
    "\n"
    "PersistentClient는 데이터를 지정 폴더(`./chroma_db`)에 영구 저장한다.\n"
    "두 번째 실행부터는 같은 코드가 기존 데이터를 그대로 불러온다."
))

cells.append(new_code_cell(
    "client = chromadb.PersistentClient(path='./chroma_db')\n"
    "\n"
    "collection = client.get_or_create_collection(\n"
    "    name='ai_ready_chunks',\n"
    "    metadata={'hnsw:space': 'cosine'},  # 거리 척도: 코사인\n"
    ")\n"
    "print(f'컬렉션 {collection.name}: 현재 {collection.count()}개 청크')"
))

cells.append(new_markdown_cell(
    "## 2단계 · §6.3.3 Ch.5 청크를 임베딩해 적재\n"
    "\n"
    "Ch.5 결과(`../ch05/ch05_chunks.jsonl`)에서 청크를 읽어\n"
    "각 청크 텍스트를 Gemini로 768차원 임베딩으로 변환하고 ChromaDB에 넣는다.\n"
    "\n"
    "이미 같은 ID로 적재된 청크가 있으면 skip 한다(재실행 안전)."
))

cells.append(new_code_cell(
    "INPUT = '../ch05/ch05_chunks.jsonl'\n"
    "chunks = pd.read_json(INPUT, lines=True)\n"
    "print(f'Ch.5 청크 {len(chunks)}개 로드')\n"
    "\n"
    "# 이미 적재된 ID 확인\n"
    "existing_ids = set(collection.get()['ids']) if collection.count() else set()\n"
    "new_chunks = chunks[~chunks['chunk_id'].isin(existing_ids)]\n"
    "print(f'적재할 신규 청크: {len(new_chunks)}개')\n"
    "\n"
    "if len(new_chunks) > 0:\n"
    "    texts = new_chunks['text'].tolist()\n"
    "    ids   = new_chunks['chunk_id'].tolist()\n"
    "    metas = [\n"
    "        {'doc_id': r['doc_id'],\n"
    "         'chunk_index': int(r['chunk_index'])}\n"
    "        for _, r in new_chunks.iterrows()\n"
    "    ]\n"
    "\n"
    "    # Gemini 임베딩 — 배치 호출\n"
    "    resp = ai.models.embed_content(\n"
    "        model='gemini-embedding-001',\n"
    "        contents=texts,\n"
    "        config={'output_dimensionality': 768},\n"
    "    )\n"
    "    embeddings = [e.values for e in resp.embeddings]\n"
    "\n"
    "    collection.add(\n"
    "        ids=ids,\n"
    "        documents=texts,\n"
    "        embeddings=embeddings,\n"
    "        metadatas=metas,\n"
    "    )\n"
    "    print(f'적재 완료. 총 {collection.count()}개 청크.')"
))

cells.append(new_markdown_cell(
    "## 3단계 · §6.4 의미 검색 — 질의 한 줄로 유사 청크 찾기\n"
    "\n"
    "질의 텍스트를 같은 모델로 임베딩한 다음 ChromaDB에 가까운 청크 상위 N개를 부탁한다."
))

cells.append(new_code_cell(
    "def search(query, k=3, where=None):\n"
    "    '''의미 검색 — 질의에 가까운 청크 k개 반환'''\n"
    "    q_resp = ai.models.embed_content(\n"
    "        model='gemini-embedding-001',\n"
    "        contents=[query],\n"
    "        config={'output_dimensionality': 768},\n"
    "    )\n"
    "    q_emb = q_resp.embeddings[0].values\n"
    "\n"
    "    kwargs = {\n"
    "        'query_embeddings': [q_emb],\n"
    "        'n_results': k,\n"
    "    }\n"
    "    if where:\n"
    "        kwargs['where'] = where\n"
    "    return collection.query(**kwargs)\n"
    "\n"
    "\n"
    "# 사용 예\n"
    "r = search('RAG가 무엇인지 설명해 줘', k=3)\n"
    "for i in range(len(r['ids'][0])):\n"
    "    cid  = r['ids'][0][i]\n"
    "    dist = r['distances'][0][i]\n"
    "    text = r['documents'][0][i]\n"
    "    print(f'\\n[{i+1}] {cid}  (코사인 거리 {dist:.3f})')\n"
    "    print(f'    {text[:160]}…')"
))

cells.append(new_markdown_cell(
    "## 4단계 · §6.4.2 메타데이터 필터로 범위 좁히기\n"
    "\n"
    "특정 자료의 청크만, 또는 여러 자료 중에서만 검색."
))

cells.append(new_code_cell(
    "# 특정 자료 1건의 청크만\n"
    "r = search('augmentation', k=3,\n"
    "           where={'doc_id': 'arxiv:2005.11401v4'})\n"
    "print('자료 한 건 안에서 검색:')\n"
    "for i in range(len(r['ids'][0])):\n"
    "    print(f'  [{i+1}] {r[\"ids\"][0][i]}  dist={r[\"distances\"][0][i]:.3f}')\n"
    "\n"
    "# 두 자료 안에서\n"
    "r = search('augmentation', k=3,\n"
    "           where={'doc_id': {'$in': [\n"
    "               'arxiv:2005.11401v4',\n"
    "               'arxiv:2312.10997v5',\n"
    "           ]}})\n"
    "print('\\n두 자료 안에서 검색:')\n"
    "for i in range(len(r['ids'][0])):\n"
    "    print(f'  [{i+1}] {r[\"ids\"][0][i]}  dist={r[\"distances\"][0][i]:.3f}')"
))

cells.append(new_markdown_cell(
    "## 5단계 · §6.5 embedding_id 채워서 스키마 마무리\n"
    "\n"
    "Ch.3 스키마의 마지막 AI 확장 필드 `embedding_id`를 채운다.\n"
    "자료 1건당 첫 청크의 ID를 대표값으로 둔다."
))

cells.append(new_code_cell(
    "collected = pd.read_json('../ch05/ch05_collected_filled.jsonl', lines=True)\n"
    "\n"
    "for idx, row in collected.iterrows():\n"
    "    chunk_ids = row.get('chunk_ids') or []\n"
    "    if isinstance(chunk_ids, list) and chunk_ids:\n"
    "        collected.at[idx, 'embedding_id'] = chunk_ids[0]\n"
    "\n"
    "collected.to_json('ch06_collected_embedded.jsonl',\n"
    "                  orient='records', lines=True, force_ascii=False)\n"
    "\n"
    "print('Ch.3 스키마 AI 확장 6필드 채움 상태:')\n"
    "for f in ['summary','keywords','chunk_ids','embedding_id','source_url','license_code']:\n"
    "    if f not in collected.columns:\n"
    "        print(f'  {f:<15}: 0/{len(collected)} (없음)')\n"
    "        continue\n"
    "    filled = sum(1 for v in collected[f]\n"
    "                 if (isinstance(v, list) and v) or\n"
    "                    (isinstance(v, str) and v.strip()))\n"
    "    print(f'  {f:<15}: {filled}/{len(collected)}')\n"
    "\n"
    "print('\\nsummary는 Ch.7 §7.4에서 LLM이 자동 생성합니다.')"
))

cells.append(new_markdown_cell(
    "## 다음 단계\n"
    "\n"
    "- Ch.7 §7.1 : Gemini LLM 호출과 프롬프트 5가지 패턴\n"
    "- Ch.7 §7.4 : LLM이 본문을 읽고 summary 필드 자동 생성 → 본서 스키마의 마지막 필드 채움\n"
    "- Ch.8 §8.2 : 본 노트북의 search() 함수를 이용한 RAG 챗봇 검색 단계"
))

nb["cells"] = cells

with open("ch06_vector_search.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[OK] ch06_vector_search.ipynb ({len(cells)} cells)")
