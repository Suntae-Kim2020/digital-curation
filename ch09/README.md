# Chapter 9. 미니 프로젝트 — 자기 기관 RAG 챗봇

본서 Ch.4~Ch.8 코드 자산을 **자기 기관 자료**로 갈아 끼우는 90분 워크숍.

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch09_rubric.json` | **평가 루브릭** — 4기준 × 4단계 (16점 만점, 통과선 12점) |
| `ch09_demo_queries_template.json` | 시험 질의 5개 템플릿 (환각 방어 시험 포함) |
| `templates/build_my_data.py` | 팀용 PDF → 스키마 매핑 빌더 |
| `templates/my_rag.py` | 팀용 RAG 모듈 (ch08_rag 복사본, COLLECTION_NAME만 수정) |
| `templates/README.md` | 팀 작업 시작 가이드 |
| `build_ch09_files.py` | 본 폴더의 루브릭·질의 템플릿 재생성 + 워크숍 안내 출력 |

## 🎯 학습 목표

- 본서 코드 자산이 다른 도메인 자료에 어떻게 재사용되는지 직접 확인
- 자기 기관 자료 5~30건으로 동작하는 RAG 챗봇 완성
- 4기준 평가 루브릭으로 팀·동료 평가

## 🚀 워크숍 진행 (90분 + 8분 시연)

### 사전 조건
- Ch.5~Ch.8을 따라 한 번 실행해 봐서 코드와 데이터 흐름을 안다
- 환경변수 `GEMINI_API_KEY` 등록 + ChromaDB·google-genai 설치

### 단계 1 — 자료 준비 (15분)

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
xcopy /e /i ch09\templates my_project
cd my_project
mkdir data

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
cp -r ch09/templates my_project
cd my_project
mkdir data
```

자관 자료(PDF) 10~20개를 `my_project/data/`에 복사한다. HWP는 한컴오피스로 PDF 변환 후 복사 (책 §5.2.4).

### 단계 2 — 본문 추출·매핑 (20분)

```
python build_my_data.py
# → my_collected.jsonl 생성
```

`build_my_data.py`의 `CREATOR_DEFAULT`·`extract_metadata_from_filename()`을 자관 규칙에 맞게 손본다.

### 단계 3 — 청킹·임베딩·요약 (30분)

본서 ch05/ch06/ch07 빌드 스크립트를 입력 파일·컬렉션 이름만 바꿔 실행:

```
# 청킹 (Ch.5 코드 — INPUT만 'my_collected.jsonl'로)
# 임베딩 (Ch.6 노트북 — collection name을 'my_thesis_chunks' 같이 변경)
# 요약 (Ch.7 코드 — INPUT만 'my_collected_filled.jsonl'로)
```

### 단계 4 — RAG 조립·테스트 (25분)

```
# my_rag.py에서 COLLECTION_NAME 한 줄만 수정
# ch09_demo_queries_template.json의 your_query 자리 5개에 팀 질의 작성
python my_rag.py
```

### 8분 시연 (팀당)

| 시간 | 내용 |
|------|------|
| 1분 | 소개 — 자관·자료·건수 |
| 3분 | 시연 — 시험 질의 3~4건 (마지막은 환각 방어) |
| 1분 | 회고 — 어디가 어려웠는지 |
| 3분 | Q&A |

## 📊 평가 루브릭 (ch09_rubric.json)

| 기준 | 1점 | 4점 |
|------|-----|-----|
| 데이터 품질 | 본문 추출 깨짐 다수 | 스키마 22필드 완성 |
| 검색 정확도 | 관련 없는 청크 자주 | 상위 3개 모두 관련 |
| 답변 충실성 | 자료 외 내용 자주 | 자료 기반 일관 |
| 출처 표시 | 출처 빠짐 잦음 | 모든 답변 정확한 ID |

**16점 만점 / 12점 이상 통과**

## 🔗 본서 연결

- 사전:
  - 본서 Ch.4~Ch.8 코드 한 번씩 통과 (필수)
  - Ch.6 §6.2.4 GEMINI_API_KEY 등록
- 이후: Ch.10 자관 본격 운영을 위한 저작권·개인정보·비용·거버넌스

## ⚠️ 알려진 함정

`templates/README.md`의 '자주 만나는 문제' 섹션 참조.

가장 잦은 4가지:
- 스캔본 PDF → 본문 빈 문자열 → OCR 필요
- COLLECTION_NAME 불일치 → my_rag.py 첫 줄 확인
- 청크 크기 비정상 → max_chars 조정
- 환각 → build_prompt 규칙 강조

## 📚 외부 참고

본 챕터는 외부 인용 없이 본서 Ch.4~Ch.8 코드와 흐름을 그대로 재사용한다. 관련 문헌은 각 본문 챕터의 참고문헌 절을 참조한다.
