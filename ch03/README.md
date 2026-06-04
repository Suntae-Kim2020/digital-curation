# Chapter 3. 메타데이터 설계 실습

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch03_metadata_schema.ipynb` | **§3.4 실습 노트북** (본인 PC의 Jupyter 또는 VS Code 노트북에서 실행) |
| `ch03_schema.csv` | Dublin Core 15 + AI 확장 6 = 22필드 스키마 |
| `ch03_sample.jsonl` | 샘플 레코드 5건 (JSON Lines) |
| `build_ch03_files.py` | 위 두 데이터 파일을 생성하는 빌드 스크립트 |
| `build_notebook.py` | 노트북을 생성하는 빌드 스크립트 |

## 🎯 학습 목표

- 메타데이터의 5가지 표준 유형과 한국어 동음이의 함정 이해
- Dublin Core 15요소로 기본 레코드 작성
- AI 활용을 위한 6개 확장 필드 설계
- Pandas로 스키마를 CSV로 정의·검증

## 🚀 실습 시작하기 (본인 PC에서 직접)

이 실습은 본서 Ch.1에서 만든 본인 PC의 로컬 환경에서 진행한다.
Python·VS Code·Claude Code·가상환경(.venv)·Jupyter는 Ch.1에서 이미 설치된 것으로 가정한다.

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
..\.venv\Scripts\Activate.ps1     # 가상환경 활성화 → (.venv) 표시 확인
pip install pandas                # 본 챕터의 새 라이브러리
jupyter notebook ch03\ch03_metadata_schema.ipynb

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
source ../.venv/bin/activate      # 가상환경 활성화 → (.venv) 표시 확인
pip install pandas                # 본 챕터의 새 라이브러리
jupyter notebook ch03/ch03_metadata_schema.ipynb
```

> Ch.1에서 가상환경을 만들지 않았다면 먼저 본서 Ch.1 §1.7을 따라 환경을 준비한다.

## 📊 산출물

이 챕터를 마치면 다음 두 파일을 자기 기관 데이터에 맞게 가지고 있어야 한다.

1. **메타데이터 스키마** (`my_schema.csv`)
2. **샘플 레코드 5~10건** (`my_records.jsonl`)

## 🔗 본서 관련 참고

- 사전 학습: Ch.2 §2.3 AI 레디 데이터 5조건 + Ch.2 §2.4 데이터 진단 결과
- 이후 활용:
  - Ch.4 §4.4 수집한 외부 데이터를 이 스키마에 매핑
  - Ch.5 §5.3 LLM·형태소 분석으로 `keywords` 채우기
  - Ch.5 §5.4 청킹 후 `chunk_ids` 채우기
  - Ch.6 §6.5 벡터DB 적재 후 `embedding_flag` True로 켜기
  - Ch.7 §7.4 LLM 자동 요약으로 `summary` 채우기

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
- **license 표기는 표준 코드로**: 자유 문장이 아니라 `CC-BY-4.0`·`KOGL-1`·`ALL-RIGHTS-RESERVED` 같은 코드로 기록 (Ch.10 §10.1에서 활용)
