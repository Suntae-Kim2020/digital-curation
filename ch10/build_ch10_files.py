# -*- coding: utf-8 -*-
r"""
Ch.10 산출물 생성기 — 운영 참조 자료

본 챕터의 산출물은 데이터가 아니라 자관 RAG 운영에 사용할 참조 자료다.
- 라이선스 코드 표준 (JSON, 코드에서 import 가능)
- 비식별 체크리스트 (Markdown, 인쇄·검토용)
- 거버넌스 한 페이지 템플릿 (Markdown)
- 자관 적용 종합 체크리스트 (Markdown)
"""
import io
import os
import sys
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# =============================================================================
# 라이선스 코드 표준 — 책 §10.1.3
# =============================================================================
LICENSE_CODES = {
    "schema_version": "1.0",
    "last_updated": "2026-05-30",
    "codes": [
        {
            "code":     "CC-BY-4.0",
            "name":     "Creative Commons Attribution 4.0",
            "family":   "CC",
            "url":      "https://creativecommons.org/licenses/by/4.0/",
            "summary":  "출처 표시만 하면 자유 이용",
            "ai_train": True,
            "redistribute": True,
            "modify":   True,
            "commercial": True,
        },
        {
            "code":     "CC-BY-SA-4.0",
            "name":     "Creative Commons Attribution-ShareAlike 4.0",
            "family":   "CC",
            "url":      "https://creativecommons.org/licenses/by-sa/4.0/",
            "summary":  "출처 표시 + 같은 조건으로 공유",
            "ai_train": True,
            "redistribute": True,
            "modify":   True,
            "commercial": True,
            "note":     "파생물도 같은 라이선스로 공유 의무",
        },
        {
            "code":     "CC-BY-NC-4.0",
            "name":     "Creative Commons Attribution-NonCommercial 4.0",
            "family":   "CC",
            "url":      "https://creativecommons.org/licenses/by-nc/4.0/",
            "summary":  "출처 표시 + 비영리만",
            "ai_train": True,
            "redistribute": True,
            "modify":   True,
            "commercial": False,
        },
        {
            "code":     "CC-BY-ND-4.0",
            "name":     "Creative Commons Attribution-NoDerivatives 4.0",
            "family":   "CC",
            "url":      "https://creativecommons.org/licenses/by-nd/4.0/",
            "summary":  "출처 표시 + 변경 금지",
            "ai_train": True,
            "redistribute": True,
            "modify":   False,
            "commercial": True,
        },
        {
            "code":     "CC0",
            "name":     "Creative Commons Zero (Public Domain Dedication)",
            "family":   "CC",
            "url":      "https://creativecommons.org/publicdomain/zero/1.0/",
            "summary":  "공유 자산, 조건 없음",
            "ai_train": True,
            "redistribute": True,
            "modify":   True,
            "commercial": True,
        },
        {
            "code":     "KOGL-1",
            "name":     "공공누리 제1유형 (출처표시)",
            "family":   "KOGL",
            "url":      "https://www.kogl.or.kr/info/license.do",
            "summary":  "자유 이용 + 출처 표시",
            "ai_train": True,
            "redistribute": True,
            "modify":   True,
            "commercial": True,
        },
        {
            "code":     "KOGL-2",
            "name":     "공공누리 제2유형 (출처표시 + 상업적 이용금지)",
            "family":   "KOGL",
            "url":      "https://www.kogl.or.kr/info/license.do",
            "summary":  "비상업 이용만",
            "ai_train": True,
            "redistribute": True,
            "modify":   True,
            "commercial": False,
        },
        {
            "code":     "KOGL-3",
            "name":     "공공누리 제3유형 (출처표시 + 변경금지)",
            "family":   "KOGL",
            "url":      "https://www.kogl.or.kr/info/license.do",
            "summary":  "원본 유지",
            "ai_train": True,
            "redistribute": True,
            "modify":   False,
            "commercial": True,
        },
        {
            "code":     "KOGL-4",
            "name":     "공공누리 제4유형 (출처표시 + 상업적 이용금지 + 변경금지)",
            "family":   "KOGL",
            "url":      "https://www.kogl.or.kr/info/license.do",
            "summary":  "가장 제한적",
            "ai_train": True,
            "redistribute": True,
            "modify":   False,
            "commercial": False,
        },
        {
            "code":     "ARXIV-NONEXCLUSIVE",
            "name":     "arXiv non-exclusive license to distribute",
            "family":   "ARXIV",
            "url":      "https://arxiv.org/licenses/nonexclusive-distrib/1.0/",
            "summary":  "arXiv 배포 비독점 라이선스 (저자에게 저작권 유지)",
            "ai_train": True,
            "redistribute": False,
            "modify":   False,
            "commercial": False,
            "note":     "원본을 그대로 재배포하지 않는 한 학술 분석은 가능",
        },
        {
            "code":     "ALL-RIGHTS-RESERVED",
            "name":     "전통적 모든 권리 보유",
            "family":   "PROPRIETARY",
            "url":      "",
            "summary":  "사용 전 저작권자 허락 필요",
            "ai_train": False,
            "redistribute": False,
            "modify":   False,
            "commercial": False,
            "note":     "TDM 면책 조항 적용 검토 필요 (책 §10.1.2)",
        },
        {
            "code":     "INTERNAL",
            "name":     "자관 내부 자료",
            "family":   "INTERNAL",
            "url":      "",
            "summary":  "자관 정책에 따라 사용 (외부 노출 별도 검토)",
            "ai_train": True,
            "redistribute": False,
            "modify":   True,
            "commercial": True,
            "note":     "자관 내부 RAG 챗봇 적합",
        },
    ],
}


# =============================================================================
# 비식별 6단계 체크리스트 — 책 §10.2.3
# =============================================================================
PII_CHECKLIST_MD = """# 비식별 처리 6단계 체크리스트

『AI 레디 데이터와 디지털 큐레이션』 §10.2.3 참조.

자관 자료를 RAG 챗봇에 넣기 전 다음 6단계를 통과시킨다.

---

## 1️⃣ 식별자 직접 검출

본문에서 직접 식별자를 정규식·키워드 검색으로 찾아낸다.

- ☐ 이름 (한국어·한자·영문) — 정규식: `[가-힣]{2,4}` + 직원 명부 매칭
- ☐ 전화번호 — `0\\d{1,2}-\\d{3,4}-\\d{4}`
- ☐ 주민등록번호 — `\\d{6}-?\\d{7}` (저장 자체가 위법 가능)
- ☐ 이메일 — `[\\w.-]+@[\\w.-]+\\.[a-z]+`
- ☐ 주소 — '○○구 ○○동' 패턴

## 2️⃣ 직접 식별자 가명화

동일 인물에 동일 코드를 부여한다. 매핑표를 별도 안전 보관.

- ☐ 이름 → P001, P002 식 일련 번호
- ☐ 전화·이메일 → CONTACT_001 또는 마스킹
- ☐ 매핑표는 RAG 챗봇이 접근 불가한 별도 저장소

## 3️⃣ 준식별자 확인

결합하면 식별 가능한 항목들을 찾는다.

- ☐ 거주 지역 (시·군·구 단위)
- ☐ 소속 기관 (대학·부서)
- ☐ 생년월일·졸업년도 (특정 가능한 작은 그룹)
- ☐ 직책·전공
- ☐ 특이 사항 (수상·이력)

## 4️⃣ 준식별자 일반화

식별 가능성을 줄이도록 광역 단위·연대로 일반화.

- ☐ '서울 강남구' → '수도권'
- ☐ '2023년 4월 졸업' → '2020년대 초반 졸업'
- ☐ '○○과 박사 1년차' → '대학원 박사 과정'

## 5️⃣ 결합 위험 평가

외부 공개 자료와 결합 시 재식별 가능성을 검토.

- ☐ 동일 그룹(같은 소속·연차) 안에 몇 명이 있는가? (k-익명성)
- ☐ k=1이면 식별 위험 큼, k=5 이상 권장
- ☐ 외부 SNS·뉴스에 동일 인물 식별 가능한가
- ☐ 자료 공개 범위(내부·등록 이용자·일반)에 따라 차등 적용

## 6️⃣ 동의·법적 근거 확인

자료 생성 시점의 동의 범위를 최종 확인.

- ☐ 자료 수집 시 동의서 항목 점검
- ☐ AI 학습·RAG 활용이 동의 범위 안에 포함되는가
- ☐ 동의 범위 밖이면 비식별을 더 강하게 또는 자료 제외
- ☐ 동의서 메타데이터를 자료와 함께 보관

---

## 자동화 도구 (책 §10.2 더 알아보기 ②)

- **Microsoft Presidio** — 다국어 식별자 검출, 한국어 패턴 별도 등록 가능
- **KoNLPy + 정규식** — 단순 패턴(주민번호·연락처)에 충분
- **사내 사전 매칭** — 직원·이용자 명부 결합 (가장 정밀)

## 통과 기준

위 6단계를 모두 ✅로 표시하고 동의 근거가 보존된 자료만 RAG에 적재한다.
"""


# =============================================================================
# 거버넌스 한 페이지 템플릿 — 책 §10.3.4
# =============================================================================
GOVERNANCE_TEMPLATE_MD = """# RAG 챗봇 거버넌스 한 페이지

『AI 레디 데이터와 디지털 큐레이션』 §10.3.4의 거버넌스 템플릿. 자관 안에서 운영을 시작할 때 한 페이지에 핵심을 합의해 둔다.

---

## 1. 서비스 정보

- **서비스 이름**: (예: ○○대학교 학위논문 도우미)
- **버전**: v0.1 (시범) / v1.0 (정식 공개)
- **운영 시작일**: YYYY-MM-DD

## 2. 서비스 목적

(어떤 이용자에게 어떤 가치를 주는가 — 1~2 문장)

> 예: 우리 학교 학위논문 8,500편에서 주제·방법론·연구자별 검색·요약을 즉시 제공함으로써, 사서가 1차 안내에 들이는 시간을 줄이고 이용자의 자료 발견을 돕는다.

## 3. 적용 자료 범위

| 포함 | 제외 |
|------|------|
| (예: 학위논문 PDF 8,500편) | (예: 미공개·심사 중 논문) |
| (예: 자관 발간 연감) | (예: 외부 구독 자료) |

라이선스 기준: ___________
개인정보 처리: 비식별 6단계 통과한 자료만

## 4. 답변 정책

- 출처 표시: 답변 끝에 [출처: 청크ID] 의무 표시 (책 §8.3)
- 금지 답변: 자료에 없는 내용·정치·종교·민감 개인사 답변 거부
- 모르는 것: "제공된 자료에서는 확인되지 않습니다" 답변 강제
- 답변 모델: gemini-2.5-flash (temperature 0.2)
- 청크 검색: 상위 3개, 코사인 유사도 0.5 이내

## 5. 담당자

| 역할 | 이름 | 이메일 |
|------|------|--------|
| 데이터 큐레이션 책임 | | |
| 기술 운영 책임 | | |
| 법무·정책 자문 | | |
| 이용자 응대·피드백 | | |

## 6. 갱신 주기

- 신규 자료 추가: 매월 첫째 주
- 재임베딩: 임베딩 모델 변경 시 또는 청킹 전략 변경 시
- 정책 검토: 분기별 1회

## 7. 감사·로그

- **수집 항목**: 질의·시각·이용자(가명)·검색 청크·LLM 응답·이상 표시
- **보관 기간**: ___ 개월 (자관 정책 따름)
- **접근 권한**: ______ 부서만

## 8. 사용자 피드백·신고

- 잘못된 답변 신고: __________ (이메일·웹 폼)
- 개인정보 노출 신고: __________ (즉시 대응 채널)
- 일반 의견: __________

## 9. 사고 대응 절차

다음 사고 발생 시 24시간 안에 대응한다.

1. **환각**: 자료에 없는 답변이 인용된 사례 발견
   → 청크·프롬프트 점검 → 임시 답변 차단 → 보정 후 재개
2. **개인정보 노출**: 답변에 식별자가 그대로 노출
   → 즉시 챗봇 정지 → 원본 자료 비식별 재처리 → 컬렉션 재구성
3. **라이선스 위반**: 무단 사용 자료 발견
   → 해당 자료 컬렉션에서 제거 → 권리자 통보 → 절차 재정비

## 10. 점검 일자·서명

- 작성일: YYYY-MM-DD
- 작성자:
- 최종 검토:
"""


# =============================================================================
# 자관 적용 종합 체크리스트 — 책 도입부 outcomes
# =============================================================================
APPLICATION_CHECKLIST_MD = """# 자관 RAG 운영 적용 종합 체크리스트

『AI 레디 데이터와 디지털 큐레이션』 Ch.10 도입부의 10문항 체크리스트.

본격 운영을 시작하기 전 자관 안에서 한 번 점검한다.

---

## 저작권 (4문항)

- ☐ 자료마다 license_code가 표준 코드(CC-BY-4.0·KOGL-1 등)로 표기되어 있는가?
- ☐ 외부 수집 자료 중 라이선스가 명시되지 않은 자료가 있는가?
- ☐ TDM 면책 조항(저작권법 §35조의5)이 자관 활용에 해당하는지 법무 검토를 받았는가?
- ☐ 라이선스 변경·자료 철회 시 컬렉션에서 제거하는 절차가 있는가?

## 개인정보 (3문항)

- ☐ 자료에 이름·연락처·주민번호 같은 식별 정보가 포함되어 있는가?
- ☐ 비식별 6단계 체크리스트(ch10_pii_checklist.md)를 자료에 적용했는가?
- ☐ 외부 이용자에게 노출되는 RAG 답변에 권한별 접근 필터가 있는가?

## 운영 (3문항)

- ☐ 월별 API 호출량과 비용을 추정해 두었는가? (책 §10.3.1 또는 ch10_cost_calculator.py)
- ☐ 모델 변경·자료 갱신 시 재임베딩 주기를 정해 두었는가?
- ☐ 거버넌스 한 페이지(ch10_governance_template.md)가 작성·승인되어 있는가?

---

## 통과 기준

10문항 모두 ☑가 되어야 본격 운영을 시작한다. 미달이라면 미달 항목을 우선 보완한 뒤 재점검한다.

## 점검자

- 일자:
- 점검자:
- 다음 점검 예정일:
"""


def main():
    print("=" * 60)
    print(" Chapter 10. 데이터 윤리·저작권·운영 — 운영 자산 생성")
    print("=" * 60)

    # 1) license_code 표준 JSON
    with open("ch10_license_codes.json", "w", encoding="utf-8") as f:
        json.dump(LICENSE_CODES, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] ch10_license_codes.json ({len(LICENSE_CODES['codes'])}개 코드)")

    # 2) 비식별 체크리스트
    with open("ch10_pii_checklist.md", "w", encoding="utf-8") as f:
        f.write(PII_CHECKLIST_MD)
    print(f"[OK] ch10_pii_checklist.md (6단계 비식별 처리)")

    # 3) 거버넌스 템플릿
    with open("ch10_governance_template.md", "w", encoding="utf-8") as f:
        f.write(GOVERNANCE_TEMPLATE_MD)
    print(f"[OK] ch10_governance_template.md (거버넌스 한 페이지)")

    # 4) 자관 적용 체크리스트
    with open("ch10_application_checklist.md", "w", encoding="utf-8") as f:
        f.write(APPLICATION_CHECKLIST_MD)
    print(f"[OK] ch10_application_checklist.md (10문항 점검)")

    # 5) 비용 계산기는 별도 파이썬 스크립트로
    print(f"\n[참고] ch10_cost_calculator.py — 비용 추정 계산기 (별도 파일)")

    # 본서 마무리 메시지
    print()
    print("=" * 60)
    print(" 본서 GitHub 저장소 자산이 모두 완성되었습니다 🎉")
    print("=" * 60)
    print()
    print("  ch02 진단 → ch03 스키마 → ch04 수집 → ch05 청킹·키워드 →")
    print("  ch06 임베딩·벡터 검색 → ch07 LLM·요약 → ch08 RAG 챗봇 →")
    print("  ch09 미니 프로젝트 → ch10 윤리·저작권·운영")
    print()
    print("  본서가 자관 RAG 운영의 첫 사이클이 되기를 바랍니다.")


if __name__ == "__main__":
    main()
