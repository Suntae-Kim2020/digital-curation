# Chapter 10. 데이터 윤리·저작권·운영 🏁

본서의 **마지막 챕터**. 자관에 RAG 챗봇을 본격 운영할 때 필요한 저작권·개인정보·비용·거버넌스 점검 자료.

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch10_license_codes.json` | **license_code 표준 12종** (CC·KOGL·기타, 코드에서 import 가능) |
| `ch10_pii_checklist.md` | **비식별 6단계 체크리스트** (책 §10.2.3) |
| `ch10_governance_template.md` | **거버넌스 한 페이지 템플릿** (책 §10.3.4) |
| `ch10_application_checklist.md` | **자관 적용 종합 체크리스트 10문항** |
| `ch10_cost_calculator.py` | **월간 운영비 추정기** (3가지 시나리오 데모 포함) |
| `build_ch10_files.py` | 위 자료 재생성기 |

## 🎯 이 챕터 자산을 어떻게 쓰는가

### 1) license_code 표준 — 코드에 직접 import

자관 자료의 라이선스를 표준 코드로 표기할 때 참조.

```python
import json
with open('ch10_license_codes.json', 'r', encoding='utf-8') as f:
    codes = json.load(f)

# 예: KOGL-1 라이선스 정보 조회
kogl1 = next(c for c in codes['codes'] if c['code'] == 'KOGL-1')
print(kogl1['summary'])           # '자유 이용 + 출처 표시'
print(kogl1['ai_train'])          # True → AI 학습에 활용 가능
print(kogl1['commercial'])        # True → 상업적 이용 가능
```

각 코드에 다섯 가지 boolean 플래그가 붙어 있어 RAG 답변에서 라이선스 안내를 자동 생성할 수 있다.

### 2) 비식별 체크리스트 — 인쇄 후 점검

`ch10_pii_checklist.md`를 출력해 자관 자료 점검에 사용. 6단계 각 하위 항목을 ☐로 두어 자관별로 ☑ 표시.

### 3) 거버넌스 템플릿 — 한 페이지 합의문

`ch10_governance_template.md`를 자관용으로 채워 부서·법무·기술 담당과 합의. 분기별 1회 검토.

### 4) 자관 적용 체크리스트 — 본격 운영 직전 점검

`ch10_application_checklist.md`의 **저작권 4 + 개인정보 3 + 운영 3 = 10문항** 모두 ☑이어야 본격 시작.

### 5) 비용 계산기 — 자관 시나리오 추정

```bash
python ch10_cost_calculator.py
```

세 가지 시나리오(소·중·대규모 자관) 비용을 자동 출력. 본인 자관 규모에 맞춰 파라미터 조정:

```python
from ch10_cost_calculator import estimate, print_breakdown

b = estimate(
    chunks=15_000,           # 우리 자관 청크 수
    queries_per_day=200,     # 일 평균 질의 수
    new_chunks_per_month=500, # 월 신규 청크
)
print_breakdown(b)
```

## 🔗 본서 연결

- 사전: Ch.4 §4.1.2 라이선스 점검 + Ch.7 §7.3.5 프롬프트 제약 + Ch.8 §8.3 출처 표시
- 이후: **본서 본문 끝** — 자관 두 번째 사이클 시작

## ⚠️ 알려진 함정

- **단가 변동**: `ch10_cost_calculator.py`의 `RATES`는 2026-05 기준 참고치. 운영 시점 https://ai.google.dev/pricing 에서 재확인 필요
- **TDM 자가 면책 오해**: "AI니까 다 된다"가 아니다. 적법 접근·필요 한도·향유 목적 아님 세 조건 모두 충족 필요 (책 §10.1.2)
- **가명을 익명으로 오해**: 단순 이름 변경만으로는 익명이 아니다. 결합 식별 가능성 검토 필요 (책 §10.2.2)
- **장기 운영 미고려**: 모델·자료 변경 시 재임베딩 비용·시간 사전 계획 필요 (책 §10.3.2)

## 📚 외부 참고 — 본서 닫는 페이지

본서 학습 후 자연스럽게 이어지는 다음 학습:

- 한국법령정보센터 (저작권법·개인정보보호법): https://www.law.go.kr/
- 개인정보보호위원회: https://www.pipc.go.kr/
- 공공누리 라이선스 안내: https://www.kogl.or.kr/info/license.do
- Creative Commons: https://creativecommons.org/share-your-work/cclicenses/
- Microsoft Presidio (자동 비식별): https://github.com/microsoft/presidio
- EU AI Act 공식 페이지: https://artificialintelligenceact.eu/
- OWASP LLM Top 10: https://genai.owasp.org/
- RAGAS (자동 평가): https://docs.ragas.io/

## 🎉 본서 학습 여정 완주

```
Ch.1 환경
   ↓
Ch.2 디지털 큐레이션 개념
   ↓
Ch.3 메타데이터 설계 ┐
Ch.4 데이터 수집     │ 데이터 사이클
Ch.5 전처리·청킹     ┘
   ↓
Ch.6 임베딩·ChromaDB  ── 검색
   ↓
Ch.7 Gemini LLM·프롬프트  ── 생성
   ↓
Ch.8 RAG 챗봇 ⭐  ── 통합
   ↓
Ch.9 자기 기관 미니 프로젝트  ── 응용
   ↓
Ch.10 윤리·저작권·운영  ── 본격 운영 🏁
```

본서가 자관 RAG 운영의 **첫 번째 사이클**이 되었기를 바랍니다. 두 번째 사이클은 자관 자료와 함께 시작됩니다.
