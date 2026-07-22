# digital-curation

> **AI 레디 데이터와 디지털 큐레이션** — 생성형 AI 시대, 데이터를 가치로 만드는 방법
> **📗 전자책(EPUB) 출간!** (단행본 출간 예정) · 3일 / 5일 집중 교육 교재

이 저장소는 『**AI 레디 데이터와 디지털 큐레이션**』 교재의 실습 코드·데이터셋·워크시트·참고 링크 아카이브를 보관하는 공식 저장소입니다.

---

## 📚 책 소개

| 항목 | 내용 |
|------|------|
| 제목 | AI 레디 데이터와 디지털 큐레이션 |
| 부제 | 생성형 AI 시대, 데이터를 가치로 만드는 방법 |
| 대상 | 사서·기록관리자·연구지원자·데이터 큐레이터 |
| 구성 | 들어가며 + 본문 10개 챕터 |
| 실습 환경 | **본인 PC 로컬 (Windows / macOS)** · Python 3.12 + Jupyter + ChromaDB · Google Gemini API (무료 한도) |
| 출간 형태 | **전자책(EPUB) 출간** · 단행본 출간 예정 |

> 본서는 **로컬 PC 실행을 기본**으로 합니다. Colab을 사용하지 않으며, 모든 코드는 본인 노트북·데스크톱에서 직접 실행합니다. 환경 구축은 책 Ch.1에서 단계별로 안내됩니다.

---

## 🛒 전자책 구매

전자책(EPUB)이 주요 온라인 서점에서 출간되었습니다.

| 서점 | 링크 |
|------|------|
| 📗 교보문고 | https://ebook-product.kyobobook.co.kr/dig/epd/ebook/E000013278674 |
| 📘 예스24 | https://www.yes24.com/product/goods/193987832 |
| 📙 알라딘 | https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=398300155 |

---

## 🗂️ 저장소 구조

```
digital-curation/
├── ch02/   Ch.2 디지털 큐레이션과 AI 레디 데이터 — 진단 워크시트
├── ch03/   Ch.3 메타데이터 설계 실습 — 22필드 스키마·샘플 jsonl
├── ch04/   Ch.4 데이터 수집 실습 — arXiv·KCI 수집·매핑
├── ch05/   Ch.5 텍스트 전처리와 청킹 — PyMuPDF·Kiwi·청킹
├── ch06/   Ch.6 임베딩과 벡터 검색 — Gemini Embedding·ChromaDB
├── ch07/   Ch.7 Gemini API와 프롬프트 — LLM 호출·5패턴·summary
├── ch08/   Ch.8 RAG 챗봇 구축 — 본서 클라이맥스 (ch08_rag.py 통합 모듈)
├── ch09/   Ch.9 미니 프로젝트 — 자기 기관 자료로 챗봇 만들기 (워크숍 가이드)
├── ch10/   Ch.10 데이터 윤리·저작권·운영 — 라이선스·비식별·거버넌스
├── data/   공통 샘플 데이터셋
├── utils/  공통 유틸리티 코드
└── links/  인용 URL 아카이브 (Wayback 스냅숏 포함)
```

> 책의 **Ch.1 시작하기 전에 — 개발환경 만들기**는 설치·환경 설정 챕터로 별도 자산이 필요하지 않아 저장소 폴더가 없습니다. 책 본문의 단계만 따라 하면 됩니다.

각 챕터 폴더에는 다음이 포함됩니다.

- `*.ipynb` — **본인 PC의 Jupyter (또는 VS Code 노트북)** 에서 실행할 실습 노트북
- `*.py` — 재사용 가능한 모듈·빌드 스크립트
- `*.jsonl` / `*.csv` / `*.json` / `*.xlsx` — 워크시트·샘플 데이터·산출물
- `README.md` — 챕터별 실습 안내

---

## 🚀 시작하기

1. 책 **Ch.1** 의 안내에 따라 Python·VS Code·Git·가상환경(.venv)·Jupyter 설치
2. 본 저장소를 클론
   ```
   git clone https://github.com/Suntae-Kim2020/digital-curation.git
   ```
3. 가상환경 활성화 후 챕터별 README의 `pip install ...` 명령 실행
4. 원하는 챕터 폴더로 이동해 `.ipynb` 노트북을 Jupyter에서 열어 실행
5. Gemini API 키 발급·환경변수 등록은 [`./ch06/README.md`](./ch06/README.md) 참조

---

## 🔗 링크 보존 정책

본서의 모든 인용 URL은 출간 직전 일괄 재검증됩니다. 출간 이후 사라진 링크는 [`/links/archive.md`](./links/archive.md)에서 **Wayback Machine 스냅숏**으로 확인할 수 있습니다.

---

## ⚖️ 라이선스

- 실습 코드: **MIT License**
- 교재 본문: 저작권 © 김선태(Suntae Kim), 무단 전재·배포 금지
- 샘플 데이터: 각 데이터셋의 원 라이선스를 따름(공공누리·CC 등 표기)

---

## 📮 문의

- 저자: 김선태 (Suntae Kim) · kim.suntae@jbnu.ac.kr
- 이슈 등록: [GitHub Issues](https://github.com/Suntae-Kim2020/digital-curation/issues)
