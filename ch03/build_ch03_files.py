# -*- coding: utf-8 -*-
r"""
ch03_schema.csv 와 ch03_sample.jsonl 생성기

교재 Chapter 2 §3.4의 코드를 그대로 따른다.
[메모리 참조] feedback_impl_pitfalls.md #1, #8 — utf-8-sig 사용
"""
import io
import sys
import pandas as pd

# Windows 콘솔 cp949 회피
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# =============================================================================
# 1. 스키마 정의 (Dublin Core 15요소 + AI 확장 6요소)
# =============================================================================
schema_rows = [
    # ── Dublin Core 베이스 ──
    {"field": "id",           "type": "string",   "required": True,  "category": "ID", "desc": "고유 식별자"},
    {"field": "title",        "type": "string",   "required": True,  "category": "DC", "desc": "자료 제목"},
    {"field": "creator",      "type": "string",   "required": True,  "category": "DC", "desc": "저자/제작자"},
    {"field": "subject",      "type": "string[]", "required": False, "category": "DC", "desc": "주제어 리스트"},
    {"field": "description",  "type": "string",   "required": False, "category": "DC", "desc": "원본 설명·초록"},
    {"field": "publisher",    "type": "string",   "required": False, "category": "DC", "desc": "발행자"},
    {"field": "contributor",  "type": "string",   "required": False, "category": "DC", "desc": "공동 저자/번역자"},
    {"field": "date",         "type": "string",   "required": True,  "category": "DC", "desc": "발행일 (YYYY-MM-DD)"},
    {"field": "type",         "type": "string",   "required": False, "category": "DC", "desc": "DCMI Type 어휘"},
    {"field": "format",       "type": "string",   "required": False, "category": "DC", "desc": "MIME 타입"},
    {"field": "identifier",   "type": "string",   "required": False, "category": "DC", "desc": "ISBN/DOI 등"},
    {"field": "source",       "type": "string",   "required": False, "category": "DC", "desc": "원본 출처"},
    {"field": "language",     "type": "string",   "required": True,  "category": "DC", "desc": "ISO 639-1 (ko/en)"},
    {"field": "relation",     "type": "string",   "required": False, "category": "DC", "desc": "관계 (isPartOf 등)"},
    {"field": "coverage",     "type": "string",   "required": False, "category": "DC", "desc": "공간·시간 범위"},
    {"field": "rights",       "type": "string",   "required": False, "category": "DC", "desc": "권리 자유 표기"},
    # ── AI 활용 확장 ──
    {"field": "summary",      "type": "string",   "required": False, "category": "AI", "desc": "LLM 요약 (Ch.7 §7.4)"},
    {"field": "keywords",     "type": "string[]", "required": False, "category": "AI", "desc": "추출 키워드 (Ch.5 §5.3)"},
    {"field": "source_url",   "type": "string",   "required": True,  "category": "AI", "desc": "원본 URL"},
    {"field": "license_code", "type": "string",   "required": True,  "category": "AI", "desc": "CC-BY-4.0 등 표준 코드"},
    {"field": "chunk_ids",    "type": "string[]", "required": False, "category": "AI", "desc": "청크 ID (Ch.5 §5.4)"},
    {"field": "embedding_flag","type": "boolean", "required": False, "category": "AI", "desc": "임베딩 처리 완료 여부 (Ch.6 §6.5)"},
]
schema = pd.DataFrame(schema_rows)

# Windows Excel 한글 안전 — utf-8-sig (BOM 포함)
schema.to_csv("ch03_schema.csv", index=False, encoding="utf-8-sig")
print(f"[OK] ch03_schema.csv ({len(schema)} fields)")


# =============================================================================
# 2. 샘플 레코드 5건
# =============================================================================
sample_rows = [
    {
        "id": "R001",
        "title": "AI 레디 데이터와 디지털 큐레이션",
        "creator": "김선태",
        "subject": ["디지털 큐레이션", "메타데이터", "RAG", "생성형 AI"],
        "description": "생성형 AI 시대 도서관·기록관·연구지원자를 위한 데이터 활용 가이드. 3일/5일 집중 교육 교재.",
        "publisher": "",
        "contributor": "",
        "date": "2026-06",
        "type": "Text",
        "format": "application/pdf",
        "identifier": "",
        "source": "",
        "language": "ko",
        "relation": "",
        "coverage": "",
        "rights": "© 김선태",
        "summary": "",
        "keywords": [],
        "source_url": "https://github.com/Suntae-Kim2020/digital-curation",
        "license_code": "ALL-RIGHTS-RESERVED",
        "chunk_ids": [],
        "embedding_flag": False,
    },
    {
        "id": "R002",
        "title": "The FAIR Guiding Principles for scientific data management and stewardship",
        "creator": "Wilkinson, M. D.; Dumontier, M.; Aalbersberg, I. J.; et al.",
        "subject": ["FAIR", "data management", "scientific data"],
        "description": "FAIR 원칙을 처음 정립한 2016년 Nature Scientific Data 논문.",
        "publisher": "Nature Publishing Group",
        "contributor": "",
        "date": "2016-03-15",
        "type": "Article",
        "format": "text/html",
        "identifier": "10.1038/sdata.2016.18",
        "source": "Scientific Data, 3, 160018",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "CC BY 4.0",
        "summary": "",
        "keywords": [],
        "source_url": "https://doi.org/10.1038/sdata.2016.18",
        "license_code": "CC-BY-4.0",
        "chunk_ids": [],
        "embedding_flag": False,
    },
    {
        "id": "R003",
        "title": "공공데이터 개방·활용 가이드라인",
        "creator": "행정안전부",
        "subject": ["공공데이터", "개방", "활용", "가이드라인"],
        "description": "공공데이터 개방 표준, 라이선스, 품질관리에 관한 가이드.",
        "publisher": "행정안전부",
        "contributor": "",
        "date": "2024-12-01",
        "type": "Text",
        "format": "application/pdf",
        "identifier": "",
        "source": "",
        "language": "ko",
        "relation": "",
        "coverage": "대한민국",
        "rights": "공공누리 제1유형",
        "summary": "",
        "keywords": [],
        "source_url": "https://www.data.go.kr/",
        "license_code": "KOGL-1",
        "chunk_ids": [],
        "embedding_flag": False,
    },
    {
        "id": "R004",
        "title": "DCMI Metadata Terms (specification)",
        "creator": "Dublin Core Metadata Initiative",
        "subject": ["Dublin Core", "metadata", "specification"],
        "description": "DCMI가 유지·관리하는 메타데이터 용어 명세서.",
        "publisher": "DCMI",
        "contributor": "",
        "date": "2020-01-20",
        "type": "Specification",
        "format": "text/html",
        "identifier": "",
        "source": "",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "CC BY 4.0",
        "summary": "",
        "keywords": [],
        "source_url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
        "license_code": "CC-BY-4.0",
        "chunk_ids": [],
        "embedding_flag": False,
    },
    {
        "id": "R005",
        "title": "Schema.org",
        "creator": "Schema.org Community Group",
        "subject": ["Schema.org", "structured data", "JSON-LD"],
        "description": "웹용 구조화 데이터 어휘 표준 (Google·MS·Yahoo 공동 운영).",
        "publisher": "Schema.org Community Group",
        "contributor": "",
        "date": "2025-01-01",
        "type": "Vocabulary",
        "format": "text/html",
        "identifier": "",
        "source": "",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "CC BY-SA 3.0",
        "summary": "",
        "keywords": [],
        "source_url": "https://schema.org/",
        "license_code": "CC-BY-SA-3.0",
        "chunk_ids": [],
        "embedding_flag": False,
    },
]
sample = pd.DataFrame(sample_rows)

# JSON Lines로 저장 (리스트 필드 보존)
sample.to_json("ch03_sample.jsonl", orient="records", lines=True, force_ascii=False)
print(f"[OK] ch03_sample.jsonl ({len(sample)} records)")


# =============================================================================
# 3. 검증 실행
# =============================================================================
def validate(records: pd.DataFrame, schema: pd.DataFrame) -> list:
    """필수 필드 누락 점검. 에러 목록 반환 (빈 리스트=통과)"""
    errors = []
    required = schema[schema["required"]]["field"].tolist()

    missing_fields = [f for f in required if f not in records.columns]
    if missing_fields:
        errors.append(f"필수 필드 누락: {missing_fields}")

    for f in required:
        if f in records.columns:
            null_rows = records[records[f].isna() | (records[f] == "")].index.tolist()
            if null_rows:
                errors.append(f"{f}: 값 누락 행 {null_rows}")

    return errors


result = validate(sample, schema)
print(f"[검증] {'통과' if not result else result}")

# 요약 출력
print()
print("[스키마 요약]")
print(schema.groupby(["category", "required"]).size().to_string())
print()
print("[샘플 요약]")
print(sample[["id", "title", "license_code", "language"]].to_string(index=False))
