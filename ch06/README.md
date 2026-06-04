# Chapter 6. 임베딩과 벡터 검색

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch06_vector_search.ipynb` | **§6.3~§6.5 실습 노트북** (Gemini Embedding + ChromaDB + 의미 검색) |
| `ch06_collected_embedded.jsonl` | Ch.3 스키마 AI 확장 6필드 중 5개 채워진 완성형 (summary만 비어 있음) |
| `build_ch06_files.py` | Ch.5 입력 → ch06 산출물 자동 생성 (API 키 불필요) |
| `build_notebook.py` | 노트북 빌더 |

`./chroma_db/` 폴더(컬렉션 SQLite 파일)는 본인 PC에서 노트북 실행 시 생성됩니다 — 저장소에는 커밋되지 않습니다.

## 🎯 학습 목표

- 임베딩과 코사인 유사도 개념을 이해한다
- Gemini Embedding(`gemini-embedding-001`, 768차원)으로 청크를 벡터로 변환한다
- ChromaDB PersistentClient에 컬렉션을 만들고 청크를 적재한다
- 사용자 질의에 의미적으로 가까운 청크 상위 N개를 찾는다
- 메타데이터로 검색 범위를 좁힌다
- Ch.3 스키마의 `embedding_flag` 필드를 True로 켠다

## 🚀 실습 시작하기 (본인 PC에서 직접)

이 실습은 본서 Ch.1에서 만든 본인 PC의 로컬 환경 + Gemini API 키가 필요하다.

### 1) Gemini API 키 발급 (책 §6.2.4 참조)

1. https://aistudio.google.com 에 Google 계정으로 로그인
2. 좌측 메뉴 'Get API key' → 'Create API key'
3. 발급된 키를 환경변수 `GEMINI_API_KEY`로 등록

### 2) 라이브러리 설치 + 노트북 실행

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
..\.venv\Scripts\Activate.ps1     # 가상환경 활성화 → (.venv) 표시 확인
pip install chromadb google-genai
$env:GEMINI_API_KEY = 'AIzaSy...실제 키...'
jupyter notebook ch06\ch06_vector_search.ipynb

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
source ../.venv/bin/activate
pip install chromadb google-genai
export GEMINI_API_KEY='AIzaSy...실제 키...'
jupyter notebook ch06/ch06_vector_search.ipynb
```

> Ch.3·Ch.5를 이미 거쳤다면 pandas는 설치돼 있다. chromadb·google-genai만 추가하면 된다.

## 📊 산출물

- `./chroma_db/` — 노트북 실행 후 생성. 다음 실행 때 그대로 재사용
- `ch06_collected_embedded.jsonl` — 스키마 AI 확장 6필드 중 5개 채워짐 (`summary`만 비어 있음, Ch.7 §7.4에서 채워짐)

## 🔗 본서 연결

- 사전: Ch.5 §5.5 청크 결과 (`../ch05/ch05_chunks.jsonl`)
- 이후: Ch.7 §7.4 summary 자동 생성 + Ch.8 §8.2 RAG 챗봇의 검색 단계

## ⚠️ 알려진 함정

- **API 키 누출**: 코드에 직접 적지 말 것. 환경변수만 사용. `.gitignore`에 `.env` 포함되어 있는지 확인 (책 §6.2.4 함정 박스)
- **임베딩 차원 불일치**: 한 컬렉션 안 임베딩은 모두 같은 차원이어야 함. 본서는 768로 고정
- **모델명 변경**: Google이 모델명을 갱신할 수 있음. 본서 작성 시점 기준 `gemini-embedding-001`(텍스트, 출력 768)
- **무료 한도**: Gemini API 무료 한도(분당 요청 수)가 있음. 본 실습 규모(수십 청크)는 한도 안에서 충분히 처리

## 📚 외부 참고

- Gemini Embedding 공식 문서: https://ai.google.dev/gemini-api/docs/embeddings
- Google AI Studio (API 키 발급): https://aistudio.google.com/
- ChromaDB 공식 문서: https://docs.trychroma.com/
- BGE-M3 (오프라인 대안): https://huggingface.co/BAAI/bge-m3
- Gemini API Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits
