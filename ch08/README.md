# Chapter 8. RAG 챗봇 구축 ⭐

본서 본격 학습의 클라이맥스 — Ch.6 의미 검색 + Ch.7 LLM 호출을 결합해 **작동하는 RAG 챗봇**을 만든다.

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch08_rag.py` | **재사용 가능한 RAG 통합 모듈** — `from ch08_rag import ask_rag` |
| `ch08_rag_chatbot.ipynb` | **§8.2~§8.5 실습 노트북** (17셀, 다섯 시연 질의 + 직접 질문) |
| `ch08_demo_queries.json` | 시연 질의 5건 (마지막은 환각 방어 시험용) |
| `build_ch08_files.py` | 사전 조건 점검 + 시연 질의 목록 |
| `build_notebook.py` | 노트북 빌더 |

## 🎯 학습 목표

- RAG 4단계(Query → Retrieve → Augment → Generate)를 코드로 통합
- Ch.6 의미 검색과 Ch.7 LLM 호출을 한 파이프라인으로 연결
- 답변에 출처(citation) 자동 표시
- 환각·관련성·완전성 세 관점으로 답변 품질 점검
- 자료에 없는 질문에 챗봇이 안전하게 답하는지 확인

## 🚀 실습 시작하기 (본인 PC에서 직접)

사전 조건: Ch.6 ChromaDB 컬렉션 적재 + Ch.7 스키마 완성 + GEMINI_API_KEY 등록.

### 옵션 A — 노트북 (권장, 처음 학습자)

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
..\.venv\Scripts\Activate.ps1
$env:GEMINI_API_KEY = 'AIzaSy...'           # Ch.6에서 이미 설정했다면 생략
jupyter notebook ch08\ch08_rag_chatbot.ipynb

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
source ../.venv/bin/activate
export GEMINI_API_KEY='AIzaSy...'
jupyter notebook ch08/ch08_rag_chatbot.ipynb
```

### 옵션 B — 모듈 직접 실행 (다섯 시연 질의 자동)

```
cd ch08
python ch08_rag.py
```

### 옵션 C — Python 셸에서 임포트해 자유 질문

```python
from ch08_rag import ask_rag, print_rag_result
r = ask_rag("RAG가 환각을 줄이는 원리는?")
print_rag_result(r)
```

## 📊 핵심 API

```python
ask_rag(query, k=3, where=None) -> dict
    # 4단계 통합 — 사용자 질의에 출처와 함께 답변
    # 반환: {'query', 'answer', 'sources', 'distances'}

print_rag_result(result)
    # 답변 + 출처 + 거리값을 보기 좋게 출력

ask_rag_verbose(query, k=3)
    # 답변 + 검색된 원본 청크까지 한 화면에 표시
```

## 🔗 본서 연결

- 사전:
  - Ch.6 §6.3 ChromaDB 컬렉션 `ai_ready_chunks` 적재
  - Ch.7 §7.4 스키마 완성 (../ch07/ch07_collected_complete.jsonl)
  - Ch.6 §6.2.4 GEMINI_API_KEY 등록
- 이후:
  - Ch.9 §9.1~§9.3 자기 기관 자료로 RAG 챗봇 확장 (미니 프로젝트)
  - Ch.10 §10.1~§10.4 저작권·운영·거버넌스

## ⚠️ 알려진 함정

- **컬렉션 없음 에러**: `chromadb`가 컬렉션을 못 찾으면 Ch.6 노트북부터 먼저 실행
- **빈 검색 결과**: 질의가 자료와 너무 동떨어지면 `ask_rag`가 안전 기본 답변 반환 ("관련 내용이 검색되지 않습니다")
- **환각**: 그럴듯한 거짓이 섞일 수 있음 → **양자 컴퓨팅 시험 질의**로 항상 확인 (책 §8.5)
- **429 Too Many Requests**: 시연 질의 5건 연속 호출 시 분당 한도 위험 → `ch08_rag.py`의 호출은 단발이므로 보통 안전. 더 많은 호출 필요시 `time.sleep(5)` 추가
- **출처 표시 누락**: LLM이 가끔 [출처: ...]을 빠뜨림 → 프롬프트의 규칙 강조 또는 후처리로 검증

## 📚 외부 참고

- RAGAS (RAG 자동 평가): https://docs.ragas.io/
- ChromaDB query API: https://docs.trychroma.com/
- Gemini API generate_content: https://ai.google.dev/gemini-api/docs
- RAG 최초 논문 (Lewis et al. 2020): https://doi.org/10.48550/arXiv.2005.11401
