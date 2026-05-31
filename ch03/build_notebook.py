# -*- coding: utf-8 -*-
r"""
ch03_metadata_schema.ipynb 생성기 — 본인 PC의 Jupyter / VS Code 노트북에서 실행

교재 Chapter 3 §3.4를 그대로 따른다.
"""
import io
import sys
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
    "# Chapter 2 §3.4 실습 — 메타데이터 스키마 만들기\n"
    "\n"
    "> 『AI 레디 데이터와 디지털 큐레이션』 Chapter 2의 §3.4 실습 노트북입니다.\n"
    "> 작성자: 김선태 · 저장소: https://github.com/Suntae-Kim2020/digital-curation\n"
    "\n"
    "## 학습 목표\n"
    "\n"
    "- Dublin Core 15요소 + AI 확장 6요소를 가진 메타데이터 스키마를 Pandas로 정의한다\n"
    "- CSV(utf-8-sig)로 저장해 Windows·Mac Excel에서 모두 한글이 정상 표시되도록 한다\n"
    "- 샘플 자료 5건을 입력해 JSON Lines로 보존한다\n"
    "- 검증 함수로 필수 필드 누락을 점검한다\n"
    "\n"
    "## 산출물\n"
    "\n"
    "1. `ch03_schema.csv` — 22개 필드 스키마\n"
    "2. `ch03_sample.jsonl` — 샘플 레코드 5건\n"
    "3. 검증 결과 '통과'\n"
    "\n"
    "## 선행 학습\n"
    "\n"
    "- Ch.2 §2.3 AI 레디 데이터 5조건\n"
    "- 본 챕터 §3.2 Dublin Core 15요소 / §3.3 AI 확장 6필드\n"
))

cells.append(new_markdown_cell(
    "## 0단계 · 환경 점검\n"
    "\n"
    "본 실습은 본서 Ch.1에서 만든 본인 PC의 로컬 가상환경(.venv)에서 진행한다.\n"
    "터미널 프롬프트에 (.venv) 표시가 보이면 활성화된 상태다.\n"
    "\n"
    "본 챕터에서 새로 쓰는 라이브러리는 pandas 하나다. 설치하지 않았다면 터미널에서 다음 한 줄로 설치한다.\n"
    "\n"
    "**🪟 Windows (PowerShell)** · **🍎 Mac (zsh/bash)** 모두: `pip install pandas`"
))

cells.append(new_code_cell(
    "import pandas as pd\n"
    "print('pandas', pd.__version__)"
))

cells.append(new_markdown_cell(
    "## 1단계 · 스키마 정의 (DC 15 + AI 6)\n"
    "\n"
    "본서 표준 스키마: Dublin Core 15요소 + ID 1개 + AI 확장 6필드 = 총 22 필드.\n"
    "\n"
    "각 필드는 `field` · `type` · `required` · `category` · `desc` 다섯 항목으로 명세한다."
))

cells.append(new_code_cell(
    "schema = pd.DataFrame([\n"
    "    # ── Dublin Core 베이스 ──\n"
    "    {'field':'id',          'type':'string',   'required':True,\n"
    "     'category':'ID', 'desc':'고유 식별자'},\n"
    "    {'field':'title',       'type':'string',   'required':True,\n"
    "     'category':'DC', 'desc':'자료 제목'},\n"
    "    {'field':'creator',     'type':'string',   'required':True,\n"
    "     'category':'DC', 'desc':'저자/제작자'},\n"
    "    {'field':'subject',     'type':'string[]', 'required':False,\n"
    "     'category':'DC', 'desc':'주제어 리스트'},\n"
    "    {'field':'description', 'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'원본 설명·초록'},\n"
    "    {'field':'publisher',   'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'발행자'},\n"
    "    {'field':'contributor', 'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'공동 저자/번역자'},\n"
    "    {'field':'date',        'type':'string',   'required':True,\n"
    "     'category':'DC', 'desc':'발행일 (YYYY-MM-DD)'},\n"
    "    {'field':'type',        'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'DCMI Type 어휘'},\n"
    "    {'field':'format',      'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'MIME 타입'},\n"
    "    {'field':'identifier',  'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'ISBN/DOI 등'},\n"
    "    {'field':'source',      'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'원본 출처'},\n"
    "    {'field':'language',    'type':'string',   'required':True,\n"
    "     'category':'DC', 'desc':'ISO 639-1 (ko/en)'},\n"
    "    {'field':'relation',    'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'관계 (isPartOf 등)'},\n"
    "    {'field':'coverage',    'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'공간·시간 범위'},\n"
    "    {'field':'rights',      'type':'string',   'required':False,\n"
    "     'category':'DC', 'desc':'권리 자유 표기'},\n"
    "    # ── AI 활용 확장 ──\n"
    "    {'field':'summary',     'type':'string',   'required':False,\n"
    "     'category':'AI', 'desc':'LLM 요약 (Ch.7 §7.4)'},\n"
    "    {'field':'keywords',    'type':'string[]', 'required':False,\n"
    "     'category':'AI', 'desc':'추출 키워드 (Ch.5 §5.3)'},\n"
    "    {'field':'source_url',  'type':'string',   'required':True,\n"
    "     'category':'AI', 'desc':'원본 URL'},\n"
    "    {'field':'license_code','type':'string',   'required':True,\n"
    "     'category':'AI', 'desc':'CC-BY-4.0 등 표준 코드'},\n"
    "    {'field':'chunk_ids',   'type':'string[]', 'required':False,\n"
    "     'category':'AI', 'desc':'청크 ID (Ch.5 §5.4)'},\n"
    "    {'field':'embedding_id','type':'string',   'required':False,\n"
    "     'category':'AI', 'desc':'벡터DB ID (Ch.6 §6.3)'},\n"
    "])\n"
    "schema.head()"
))

cells.append(new_markdown_cell(
    "### 💡 자주 만나는 함정 — CSV의 한글 인코딩\n"
    "\n"
    "Windows Excel은 BOM이 없는 UTF-8 CSV를 cp949로 잘못 해석해 한글을 깨뜨린다.\n"
    "`encoding='utf-8-sig'`로 저장하면 BOM이 포함되어 Windows·Mac 모두에서 한글이 정상 표시된다.\n"
    "**본서의 모든 CSV 저장은 이 기본값을 사용한다.**"
))

cells.append(new_code_cell(
    "schema.to_csv('ch03_schema.csv', index=False, encoding='utf-8-sig')\n"
    "print('Saved:', 'ch03_schema.csv', '·', len(schema), 'fields')"
))

cells.append(new_markdown_cell(
    "## 2단계 · 샘플 레코드 5건 입력\n"
    "\n"
    "샘플은 본서 자체(R001) + FAIR 원문 논문(R002) + 공공데이터 가이드(R003) + DCMI 명세(R004) + Schema.org(R005)로 구성한다.\n"
    "\n"
    "이 단계에서 `summary` · `keywords` · `chunk_ids` · `embedding_id`는 의도적으로 비워 둔다.\n"
    "Ch.5 §5.3에서 키워드를, Ch.5 §5.4에서 청크 ID를, Ch.6 §6.3에서 임베딩 ID를, Ch.7 §7.4에서 요약을 단계별로 채울 것이다."
))

cells.append(new_code_cell(
    "sample = pd.DataFrame([\n"
    "    {'id':'R001','title':'AI 레디 데이터와 디지털 큐레이션','creator':'김선태',\n"
    "     'subject':['디지털 큐레이션','메타데이터','RAG'],\n"
    "     'description':'생성형 AI 시대 데이터 활용 가이드. 3일/5일 교육 교재.',\n"
    "     'publisher':'','contributor':'','date':'2026-06','type':'Text',\n"
    "     'format':'application/pdf','identifier':'','source':'','language':'ko',\n"
    "     'relation':'','coverage':'','rights':'© 김선태',\n"
    "     'summary':'','keywords':[],\n"
    "     'source_url':'https://github.com/Suntae-Kim2020/digital-curation',\n"
    "     'license_code':'ALL-RIGHTS-RESERVED','chunk_ids':[],'embedding_id':''},\n"
    "\n"
    "    {'id':'R002','title':'The FAIR Guiding Principles for scientific data management',\n"
    "     'creator':'Wilkinson, M. D.; Dumontier, M.; et al.',\n"
    "     'subject':['FAIR','data management'],\n"
    "     'description':'FAIR 원칙을 처음 정립한 2016년 Scientific Data 논문.',\n"
    "     'publisher':'Nature Publishing','contributor':'','date':'2016-03-15',\n"
    "     'type':'Article','format':'text/html','identifier':'10.1038/sdata.2016.18',\n"
    "     'source':'Scientific Data 3, 160018','language':'en','relation':'','coverage':'',\n"
    "     'rights':'CC BY 4.0','summary':'','keywords':[],\n"
    "     'source_url':'https://doi.org/10.1038/sdata.2016.18',\n"
    "     'license_code':'CC-BY-4.0','chunk_ids':[],'embedding_id':''},\n"
    "\n"
    "    {'id':'R003','title':'공공데이터 개방·활용 가이드라인','creator':'행정안전부',\n"
    "     'subject':['공공데이터','개방','가이드라인'],\n"
    "     'description':'공공데이터 개방 표준, 라이선스, 품질관리 가이드.',\n"
    "     'publisher':'행정안전부','contributor':'','date':'2024-12-01',\n"
    "     'type':'Text','format':'application/pdf','identifier':'','source':'',\n"
    "     'language':'ko','relation':'','coverage':'대한민국','rights':'공공누리 제1유형',\n"
    "     'summary':'','keywords':[],\n"
    "     'source_url':'https://www.data.go.kr/',\n"
    "     'license_code':'KOGL-1','chunk_ids':[],'embedding_id':''},\n"
    "\n"
    "    {'id':'R004','title':'DCMI Metadata Terms (specification)',\n"
    "     'creator':'Dublin Core Metadata Initiative',\n"
    "     'subject':['Dublin Core','metadata'],\n"
    "     'description':'DCMI 메타데이터 용어 명세서.','publisher':'DCMI','contributor':'',\n"
    "     'date':'2020-01-20','type':'Specification','format':'text/html',\n"
    "     'identifier':'','source':'','language':'en','relation':'','coverage':'',\n"
    "     'rights':'CC BY 4.0','summary':'','keywords':[],\n"
    "     'source_url':'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/',\n"
    "     'license_code':'CC-BY-4.0','chunk_ids':[],'embedding_id':''},\n"
    "\n"
    "    {'id':'R005','title':'Schema.org','creator':'Schema.org Community Group',\n"
    "     'subject':['Schema.org','structured data','JSON-LD'],\n"
    "     'description':'웹용 구조화 데이터 어휘 표준.','publisher':'Schema.org Community',\n"
    "     'contributor':'','date':'2025-01-01','type':'Vocabulary','format':'text/html',\n"
    "     'identifier':'','source':'','language':'en','relation':'','coverage':'',\n"
    "     'rights':'CC BY-SA 3.0','summary':'','keywords':[],\n"
    "     'source_url':'https://schema.org/',\n"
    "     'license_code':'CC-BY-SA-3.0','chunk_ids':[],'embedding_id':''},\n"
    "])\n"
    "sample[['id','title','license_code','language']]"
))

cells.append(new_markdown_cell(
    "JSON Lines로 저장하면 리스트 필드(`subject`, `keywords`, `chunk_ids`)가 그대로 보존된다.\n"
    "한글이 그대로 보이도록 `force_ascii=False`를 지정한다."
))

cells.append(new_code_cell(
    "sample.to_json('ch03_sample.jsonl', orient='records', lines=True, force_ascii=False)\n"
    "print('Saved:', 'ch03_sample.jsonl', '·', len(sample), 'records')\n"
    "\n"
    "# 첫 줄 확인\n"
    "with open('ch03_sample.jsonl', 'r', encoding='utf-8') as f:\n"
    "    print('\\n[첫 줄 미리보기]')\n"
    "    print(f.readline()[:200], '...')"
))

cells.append(new_markdown_cell(
    "## 3단계 · 유효성 검증 함수\n"
    "\n"
    "스키마와 데이터를 비교해 (1) 필수 필드 자체가 빠졌는지 (2) 필수 필드 값이 비어 있는지 점검한다.\n"
    "\n"
    "더 엄밀한 검증(자료형 일치, 코드값 표준 일치)은 Ch.5 §5.1 데이터 정제에서 다룬다."
))

cells.append(new_code_cell(
    "def validate(records, schema):\n"
    "    '''필수 필드 누락 점검. 에러 목록 반환 (빈 리스트=통과)'''\n"
    "    errors = []\n"
    "    required = schema[schema['required']]['field'].tolist()\n"
    "\n"
    "    # (1) 필수 필드 자체 누락\n"
    "    missing = [f for f in required if f not in records.columns]\n"
    "    if missing:\n"
    "        errors.append(f'필수 필드 누락: {missing}')\n"
    "\n"
    "    # (2) 필수 필드 값 누락\n"
    "    for f in required:\n"
    "        if f in records.columns:\n"
    "            nulls = records[records[f].isna() | (records[f] == '')].index.tolist()\n"
    "            if nulls:\n"
    "                errors.append(f'{f}: 값 누락 행 {nulls}')\n"
    "    return errors\n"
    "\n"
    "result = validate(sample, schema)\n"
    "print('검증 결과:', '통과' if not result else result)"
))

cells.append(new_markdown_cell(
    "## 4단계 · 응용 — 누락된 자료 만들어 검증해 보기\n"
    "\n"
    "필수 필드 `source_url`이 빠진 자료를 추가해 검증이 어떻게 실패하는지 확인한다."
))

cells.append(new_code_cell(
    "bad = pd.concat([sample, pd.DataFrame([{\n"
    "    'id':'R999','title':'잘못된 자료','creator':'???',\n"
    "    'date':'2026-01','language':'ko',\n"
    "    'source_url':'',  # ← 필수인데 비어 있음\n"
    "    'license_code':'UNKNOWN',\n"
    "}])], ignore_index=True)\n"
    "\n"
    "print('검증 결과:', validate(bad, schema))"
))

cells.append(new_markdown_cell(
    "## 다음 단계\n"
    "\n"
    "- Ch.4 §4.1~§4.4 : 외부 API/웹에서 자료를 실제로 수집해 이 스키마에 매핑\n"
    "- Ch.5 §5.3 : 본문에서 `keywords` 자동 추출 (Kiwi 형태소 분석)\n"
    "- Ch.5 §5.4 : 본문 청킹 → `chunk_ids` 채우기\n"
    "- Ch.6 §6.3 : 벡터DB(ChromaDB) 적재 → `embedding_id` 채우기\n"
    "- Ch.7 §7.4 : LLM(Gemini)으로 `summary` 자동 생성\n"
    "\n"
    "이 노트북에서 비워둔 4개 필드가 후속 챕터에서 단계적으로 채워진다."
))

nb["cells"] = cells

with open("ch03_metadata_schema.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("[OK] ch03_metadata_schema.ipynb", f"({len(cells)} cells)")
