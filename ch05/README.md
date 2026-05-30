# Chapter 5. 텍스트 전처리와 청킹

## 📁 이 폴더의 파일

| 파일 | 용도 |
|------|------|
| `ch05_text_preprocessing.ipynb` | **§5.2~§5.5 실습 노트북** (PyMuPDF·Kiwi·청킹 3전략·통합 파이프라인) |
| `ch05_chunks.jsonl` | 청크 모음 — Ch.6 §6.3 ChromaDB 임베딩의 직접 입력 |
| `ch05_collected_filled.jsonl` | Ch.3 스키마의 keywords·chunk_ids 두 필드가 채워진 완성형 |
| `build_ch05_files.py` | Ch.4 입력 → ch05 두 산출물 자동 생성 (Kiwi 없으면 영문 fallback) |
| `build_notebook.py` | 노트북 빌더 |

## 🎯 학습 목표

- PDF·HWP 자료에서 본문 텍스트를 안전하게 추출한다 (PyMuPDF)
- 한국어 형태소 분석으로 명사 키워드를 자동 추출한다 (Kiwi)
- 본문을 세 가지 전략(fixed·sentence·sentence_overlap)으로 청킹하고 결과를 비교한다
- Ch.4 수집 데이터를 본 챕터의 청크 산출물로 가공한다

## 🚀 실습 시작하기 (본인 PC에서 직접)

이 실습은 본서 Ch.1에서 만든 본인 PC의 로컬 환경에서 진행한다. 가상환경(.venv)에 본 챕터의 두 라이브러리를 추가 설치한다.

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
..\.venv\Scripts\Activate.ps1     # 가상환경 활성화 → (.venv) 표시 확인
pip install pymupdf kiwipiepy
jupyter notebook ch05\ch05_text_preprocessing.ipynb

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
source ../.venv/bin/activate
pip install pymupdf kiwipiepy
jupyter notebook ch05/ch05_text_preprocessing.ipynb
```

> Ch.3·Ch.4를 이미 거쳤다면 pandas는 설치돼 있다. pymupdf·kiwipiepy만 추가하면 된다.

## 📊 산출물

- `ch05_chunks.jsonl` — 청크 1개 = 1줄. `chunk_id`로 Ch.6 ChromaDB에서 식별
- `ch05_collected_filled.jsonl` — 본서 표준 22필드 중 keywords·chunk_ids가 채워진 상태

## 🔗 본서 연결

- 사전: Ch.3 §3.3 스키마 / Ch.4 §4.4 ch04_collected.jsonl
- 이후: Ch.6 §6.3 ChromaDB 임베딩 — ch05_chunks.jsonl이 입력

## ⚠️ 알려진 함정

- **스캔본 PDF**: 본문이 이미지로 들어 있어 PyMuPDF가 텍스트를 못 뽑음 → OCR 필요 (Tesseract 또는 PaddleOCR; 책 §5.2 끝 '더 알아보기 ①' 참조)
- **HWP**: Python 3.12 이상을 안정 지원하는 라이브러리가 없음 → 한컴오피스로 PDF 변환 후 PyMuPDF로 처리 (책 §5.2.4 권장)
- **Kiwi vs KoNLPy**: KoNLPy는 자바 의존이 까다로움 → 본서는 Kiwi(kiwipiepy)를 표준으로 채택
- **1글자 명사**: '것', '수', '때' 같은 의존 명사가 키워드 상위를 점령 → `len(t.form) >= 2` 필터링

## 📚 외부 참고

- PyMuPDF: https://pymupdf.readthedocs.io/
- Kiwi (Korean morphological analyzer): https://github.com/bab2min/Kiwi
- kiwipiepy (Kiwi의 Python 패키지): https://github.com/bab2min/kiwipiepy
- Tesseract OCR (한국어 OCR): https://github.com/tesseract-ocr/tesseract
- PaddleOCR (한국어 OCR 대안): https://github.com/PaddlePaddle/PaddleOCR
