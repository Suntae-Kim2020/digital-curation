# Chapter 2. 메타데이터 설계 실습

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch02_metadata_schema.ipynb` | **§2.4 실습 노트북** (Colab에서 바로 실행) |
| `ch02_schema.csv` | Dublin Core 15 + AI 확장 6 = 22필드 스키마 |
| `ch02_sample.jsonl` | 샘플 레코드 5건 (JSON Lines) |
| `build_ch02_files.py` | 위 두 데이터 파일을 생성하는 빌드 스크립트 |
| `build_notebook.py` | 노트북을 생성하는 빌드 스크립트 |

## 🎯 학습 목표

- 메타데이터의 5가지 표준 유형과 한국어 동음이의 함정 이해
- Dublin Core 15요소로 기본 레코드 작성
- AI 활용을 위한 6개 확장 필드 설계
- Pandas로 스키마를 CSV로 정의·검증

## 🚀 실습 시작하기

### 방법 1 — Google Colab (권장)

1. [`ch02_metadata_schema.ipynb`](./ch02_metadata_schema.ipynb)를 클릭한다.
2. 우측 상단의 **"Open in Colab"** 버튼을 누른다(자동으로 표시되지 않으면 GitHub URL 앞에 `https://colab.research.google.com/github/`를 붙여 수동 변환).
3. 셀을 순서대로 실행한다.

### 방법 2 — 로컬 Python

```
# 🪟 Windows (PowerShell)
git clone https://github.com/Suntae-Kim2020/digital-curation.git
cd digital-curation\ch02
python -m pip install pandas jupyter
jupyter notebook ch02_metadata_schema.ipynb

# 🍎 Mac (zsh/bash)
git clone https://github.com/Suntae-Kim2020/digital-curation.git
cd digital-curation/ch02
python3 -m pip install pandas jupyter
jupyter notebook ch02_metadata_schema.ipynb
```

## 📊 산출물

이 챕터를 마치면 다음 두 파일을 자기 기관 데이터에 맞게 가지고 있어야 한다.

1. **메타데이터 스키마** (`my_schema.csv`)
2. **샘플 레코드 5~10건** (`my_records.jsonl`)

## 🔗 본서 관련 참고

- 사전 학습: Ch.1 §1.3 AI 레디 데이터 5조건 + Ch.1 §1.4 데이터 진단 결과
- 이후 활용:
  - Ch.3 §3.4 수집한 외부 데이터를 이 스키마에 매핑
  - Ch.4 §4.3 LLM·형태소 분석으로 `keywords` 채우기
  - Ch.4 §4.4 청킹 후 `chunk_ids` 채우기
  - Ch.5 §5.3 벡터DB 적재 후 `embedding_id` 채우기
  - Ch.6 §6.4 LLM 자동 요약으로 `summary` 채우기

## 📚 외부 참고 링크

- DCMI Metadata Terms: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
- Schema.org: https://schema.org/
- DOI: https://www.doi.org/
- ARK Alliance: https://arks.org/
- ORCID: https://orcid.org/
- 공공누리: https://www.kogl.or.kr/info/license.do

## ⚠️ 알려진 함정

- **utf-8-sig 인코딩**: Windows Excel은 BOM 없는 UTF-8 CSV의 한글을 깨뜨린다 → 본 실습은 모두 `encoding='utf-8-sig'` 사용
- **리스트 필드 보존**: CSV는 리스트(`subject`, `keywords`)를 문자열로만 저장한다 → 본 실습은 **JSON Lines**(`.jsonl`)를 권장
- **license 표기는 표준 코드로**: 자유 문장이 아니라 `CC-BY-4.0`·`KOGL-1`·`ALL-RIGHTS-RESERVED` 같은 코드로 기록 (Ch.9 §9.1에서 활용)
