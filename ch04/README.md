# Chapter 4. 데이터 수집 실습

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch04_data_collection.ipynb` | **§4.2~§4.4 실습 노트북** (본인 PC의 Jupyter 또는 VS Code 노트북에서 실행) |
| `ch04_collected.jsonl` | arXiv RAG 논문 5건 매핑 결과 (Ch.3 스키마) |
| `build_ch04_files.py` | arXiv API 호출 + 매핑 + 폴백 빌드 스크립트 |
| `build_notebook.py` | 노트북 빌더 |

## 🎯 학습 목표

- 어떤 출처에서 어떤 권리 조건으로 데이터를 수집할지 판단
- arXiv·공공데이터 API 호출 + 인증키 안전 관리
- robots.txt 점검 + 웹 크롤링 매너
- 수집 결과를 Ch.3 §3.4 스키마에 매핑

## 🚀 실습 시작하기 (본인 PC에서 직접)

이 실습은 본서 Ch.1에서 만든 본인 PC의 로컬 환경에서 진행한다.

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
..\.venv\Scripts\Activate.ps1     # 가상환경 활성화 → (.venv) 표시 확인
pip install requests beautifulsoup4 lxml
jupyter notebook ch04\ch04_data_collection.ipynb

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
source ../.venv/bin/activate      # 가상환경 활성화 → (.venv) 표시 확인
pip install requests beautifulsoup4 lxml
jupyter notebook ch04/ch04_data_collection.ipynb
```

> Ch.3를 이미 거쳤다면 pandas는 설치되어 있다. requests·beautifulsoup4·lxml만 추가 설치하면 된다.
> Ch.1에서 가상환경을 만들지 않았다면 먼저 본서 Ch.1 §1.7을 따라 환경을 준비한다.

## 📊 산출물

- `ch04_collected.jsonl` — 수집된 5건의 RAG 논문 (Ch.3 22필드 스키마)
- 본문에서 의미 차원 필드(`summary`, `keywords`, `chunk_ids`)는 비어 있고 `embedding_flag`는 False
- 후속 챕터에서 단계적으로 채움

## 🔗 본서 연결

- 사전: Ch.3 §3.2 Dublin Core / §3.3 AI 확장 / §3.4 스키마
- 이후: Ch.5 §5.1 데이터 정제 → 이 폴더의 `ch04_collected.jsonl`을 입력으로 사용

## ⚠️ 알려진 함정

- **arXiv rate limit**: 짧은 시간 다수 호출 → 429 차단. `time.sleep(3)` 필수
- **공공데이터포털 인증키**: 환경변수 `DATA_GO_KR_KEY`로 안전 관리 (책 §4.2.2)
- **robots.txt**: 크롤링 전 매번 점검 (책 §4.3.2 + 노트북 4단계)
- **API 키 None**: `os.getenv()`가 None이면 명시적 `raise` (책의 표준 패턴)

## 📚 외부 참고

- arXiv API: https://info.arxiv.org/help/api/index.html
- requests: https://requests.readthedocs.io/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
- OAI-PMH: https://www.openarchives.org/pmh/
- IIIF: https://iiif.io/
- 공공데이터포털: https://www.data.go.kr
- 국립중앙도서관: https://www.nl.go.kr/
- KISTI ScienceON: https://scienceon.kisti.re.kr/
