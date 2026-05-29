# -*- coding: utf-8 -*-
r"""ch03_data_collection.ipynb 생성기"""
import io, sys
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

nb = new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12"},
    "colab": {"provenance": [], "toc_visible": True},
}

cells = []

cells.append(new_markdown_cell(
    "# Chapter 3 §3.2~§3.4 실습 — 데이터 수집과 스키마 매핑\n"
    "\n"
    "> 『AI 레디 데이터와 디지털 큐레이션』 Chapter 3의 실습 노트북입니다.\n"
    "> 저장소: https://github.com/Suntae-Kim2020/digital-curation\n"
    "\n"
    "## 학습 목표\n"
    "- arXiv API에서 RAG 관련 논문 5건을 수집한다\n"
    "- robots.txt를 점검하고 매너 있게 호출한다\n"
    "- 수집 결과를 Ch.2 §2.4 스키마에 매핑해 JSON Lines로 저장한다\n"
    "- Ch.2 §2.4.4 validate 함수로 필수 필드 누락을 점검한다\n"
    "\n"
    "## 산출물\n"
    "1. `ch03_collected.jsonl` — Ch.2 스키마에 매핑된 수집 결과\n"
    "\n"
    "## 선행 학습\n"
    "- Ch.2 §2.2 Dublin Core 15요소 / §2.3 AI 확장 6필드 / §2.4 스키마"
))

cells.append(new_markdown_cell(
    "## 0단계 · 환경\n"
    "\n"
    "Colab은 requests·beautifulsoup4가 이미 설치되어 있다. 로컬에서는 다음을 실행한다.\n"
    "\n"
    "**🪟 Windows (PowerShell)** : `python -m pip install requests beautifulsoup4 lxml`\n"
    "\n"
    "**🍎 Mac (zsh/bash)**      : `python3 -m pip install requests beautifulsoup4 lxml`"
))

cells.append(new_code_cell(
    "# 로컬 환경에서만 필요\n"
    "# !pip install -q requests beautifulsoup4 lxml\n"
    "\n"
    "import requests, time, json\n"
    "import pandas as pd\n"
    "from xml.etree import ElementTree as ET\n"
    "from bs4 import BeautifulSoup\n"
    "from urllib.robotparser import RobotFileParser\n"
    "\n"
    "AGENT = 'AI-Curation-Course/1.0 (your-email@example.com)'\n"
    "print('OK · requests', requests.__version__)"
))

cells.append(new_markdown_cell(
    "## 1단계 · arXiv API 호출 (인증키 불필요)\n"
    "\n"
    "arXiv API는 키 없이 즉시 호출할 수 있고, RAG 관련 논문이 풍부해 학습용으로 최적이다.\n"
    "응답은 Atom XML이다."
))

cells.append(new_code_cell(
    "BASE = 'https://export.arxiv.org/api/query'\n"
    "params = {\n"
    "    'search_query': 'all:retrieval augmented generation',\n"
    "    'start': 0,\n"
    "    'max_results': 5,\n"
    "}\n"
    "r = requests.get(BASE, params=params, headers={'User-Agent': AGENT}, timeout=15)\n"
    "r.raise_for_status()\n"
    "\n"
    "ns = {'atom': 'http://www.w3.org/2005/Atom'}\n"
    "root = ET.fromstring(r.content)\n"
    "entries = root.findall('atom:entry', ns)\n"
    "print(f'받은 entry: {len(entries)}건')\n"
    "for e in entries:\n"
    "    title = e.find('atom:title', ns).text.strip()\n"
    "    arxiv_id = e.find('atom:id', ns).text.split('/')[-1]\n"
    "    print(f'  {arxiv_id} | {title[:60]}')\n"
    "\n"
    "# arXiv 매너 — 다음 호출 전 3초\n"
    "time.sleep(3)"
))

cells.append(new_markdown_cell(
    "## 2단계 · Ch.2 §2.4 스키마로 매핑\n"
    "\n"
    "출처마다 필드 이름이 다르므로, 본서 표준 스키마(DC 15 + AI 6)에 맞춰 통일한다.\n"
    "이 단계에서 의미 차원 4필드(summary, keywords, chunk_ids, embedding_id)는 비워 두고\n"
    "후속 챕터에서 단계적으로 채운다."
))

cells.append(new_code_cell(
    "def map_arxiv_entry(e, ns):\n"
    "    arxiv_id = e.find('atom:id', ns).text.split('/')[-1]\n"
    "    authors = [a.find('atom:name', ns).text\n"
    "               for a in e.findall('atom:author', ns)]\n"
    "    return {\n"
    "        'id':           f'arxiv:{arxiv_id}',\n"
    "        'title':        e.find('atom:title', ns).text.strip(),\n"
    "        'creator':      '; '.join(authors),\n"
    "        'subject':      [],\n"
    "        'description':  e.find('atom:summary', ns).text.strip(),\n"
    "        'publisher':    'arXiv',\n"
    "        'contributor':  '',\n"
    "        'date':         e.find('atom:published', ns).text[:10],\n"
    "        'type':         'Article',\n"
    "        'format':       'application/pdf',\n"
    "        'identifier':   arxiv_id,\n"
    "        'source':       '',\n"
    "        'language':     'en',\n"
    "        'relation':     '',\n"
    "        'coverage':     '',\n"
    "        'rights':       'arXiv non-exclusive license',\n"
    "        'summary':      '',          # Ch.6 §6.4\n"
    "        'keywords':     [],          # Ch.4 §4.3\n"
    "        'source_url':   e.find('atom:id', ns).text,\n"
    "        'license_code': 'ARXIV-NONEXCLUSIVE',\n"
    "        'chunk_ids':    [],          # Ch.4 §4.4\n"
    "        'embedding_id': '',          # Ch.5 §5.3\n"
    "    }\n"
    "\n"
    "records = [map_arxiv_entry(e, ns) for e in entries]\n"
    "df = pd.DataFrame(records)\n"
    "df[['id','date','language','license_code']]"
))

cells.append(new_markdown_cell(
    "## 3단계 · JSON Lines로 저장\n"
    "\n"
    "리스트 필드(`subject`, `keywords`, `chunk_ids`)를 보존하기 위해 `.jsonl` 권장.\n"
    "한글은 `force_ascii=False`로 그대로 둔다."
))

cells.append(new_code_cell(
    "df.to_json('ch03_collected.jsonl',\n"
    "          orient='records', lines=True, force_ascii=False)\n"
    "print('Saved: ch03_collected.jsonl', '·', len(df), 'records')\n"
    "\n"
    "with open('ch03_collected.jsonl', 'r', encoding='utf-8') as f:\n"
    "    print('\\n[첫 줄 미리보기]')\n"
    "    print(f.readline()[:200], '…')"
))

cells.append(new_markdown_cell(
    "## 4단계 · robots.txt 점검 (웹 크롤링용)\n"
    "\n"
    "API가 아닌 일반 페이지를 수집할 때는 매번 robots.txt를 점검한다.\n"
    "법적 효력은 없지만 매너이자 차단 방지책이다."
))

cells.append(new_code_cell(
    "def can_collect(url, agent=AGENT):\n"
    "    rp = RobotFileParser()\n"
    "    # 도메인 루트의 robots.txt 위치 계산\n"
    "    parts = url.split('/')\n"
    "    rp.set_url(f'{parts[0]}//{parts[2]}/robots.txt')\n"
    "    rp.read()\n"
    "    allowed = rp.can_fetch(agent, url)\n"
    "    delay   = rp.crawl_delay(agent) or 1\n"
    "    return allowed, delay\n"
    "\n"
    "for u in [\n"
    "    'https://www.dublincore.org/specifications/',\n"
    "    'https://schema.org/Book',\n"
    "]:\n"
    "    allowed, delay = can_collect(u)\n"
    "    flag = '허용' if allowed else '금지'\n"
    "    print(f'{flag} · 간격 {delay}초 · {u}')"
))

cells.append(new_markdown_cell(
    "## 5단계 · 정적 페이지에서 메타 추출 (예시)\n"
    "\n"
    "robots.txt 통과 → HTML 수집 → BeautifulSoup으로 메타 추출의 표준 패턴."
))

cells.append(new_code_cell(
    "def fetch_meta(url, agent=AGENT):\n"
    "    allowed, delay = can_collect(url, agent)\n"
    "    if not allowed:\n"
    "        return None\n"
    "    r = requests.get(url, headers={'User-Agent': agent}, timeout=10)\n"
    "    r.raise_for_status()\n"
    "    s = BeautifulSoup(r.content, 'html.parser')\n"
    "    title = s.title.text.strip() if s.title else ''\n"
    "    desc = ''\n"
    "    md = s.find('meta', attrs={'name': 'description'})\n"
    "    if md and md.get('content'):\n"
    "        desc = md['content'].strip()\n"
    "    time.sleep(delay)\n"
    "    return {'title': title, 'description': desc, 'source_url': url}\n"
    "\n"
    "fetch_meta('https://www.dublincore.org/')"
))

cells.append(new_markdown_cell(
    "## 6단계 · Ch.2 §2.4.4 검증 함수 재사용\n"
    "\n"
    "수집 결과의 필수 필드 누락 여부를 점검한다."
))

cells.append(new_code_cell(
    "def validate(records, schema):\n"
    "    errors = []\n"
    "    required = schema[schema['required']]['field'].tolist()\n"
    "    for f in required:\n"
    "        if f not in records.columns:\n"
    "            errors.append(f'필수 필드 누락: {f}')\n"
    "        else:\n"
    "            nulls = records[records[f].isna() | (records[f] == '')].index.tolist()\n"
    "            if nulls:\n"
    "                errors.append(f'{f}: 값 누락 행 {nulls}')\n"
    "    return errors\n"
    "\n"
    "# Ch.2 스키마 불러오기 (저장소에 동봉)\n"
    "import urllib.request\n"
    "SCHEMA_URL = ('https://raw.githubusercontent.com/Suntae-Kim2020/'\n"
    "              'digital-curation/main/ch02/ch02_schema.csv')\n"
    "schema = pd.read_csv(SCHEMA_URL, encoding='utf-8-sig')\n"
    "errors = validate(df, schema)\n"
    "print('검증:', '통과' if not errors else errors)"
))

cells.append(new_markdown_cell(
    "## 다음 단계\n"
    "\n"
    "- Ch.4 §4.1 : 수집한 description 본문을 정제\n"
    "- Ch.4 §4.3 : 본문에서 keywords 자동 추출 (Kiwi)\n"
    "- Ch.4 §4.4 : 청킹 → chunk_ids 채우기\n"
    "- Ch.5 §5.3 : 벡터DB 적재 → embedding_id 채우기\n"
    "- Ch.6 §6.4 : LLM(Gemini)으로 summary 자동 생성"
))

nb["cells"] = cells

with open("ch03_data_collection.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[OK] ch03_data_collection.ipynb ({len(cells)} cells)")
