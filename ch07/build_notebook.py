# -*- coding: utf-8 -*-
r"""ch07_prompt_patterns.ipynb 생성기"""
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
    "# Chapter 7 §7.2~§7.4 실습 — Gemini API와 프롬프트 5패턴\n"
    "\n"
    "> 『AI 레디 데이터와 디지털 큐레이션』 Chapter 7의 §7.2부터 §7.4까지 실습 노트북.\n"
    "> 본인 PC의 가상환경(.venv)에서 실행. **GEMINI_API_KEY 필수**.\n"
    "\n"
    "## 학습 목표\n"
    "- Gemini API의 첫 호출과 응답 옵션(temperature·max_output_tokens)\n"
    "- 프롬프트 5가지 패턴(역할·예시·단계·JSON·제약)을 실제 코드로 확인\n"
    "- 본서 자료 5건에 LLM 요약 자동 생성 → Ch.3 스키마 마지막 필드(summary) 완성\n"
    "\n"
    "## 산출물\n"
    "- `ch07_collected_complete.jsonl` — 본서 스키마 AI 6확장 필드 모두 채워진 완성형\n"
    "\n"
    "## 선행\n"
    "- Ch.6 §6.2.4 GEMINI_API_KEY 발급·등록\n"
    "- Ch.6 산출물 `../ch06/ch06_collected_embedded.jsonl`"
))

cells.append(new_markdown_cell(
    "## 0단계 · 환경 점검\n"
    "\n"
    "본 챕터에서 새로 필요한 라이브러리:\n"
    "\n"
    "- **google-genai** — Gemini API 호출 공식 Python 패키지. Ch.6에서 이미 설치했다면 그대로 사용.\n"
    "\n"
    "**설치 — VS Code 통합 터미널에서 (Ch.6에서 이미 설치했으면 자동 skip)**\n"
    "\n"
    "1. `Ctrl + ` 단축키로 통합 터미널을 연다 (또는 메뉴 Terminal → New Terminal).\n"
    "2. 프롬프트 맨 앞에 `(.venv)` 표시가 보이는지 확인. 없다면 Ch.1 §1.7.4 절차로 .venv를 선택한다.\n"
    "3. 다음 한 줄을 입력 (이미 깔려 있으면 자동 skip):\n"
    "\n"
    "   ```\n"
    "   pip install google-genai\n"
    "   ```\n"
    "\n"
    "4. 설치 확인:\n"
    "\n"
    "   ```\n"
    "   python -c \"from google import genai; print('OK')\"\n"
    "   ```\n"
    "   → `OK`가 나오면 성공.\n"
    "\n"
    "**API 키**: 환경변수 `GEMINI_API_KEY`가 설정돼 있어야 한다 (책 §6.2.4 참조)."
))

cells.append(new_code_cell(
    "import os, json, time\n"
    "import pandas as pd\n"
    "from google import genai\n"
    "\n"
    "API_KEY = os.getenv('GEMINI_API_KEY')\n"
    "if not API_KEY:\n"
    "    raise RuntimeError(\n"
    "        'GEMINI_API_KEY가 설정되지 않았습니다. '\n"
    "        '책 §6.2.4 절차를 따라 등록 후 다시 실행하세요.')\n"
    "\n"
    "client = genai.Client()\n"
    "print('Gemini Client 준비 완료')"
))

cells.append(new_markdown_cell(
    "## 1단계 · §7.2.1 첫 호출\n"
    "\n"
    "가장 짧은 형태의 호출. `generate_content`에 모델명과 입력만 넣는다."
))

cells.append(new_code_cell(
    "response = client.models.generate_content(\n"
    "    model='gemini-2.5-flash',\n"
    "    contents='AI 레디 데이터가 무엇인지 두 문장으로 설명해 주세요.',\n"
    ")\n"
    "print(response.text)"
))

cells.append(new_markdown_cell(
    "## 2단계 · §7.2.2 응답 옵션 비교\n"
    "\n"
    "`temperature`로 응답 변동성을 조절한다. 같은 질문을 두 번 다른 온도로 호출해 결과를 비교."
))

cells.append(new_code_cell(
    "QUERY = 'RAG 챗봇의 핵심 가치를 한 문장으로 말해 주세요.'\n"
    "\n"
    "for temp in [0.0, 0.7]:\n"
    "    r = client.models.generate_content(\n"
    "        model='gemini-2.5-flash',\n"
    "        contents=QUERY,\n"
    "        config={'temperature': temp, 'max_output_tokens': 200},\n"
    "    )\n"
    "    print(f'\\n[temperature={temp}]')\n"
    "    print(' ', r.text.strip()[:200])"
))

cells.append(new_markdown_cell(
    "## 3단계 · §7.3 프롬프트 5패턴\n"
    "\n"
    "### 패턴 1 — 역할 부여 (Role)\n"
    "system_instruction으로 답변자 정체성을 고정."
))

cells.append(new_code_cell(
    "SYS = (\n"
    "    '당신은 대학도서관 사서입니다. '\n"
    "    '메타데이터·디지털 큐레이션·전거에 정통합니다. '\n"
    "    '답변은 한국어로 하고, 부정확한 추측은 '\n"
    "    '\"확실하지 않습니다\"라고 솔직히 말합니다.'\n"
    ")\n"
    "\n"
    "r = client.models.generate_content(\n"
    "    model='gemini-2.5-flash',\n"
    "    contents='RAG 챗봇이 출처를 표시해야 하는 이유를 설명해 주세요.',\n"
    "    config={'system_instruction': SYS, 'temperature': 0.3},\n"
    ")\n"
    "print(r.text)"
))

cells.append(new_markdown_cell(
    "### 패턴 2 — 예시 제공 (Few-shot)\n"
    "원하는 답 형식을 직접 보여 준다."
))

cells.append(new_code_cell(
    "prompt = '''다음 자료 제목을 보고 적절한 주제어 3개를 콤마로 구분해 답하세요.\n"
    "\n"
    "예시 1:\n"
    "  제목: AI 레디 데이터와 디지털 큐레이션\n"
    "  주제어: 디지털 큐레이션, 메타데이터, RAG\n"
    "\n"
    "예시 2:\n"
    "  제목: Retrieval-Augmented Generation for Knowledge-Intensive NLP\n"
    "  주제어: retrieval-augmented generation, NLP, language model\n"
    "\n"
    "이제 다음 제목의 주제어를 답하세요:\n"
    "  제목: 공공데이터 개방·활용 가이드라인\n"
    "  주제어:'''\n"
    "\n"
    "r = client.models.generate_content(\n"
    "    model='gemini-2.5-flash',\n"
    "    contents=prompt,\n"
    "    config={'temperature': 0.0},\n"
    ")\n"
    "print(r.text)"
))

cells.append(new_markdown_cell(
    "### 패턴 4 — 출력 형식 고정 (JSON)\n"
    "`response_mime_type='application/json'`으로 JSON 강제."
))

cells.append(new_code_cell(
    "prompt = '''다음 본문을 분석해 JSON으로 응답해 주세요.\n"
    "필드는 모두 채워 주세요.\n"
    "\n"
    "JSON 형식:\n"
    "  {\"summary\": \"200자 요약\",\n"
    "   \"keywords\": [\"단어1\", \"단어2\", \"단어3\"],\n"
    "   \"topic\": \"한 단어\"}\n"
    "\n"
    "본문:\n"
    "디지털 큐레이션은 도서관·기록관·연구지원자가 보유한 자료를\n"
    "생성형 AI가 활용할 수 있는 형태로 정비하는 활동이다.\n"
    "메타데이터 설계, 본문 청킹, 임베딩, RAG가 단계별로 결합된다.\n"
    "'''\n"
    "\n"
    "r = client.models.generate_content(\n"
    "    model='gemini-2.5-flash',\n"
    "    contents=prompt,\n"
    "    config={\n"
    "        'temperature': 0.2,\n"
    "        'response_mime_type': 'application/json',\n"
    "    },\n"
    ")\n"
    "\n"
    "result = json.loads(r.text)\n"
    "print('summary  :', result['summary'])\n"
    "print('keywords :', result['keywords'])\n"
    "print('topic    :', result['topic'])"
))

cells.append(new_markdown_cell(
    "## 4단계 · §7.4 본서 자료 5건에 summary 자동 생성\n"
    "\n"
    "Ch.6 결과(`../ch06/ch06_collected_embedded.jsonl`)의 모든 자료에 한국어 요약을 매긴다.\n"
    "Gemini 무료 한도(분당 약 12~15회)에 걸리지 않도록 호출 사이에 5초 휴식."
))

cells.append(new_code_cell(
    "SYS = (\n"
    "    '당신은 도서관 사서입니다. 주어진 자료의 본문을 읽고 '\n"
    "    '200~300자 분량의 한국어 요약을 만듭니다. '\n"
    "    '본문에 없는 사실은 만들어 내지 않고, 평서체로 작성합니다.'\n"
    ")\n"
    "\n"
    "def generate_summary(title, description):\n"
    "    prompt = (\n"
    "        '다음 자료를 요약해 주세요.\\n\\n'\n"
    "        f'제목: {title}\\n\\n'\n"
    "        f'본문:\\n{description}\\n\\n'\n"
    "        '아래 JSON으로 응답하세요:\\n'\n"
    "        '{\"summary\": \"200~300자 요약\"}'\n"
    "    )\n"
    "    r = client.models.generate_content(\n"
    "        model='gemini-2.5-flash',\n"
    "        contents=prompt,\n"
    "        config={\n"
    "            'system_instruction': SYS,\n"
    "            'temperature': 0.2,\n"
    "            'max_output_tokens': 600,\n"
    "            'response_mime_type': 'application/json',\n"
    "        },\n"
    "    )\n"
    "    try:\n"
    "        return json.loads(r.text)['summary']\n"
    "    except Exception as ex:\n"
    "        return f'[요약 생성 실패: {ex}]'\n"
    "\n"
    "\n"
    "collected = pd.read_json('../ch06/ch06_collected_embedded.jsonl', lines=True)\n"
    "\n"
    "for idx, row in collected.iterrows():\n"
    "    if row.get('summary'):\n"
    "        continue\n"
    "    print(f\"[{idx+1}/{len(collected)}] {row['id']} 생성 중…\")\n"
    "    s = generate_summary(row['title'], row.get('description', ''))\n"
    "    collected.at[idx, 'summary'] = s\n"
    "    print(f'  → {s[:80]}…')\n"
    "    time.sleep(5)  # rate limit 방어\n"
    "\n"
    "collected.to_json('ch07_collected_complete.jsonl',\n"
    "                  orient='records', lines=True, force_ascii=False)\n"
    "print(f'\\n저장: ch07_collected_complete.jsonl ({len(collected)} 레코드)')"
))

cells.append(new_markdown_cell(
    "## 5단계 · 스키마 완성 검증\n"
    "\n"
    "Ch.3 §3.3의 AI 확장 6필드가 모두 채워졌는지 마지막 확인."
))

cells.append(new_code_cell(
    "complete = pd.read_json('ch07_collected_complete.jsonl', lines=True)\n"
    "\n"
    "ai_fields = ['summary', 'keywords', 'chunk_ids',\n"
    "             'embedding_flag', 'source_url', 'license_code']\n"
    "for f in ai_fields:\n"
    "    filled = sum(1 for v in complete[f]\n"
    "                 if (isinstance(v, list) and v) or\n"
    "                    (isinstance(v, str) and v.strip()))\n"
    "    bar = '█' * filled + '░' * (len(complete) - filled)\n"
    "    print(f'  {f:<15}: {filled}/{len(complete)}  {bar}')\n"
    "\n"
    "all_full = all(\n"
    "    sum(1 for v in complete[f] if (isinstance(v, list) and v) or (isinstance(v, str) and v.strip())) == len(complete)\n"
    "    for f in ai_fields\n"
    ")\n"
    "print()\n"
    "print('✅ 본서 스키마 완성' if all_full else '⚠️ 일부 필드 비어 있음')"
))

cells.append(new_markdown_cell(
    "## 다음 단계\n"
    "\n"
    "- Ch.8 §8.1 : RAG 4단계 파이프라인 설계 (질의 → 검색 → 증강 → 생성)\n"
    "- Ch.8 §8.2 : Ch.6의 의미 검색 + Ch.7의 LLM 호출 결합 → 작동하는 챗봇\n"
    "- Ch.8 §8.3 : 답변 출처 표시(citation) 구현"
))

nb["cells"] = cells

with open("ch07_prompt_patterns.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"[OK] ch07_prompt_patterns.ipynb ({len(cells)} cells)")
