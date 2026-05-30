# -*- coding: utf-8 -*-
r"""
ch04_collected.jsonl 생성기

arXiv API에서 RAG 관련 논문 5건을 가져와 Ch.3 §3.4 스키마에 매핑한다.
네트워크 실패 시 동봉된 mock 데이터로 자동 폴백한다.
"""
import io
import sys
import time
import json
import pandas as pd
import requests
from xml.etree import ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# =============================================================================
# 1. arXiv API 호출 함수
# =============================================================================
def fetch_arxiv(query="retrieval augmented generation", max_results=5):
    """arXiv API 호출 → Atom XML"""
    BASE = "https://export.arxiv.org/api/query"
    params = {"search_query": f"all:{query}", "start": 0, "max_results": max_results}
    headers = {"User-Agent": "AI-Curation-Course/1.0 (kim.suntae@jbnu.ac.kr)"}
    r = requests.get(BASE, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    return r.content


def map_arxiv_entry(e, ns):
    """arXiv Atom <entry> → Ch.3 §3.4 스키마"""
    arxiv_id = e.find("atom:id", ns).text.split("/")[-1]
    authors = [a.find("atom:name", ns).text for a in e.findall("atom:author", ns)]
    return {
        "id":           f"arxiv:{arxiv_id}",
        "title":        e.find("atom:title", ns).text.strip(),
        "creator":      "; ".join(authors),
        "subject":      [],
        "description":  e.find("atom:summary", ns).text.strip(),
        "publisher":    "arXiv",
        "contributor":  "",
        "date":         e.find("atom:published", ns).text[:10],
        "type":         "Article",
        "format":       "application/pdf",
        "identifier":   arxiv_id,
        "source":       "",
        "language":     "en",
        "relation":     "",
        "coverage":     "",
        "rights":       "arXiv non-exclusive license",
        "summary":      "",
        "keywords":     [],
        "source_url":   e.find("atom:id", ns).text,
        "license_code": "ARXIV-NONEXCLUSIVE",
        "chunk_ids":    [],
        "embedding_id": "",
    }


# =============================================================================
# 2. Mock 데이터 (네트워크 실패 시 폴백)
# =============================================================================
MOCK_RECORDS = [
    {
        "id": "arxiv:2005.11401v4",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "creator": "Patrick Lewis; Ethan Perez; Aleksandra Piktus; Fabio Petroni; et al.",
        "subject": [],
        "description": "Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks…",
        "publisher": "arXiv",
        "contributor": "",
        "date": "2020-05-22",
        "type": "Article",
        "format": "application/pdf",
        "identifier": "2005.11401v4",
        "source": "",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "arXiv non-exclusive license",
        "summary": "",
        "keywords": [],
        "source_url": "http://arxiv.org/abs/2005.11401v4",
        "license_code": "ARXIV-NONEXCLUSIVE",
        "chunk_ids": [],
        "embedding_id": "",
    },
    {
        "id": "arxiv:2312.10997v5",
        "title": "Retrieval-Augmented Generation for Large Language Models: A Survey",
        "creator": "Yunfan Gao; Yun Xiong; Xinyu Gao; Kangxiang Jia; et al.",
        "subject": [],
        "description": "Large Language Models (LLMs) demonstrate significant capabilities but face challenges such as hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes…",
        "publisher": "arXiv",
        "contributor": "",
        "date": "2023-12-18",
        "type": "Article",
        "format": "application/pdf",
        "identifier": "2312.10997v5",
        "source": "",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "arXiv non-exclusive license",
        "summary": "",
        "keywords": [],
        "source_url": "http://arxiv.org/abs/2312.10997v5",
        "license_code": "ARXIV-NONEXCLUSIVE",
        "chunk_ids": [],
        "embedding_id": "",
    },
    {
        "id": "arxiv:2401.18059v1",
        "title": "RAFT: Adapting Language Model to Domain Specific RAG",
        "creator": "Tianjun Zhang; Shishir G. Patil; Naman Jain; Sheng Shen; et al.",
        "subject": [],
        "description": "Pretraining Large Language Models (LLMs) on large corpora of textual data is now a standard paradigm…",
        "publisher": "arXiv",
        "contributor": "",
        "date": "2024-03-15",
        "type": "Article",
        "format": "application/pdf",
        "identifier": "2403.10131v1",
        "source": "",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "arXiv non-exclusive license",
        "summary": "",
        "keywords": [],
        "source_url": "http://arxiv.org/abs/2403.10131v1",
        "license_code": "ARXIV-NONEXCLUSIVE",
        "chunk_ids": [],
        "embedding_id": "",
    },
    {
        "id": "arxiv:2104.07567v3",
        "title": "Dense Passage Retrieval for Open-Domain Question Answering",
        "creator": "Vladimir Karpukhin; Barlas Oğuz; Sewon Min; Patrick Lewis; et al.",
        "subject": [],
        "description": "Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method…",
        "publisher": "arXiv",
        "contributor": "",
        "date": "2020-04-10",
        "type": "Article",
        "format": "application/pdf",
        "identifier": "2004.04906v3",
        "source": "",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "arXiv non-exclusive license",
        "summary": "",
        "keywords": [],
        "source_url": "http://arxiv.org/abs/2004.04906v3",
        "license_code": "ARXIV-NONEXCLUSIVE",
        "chunk_ids": [],
        "embedding_id": "",
    },
    {
        "id": "arxiv:2305.06983v1",
        "title": "Active Retrieval Augmented Generation",
        "creator": "Zhengbao Jiang; Frank F. Xu; Luyu Gao; Zhiqing Sun; et al.",
        "subject": [],
        "description": "Despite the remarkable ability of large language models (LMs) to comprehend and generate language, they have a tendency to hallucinate and create factually inaccurate output…",
        "publisher": "arXiv",
        "contributor": "",
        "date": "2023-05-11",
        "type": "Article",
        "format": "application/pdf",
        "identifier": "2305.06983v1",
        "source": "",
        "language": "en",
        "relation": "",
        "coverage": "",
        "rights": "arXiv non-exclusive license",
        "summary": "",
        "keywords": [],
        "source_url": "http://arxiv.org/abs/2305.06983v1",
        "license_code": "ARXIV-NONEXCLUSIVE",
        "chunk_ids": [],
        "embedding_id": "",
    },
]


# =============================================================================
# 3. 메인
# =============================================================================
def main():
    records = []
    try:
        print("[arXiv API 호출] retrieval augmented generation 5건")
        xml_bytes = fetch_arxiv(max_results=5)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml_bytes)
        entries = root.findall("atom:entry", ns)
        records = [map_arxiv_entry(e, ns) for e in entries]
        print(f"  → 성공: {len(records)}건")
        time.sleep(3)  # arXiv 매너
    except Exception as ex:
        print(f"  [네트워크 실패] {ex.__class__.__name__}: {ex}")
        print("  → mock 데이터로 폴백")
        records = MOCK_RECORDS

    # 저장
    df = pd.DataFrame(records)
    df.to_json("ch04_collected.jsonl", orient="records", lines=True, force_ascii=False)
    print(f"\n[OK] ch04_collected.jsonl ({len(df)} records)")

    # 요약
    print("\n[수집 결과 요약]")
    print(df[["id", "date", "language", "license_code"]].to_string(index=False))

    # Ch.3 스키마와 검증
    schema_path = "../ch02/ch02_schema.csv"
    try:
        schema = pd.read_csv(schema_path, encoding="utf-8-sig")
        required = schema[schema["required"]]["field"].tolist()
        errors = []
        for f in required:
            if f not in df.columns:
                errors.append(f"필수 필드 누락: {f}")
            else:
                nulls = df[df[f].isna() | (df[f] == "")].index.tolist()
                if nulls:
                    errors.append(f"{f}: 값 누락 행 {nulls}")
        print(f"\n[Ch.3 스키마 검증] {'통과' if not errors else errors}")
    except FileNotFoundError:
        print(f"\n[스키마 검증 생략] {schema_path} 없음")


if __name__ == "__main__":
    main()
