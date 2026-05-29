# digital-curation

> **AI 레디 데이터와 디지털 큐레이션** — 생성형 AI 시대, 데이터를 가치로 만드는 방법
> 단행본 + 전자책 출간 예정 · 3일 / 5일 집중 교육 교재

이 저장소는 『**AI 레디 데이터와 디지털 큐레이션**』 교재의 실습 코드·데이터셋·워크시트·참고 링크 아카이브를 보관하는 공식 저장소입니다.

---

## 📚 책 소개

| 항목 | 내용 |
|------|------|
| 제목 | AI 레디 데이터와 디지털 큐레이션 |
| 부제 | 생성형 AI 시대, 데이터를 가치로 만드는 방법 |
| 대상 | 사서·기록관리자·연구지원자·데이터 큐레이터 |
| 구성 | 본문 9개 챕터 + 부록 3종 |
| 실습 환경 | Google Colab + Google Gemini API (무료) + ChromaDB |
| 출간 형태 | 단행본 + 전자책(EPUB) 동시 출간 |

---

## 🗂️ 저장소 구조

```
digital-curation/
├── ch01/   디지털 큐레이션과 AI 레디 데이터
├── ch02/   메타데이터 설계 실습
├── ch03/   데이터 수집 실습
├── ch04/   텍스트 전처리와 청킹
├── ch05/   임베딩과 벡터 검색
├── ch06/   Gemini API와 프롬프트
├── ch07/   RAG 챗봇 구축
├── ch08/   미니 프로젝트
├── ch09/   데이터 윤리·저작권·운영
├── data/   공통 샘플 데이터셋
├── utils/  공통 유틸리티 코드
└── links/  인용 URL 아카이브 (Wayback 스냅숏 포함)
```

각 챕터 폴더에는 다음이 포함됩니다.

- `*.ipynb` — Colab 실습 노트북
- `*.xlsx` / `*.csv` / `*.json` — 워크시트 및 샘플 데이터
- `README.md` — 챕터별 실습 안내

---

## 🚀 시작하기

1. 본 저장소의 원하는 챕터 폴더로 이동
2. `.ipynb` 파일을 클릭하면 GitHub에서 미리보기 가능
3. **"Open in Colab"** 버튼으로 즉시 실습 시작
4. Gemini API 키 발급은 [부록 A 가이드](./ch01/README.md) 참조

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
