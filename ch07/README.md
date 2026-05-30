# Chapter 7. Gemini API와 프롬프트

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch07_prompt_patterns.ipynb` | **§7.2~§7.4 실습 노트북** (API 호출·5패턴·summary 자동 생성) |
| `ch07_collected_complete.jsonl` | **본서 스키마 22필드 모두 채워진 완성형** (AI 6확장 100%) |
| `build_ch07_files.py` | Ch.6 → Ch.7 파이프라인. **LIVE/DEMO 두 모드 자동 전환** |
| `build_notebook.py` | 노트북 빌더 |

## 🎯 학습 목표

- LLM(대규모 언어 모델)의 토큰 단위 동작과 환각 메커니즘을 이해한다
- Gemini API의 첫 호출 + `temperature`·`max_output_tokens`·`system_instruction` 옵션을 다룬다
- 프롬프트 5가지 패턴(역할·예시·단계·JSON·제약)을 실제 코드로 적용한다
- 본서 자료 5건에 LLM 요약을 자동 생성해 **스키마의 마지막 빈 필드(summary)를 완성**한다

## 🚀 실습 시작하기 (본인 PC에서 직접)

API 키 발급은 책 §6.2.4 또는 Ch.6 README 참조.

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
..\.venv\Scripts\Activate.ps1
$env:GEMINI_API_KEY = 'AIzaSy...'           # Ch.6에서 이미 설정했다면 생략
pip install google-genai                    # Ch.6에서 설치 안 했다면
jupyter notebook ch07\ch07_prompt_patterns.ipynb

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
source ../.venv/bin/activate
export GEMINI_API_KEY='AIzaSy...'
pip install google-genai
jupyter notebook ch07/ch07_prompt_patterns.ipynb
```

## 📊 산출물

`ch07_collected_complete.jsonl` — **본서 스키마 22필드 모두 채워진 최종 완성형**.

| 필드 | 채움 단계 |
|------|----------|
| id, title, creator, … (Dublin Core 15) | Ch.3 §3.5 설계 + Ch.4 §4.4 수집 |
| `source_url`, `license_code` | Ch.4 §4.4 |
| `keywords`, `chunk_ids` | Ch.5 §5.5 |
| `embedding_id` | Ch.6 §6.5 |
| **`summary`** | **Ch.7 §7.4 ← 이번 챕터** |

## 🔄 빌드 스크립트의 두 모드

`build_ch07_files.py`는 환경을 자동 감지한다:

- **LIVE 모드**: `GEMINI_API_KEY`가 있고 `google-genai`가 설치돼 있으면 → 실제 Gemini API 호출로 요약 생성
- **DEMO 모드**: 그 외 → 스크립트에 사전 작성된 5개 데모 요약 사용

저장소에 커밋된 `ch07_collected_complete.jsonl`은 DEMO 모드 결과 — "완성된 스키마의 모양"을 보여 주는 견본. 본인 PC에서 노트북을 실행하면 LIVE 모드로 실제 LLM 요약이 그 자리에 덮어쓰여진다.

## 🔗 본서 연결

- 사전: Ch.6 §6.5 ch06_collected_embedded.jsonl
- 이후: Ch.8 §8.1~§8.4 RAG 챗봇 — 본 챕터의 LLM 호출 + Ch.6의 의미 검색을 결합

## ⚠️ 알려진 함정

- **429 Too Many Requests**: Gemini 무료 한도(분당 약 12~15회)에 걸리면 발생 → 호출 사이 `time.sleep(5)` 권장 (책 §7.2.3 + 함정 박스)
- **JSON 깨짐**: `response_mime_type='application/json'`을 지정해도 드물게 깨질 수 있음 → `try/except` + 재시도 패턴 (책 §7.3.4 함정 박스)
- **환각(hallucination)**: LLM은 사실 검증을 안 함 → §7.3.5 제약 패턴으로 1차 방어, Ch.8에서 RAG로 본격 줄임
- **프롬프트 인젝션**: 본문에 악의적 지시가 숨어 있을 위험 → 책 더 알아보기 ① 참조
- **API 키 누출**: 코드에 직접 적지 말 것. 환경변수만 사용 (Ch.6 §6.2.4)

## 📚 외부 참고

- Gemini API 공식 문서: https://ai.google.dev/gemini-api/docs
- Google AI Studio (API 키 + 본인 한도): https://aistudio.google.com/
- Gemini 모델 라인업: https://ai.google.dev/gemini-api/docs/models
- Anthropic Claude API (호환 대안): https://docs.claude.com/
- OpenAI Platform (호환 대안): https://platform.openai.com/docs
