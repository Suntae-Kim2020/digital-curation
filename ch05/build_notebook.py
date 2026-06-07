# -*- coding: utf-8 -*-
r"""ch05_text_preprocessing.ipynb 생성기"""
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
    "# Chapter 5 §5.2~§5.5 실습 — 텍스트 전처리와 청킹\n"
    "\n"
    "> 『AI 레디 데이터와 디지털 큐레이션』 Chapter 5의 §5.2부터 §5.5까지 실습 노트북.\n"
    "> 본인 PC의 가상환경(.venv)에서 실행한다.\n"
    "\n"
    "## 학습 목표\n"
    "- PyMuPDF로 PDF에서 본문 텍스트를 추출한다\n"
    "- Kiwi로 한국어 형태소 분석을 수행하고 명사 키워드를 추출한다\n"
    "- 세 가지 청킹 전략(fixed·sentence·sentence_overlap)을 비교한다\n"
    "- Ch.4 §4.4의 ch04_collected.jsonl을 입력으로 받아 ch05_chunks.jsonl과 ch05_collected_filled.jsonl을 생성한다\n"
    "\n"
    "## 산출물\n"
    "1. `ch05_chunks.jsonl` — 본문이 청크 단위로 잘려 저장된 파일\n"
    "2. `ch05_collected_filled.jsonl` — Ch.3 스키마의 keywords·chunk_ids 두 필드가 채워진 완성형\n"
    "\n"
    "## 선행\n"
    "- Ch.3 §3.3 본서 표준 스키마\n"
    "- Ch.4 §4.4 수집 결과 (`../ch04/ch04_collected.jsonl`)"
))

cells.append(new_markdown_cell(
    "## 0단계 · 환경 점검\n"
    "\n"
    "본 챕터에서 새로 사용할 라이브러리 두 개:\n"
    "\n"
    "- **pymupdf** — PDF 본문 텍스트 추출. 빠르고 한글 안정적, 페이지 단위 처리 가능.\n"
    "- **kiwipiepy** — 한국어 형태소 분석기 Kiwi의 Python 패키지. 자바 의존이 없어 Windows·Mac 모두 pip 한 줄로 설치.\n"
    "\n"
    "**설치 — VS Code 통합 터미널에서**\n"
    "\n"
    "1. **단축키 Ctrl + 백틱(키보드 숫자 1 왼쪽 ~ 키)**을 누른다 — 또는 메뉴 Terminal → New Terminal.\n"
    "2. 프롬프트 맨 앞에 `(.venv)` 표시가 보이는지 확인. 없다면 Ch.1 §1.7.4 절차로 .venv를 선택한다.\n"
    "3. 다음 한 줄을 입력:\n"
    "\n"
    "   ```\n"
    "   pip install pymupdf kiwipiepy\n"
    "   ```\n"
    "\n"
    "4. 설치 확인:\n"
    "\n"
    "   ```\n"
    "   python -c \"import fitz, kiwipiepy; print('OK')\"\n"
    "   ```\n"
    "   → `OK`가 나오면 성공. `.venv` 안에만 설치되어 시스템 Python에는 영향 없음.\n"
    "   (pymupdf의 import 이름은 `fitz` — 역사적 이유로 라이브러리명과 모듈명이 다름)"
))

cells.append(new_code_cell(
    "import re, json\n"
    "from collections import Counter\n"
    "import pandas as pd\n"
    "\n"
    "# Kiwi (한국어 형태소 분석)\n"
    "from kiwipiepy import Kiwi\n"
    "kiwi = Kiwi()\n"
    "print('kiwipiepy', kiwi.version, '준비 완료')\n"
    "\n"
    "# PyMuPDF (PDF 처리)\n"
    "try:\n"
    "    import fitz\n"
    "    print('pymupdf', fitz.__doc__.splitlines()[0])\n"
    "except ImportError:\n"
    "    print('pymupdf 미설치 — pip install pymupdf 후 다시 실행')"
))

cells.append(new_markdown_cell(
    "## 1단계 · §5.2 PyMuPDF로 PDF 텍스트 추출\n"
    "\n"
    "본인 PC에 있는 PDF 파일 경로를 `PDF_PATH`에 넣고 실행한다. 한국어 PDF·영문 PDF 모두 작동한다.\n"
    "\n"
    "PDF가 손에 없으면 이 셀은 건너뛰어도 된다 (이후 §5.3·§5.4는 텍스트만 있으면 진행 가능)."
))

cells.append(new_code_cell(
    "def extract_pdf_text(pdf_path):\n"
    "    '''PDF 모든 페이지의 텍스트를 [page N] 표시와 함께 이어 붙여 반환'''\n"
    "    doc = fitz.open(pdf_path)\n"
    "    pages = []\n"
    "    for i, page in enumerate(doc, start=1):\n"
    "        text = page.get_text()\n"
    "        pages.append(f'[page {i}]\\n{text}')\n"
    "    doc.close()\n"
    "    return '\\n\\n'.join(pages)\n"
    "\n"
    "\n"
    "def clean_text(text):\n"
    "    '''PDF 추출 결과 정제'''\n"
    "    text = re.sub(r'[ \\t]+', ' ', text)\n"
    "    text = re.sub(r'\\n{3,}', '\\n\\n', text)\n"
    "    text = re.sub(r'-\\n([a-zA-Z])', r'\\1', text)\n"
    "    text = re.sub(r'(?<=[a-zA-Z,])\\n(?=[a-zA-Z])', ' ', text)\n"
    "    return text.strip()\n"
    "\n"
    "\n"
    "# 본인 PDF로 시험해 보세요 (없으면 이 셀 건너뛰기)\n"
    "# PDF_PATH = 'sample.pdf'\n"
    "# raw = extract_pdf_text(PDF_PATH)\n"
    "# cleaned = clean_text(raw)\n"
    "# print(cleaned[:500])"
))

cells.append(new_markdown_cell(
    "## 2단계 · §5.3 Kiwi로 한국어 키워드 추출\n"
    "\n"
    "Kiwi는 본문을 형태소(의미를 가진 최소 단위)로 분해한 다음 각 형태소에 품사 태그를 붙여 준다.\n"
    "키워드 후보로는 일반 명사(NNG)·고유 명사(NNP)만 쓰는 게 보편적이다."
))

cells.append(new_code_cell(
    "def extract_keywords_ko(text, top_k=10):\n"
    "    '''한국어 본문에서 명사 키워드 top_k개를 빈도순으로 반환'''\n"
    "    tokens = kiwi.tokenize(text)\n"
    "    NOUN_TAGS = {'NNG', 'NNP'}\n"
    "    nouns = [t.form for t in tokens\n"
    "             if t.tag in NOUN_TAGS and len(t.form) >= 2]\n"
    "    return [w for w, _ in Counter(nouns).most_common(top_k)]\n"
    "\n"
    "\n"
    "sample_ko = '''디지털 큐레이션은 도서관·기록관이 보유한 데이터를\n"
    "생성형 AI가 활용할 수 있는 형태로 정비하는 활동이다.\n"
    "메타데이터·임베딩·RAG 같은 기술이 활용된다. 본 챕터에서는\n"
    "텍스트 전처리와 청킹을 다룬다. 청킹은 본문을 적당한 크기의\n"
    "토막으로 잘라 두는 작업이다.'''\n"
    "\n"
    "print(extract_keywords_ko(sample_ko, top_k=10))"
))

cells.append(new_markdown_cell(
    "## 3단계 · §5.4 청킹 — 세 가지 전략\n"
    "\n"
    "본서가 권장하는 sentence_overlap을 포함해 세 가지를 모두 정의하고 비교한다."
))

cells.append(new_code_cell(
    "def chunk_fixed(text, size=800):\n"
    "    '''고정 길이 — 가장 단순. 문장 중간에서 잘릴 수 있음'''\n"
    "    return [text[i:i+size] for i in range(0, len(text), size)]\n"
    "\n"
    "\n"
    "def chunk_sentence(text, max_chars=800):\n"
    "    '''문장 단위 — 의미가 깨지지 않음'''\n"
    "    sents = [s.text for s in kiwi.split_into_sents(text)]\n"
    "    chunks, buf = [], ''\n"
    "    for s in sents:\n"
    "        if len(buf) + len(s) > max_chars and buf:\n"
    "            chunks.append(buf)\n"
    "            buf = s\n"
    "        else:\n"
    "            buf = (buf + ' ' + s).strip() if buf else s\n"
    "    if buf:\n"
    "        chunks.append(buf)\n"
    "    return chunks\n"
    "\n"
    "\n"
    "def chunk_sentence_overlap(text, max_chars=800, overlap_sents=1):\n"
    "    '''문장 + 오버랩 — 본서 권장. 문맥 연결 보존'''\n"
    "    sents = [s.text for s in kiwi.split_into_sents(text)]\n"
    "    chunks, buf_sents, buf = [], [], ''\n"
    "    for s in sents:\n"
    "        if len(buf) + len(s) > max_chars and buf:\n"
    "            chunks.append(buf)\n"
    "            overlap = buf_sents[-overlap_sents:] if overlap_sents else []\n"
    "            buf_sents = overlap + [s]\n"
    "            buf = ' '.join(buf_sents)\n"
    "        else:\n"
    "            buf_sents.append(s)\n"
    "            buf = (buf + ' ' + s).strip() if buf else s\n"
    "    if buf:\n"
    "        chunks.append(buf)\n"
    "    return chunks"
))

cells.append(new_markdown_cell(
    "긴 본문에 세 전략을 적용해 결과를 비교한다."
))

cells.append(new_code_cell(
    "long_text = sample_ko * 8  # 시연용으로 8배 늘림\n"
    "\n"
    "for name, fn in [\n"
    "    ('fixed_800',          lambda t: chunk_fixed(t, 800)),\n"
    "    ('sentence',           lambda t: chunk_sentence(t, 800)),\n"
    "    ('sentence_overlap_1', lambda t: chunk_sentence_overlap(t, 800, 1)),\n"
    "]:\n"
    "    chunks = fn(long_text)\n"
    "    avg = sum(len(c) for c in chunks) // max(len(chunks), 1)\n"
    "    print(f'{name:<22} 청크 {len(chunks)}개  평균 {avg}자')\n"
    "    print(f'  첫 청크 앞 80자: {chunks[0][:80]}')\n"
    "    print()"
))

cells.append(new_markdown_cell(
    "## 4단계 · §5.5 통합 산출물 — ch04 → ch05 파이프라인\n"
    "\n"
    "Ch.4의 수집 결과를 입력으로 받아 본 챕터 두 산출물(ch05_chunks.jsonl, ch05_collected_filled.jsonl)을 만든다."
))

cells.append(new_code_cell(
    "import os\n"
    "\n"
    "INPUT = os.path.join('..', 'ch04', 'ch04_collected.jsonl')\n"
    "assert os.path.exists(INPUT), f'{INPUT}을 먼저 만들어 두세요 (Ch.4 실습).'\n"
    "\n"
    "collected = pd.read_json(INPUT, lines=True)\n"
    "all_chunks = []\n"
    "\n"
    "for idx, row in collected.iterrows():\n"
    "    doc_id = row['id']\n"
    "    text = row.get('description', '') or ''\n"
    "    if not text:\n"
    "        continue\n"
    "    # 키워드 (한국어 자료면 Kiwi 결과가 정확; 영문 자료면 NNG/NNP가 거의 안 나옴)\n"
    "    collected.at[idx, 'keywords'] = extract_keywords_ko(text, top_k=10)\n"
    "    # 청크\n"
    "    chunks = chunk_sentence_overlap(text, max_chars=800, overlap_sents=1)\n"
    "    chunk_ids = []\n"
    "    for i, ctext in enumerate(chunks):\n"
    "        cid = f'{doc_id}-c{i+1:03d}'\n"
    "        chunk_ids.append(cid)\n"
    "        all_chunks.append({\n"
    "            'chunk_id':    cid,\n"
    "            'doc_id':      doc_id,\n"
    "            'chunk_index': i,\n"
    "            'method':      'sentence_overlap_1',\n"
    "            'char_count':  len(ctext),\n"
    "            'text':        ctext,\n"
    "        })\n"
    "    collected.at[idx, 'chunk_ids'] = chunk_ids\n"
    "\n"
    "# 저장\n"
    "collected.to_json('ch05_collected_filled.jsonl',\n"
    "                  orient='records', lines=True, force_ascii=False)\n"
    "pd.DataFrame(all_chunks).to_json('ch05_chunks.jsonl',\n"
    "                                  orient='records', lines=True, force_ascii=False)\n"
    "\n"
    "print(f'저장: ch05_collected_filled.jsonl ({len(collected)} 레코드)')\n"
    "print(f'저장: ch05_chunks.jsonl ({len(all_chunks)} 청크)')\n"
    "print()\n"
    "print('자료별 청크 수:')\n"
    "print(pd.DataFrame(all_chunks).groupby('doc_id').size().to_string())"
))

cells.append(new_markdown_cell(
    "## 다음 단계\n"
    "\n"
    "- Ch.6 §6.1 : 임베딩 개념과 의미 공간 시각화\n"
    "- Ch.6 §6.2 : Gemini text-embedding-004 호출\n"
    "- Ch.6 §6.3 : ch05_chunks.jsonl을 ChromaDB에 적재 → 의미 검색 가능\n"
    "- Ch.6 §6.5 : embedding_flag 켜고 의미 기반 자료 조회"
))

nb["cells"] = cells

with open("ch05_text_preprocessing.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[OK] ch05_text_preprocessing.ipynb ({len(cells)} cells)")
