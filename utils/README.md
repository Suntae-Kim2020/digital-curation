# /utils — 공통 유틸리티

여러 챕터의 노트북에서 공통으로 import하는 유틸리티 코드입니다.

## 예정 모듈

| 파일 | 용도 |
|------|------|
| `colab_setup.py` | Colab 환경 초기화 (라이브러리 설치·API 키 로드) |
| `gemini_client.py` | Gemini API 호출 래퍼 (재시도·캐시 포함) |
| `chunker.py` | 3종 청킹 전략 함수 |
| `metadata_validator.py` | 메타데이터 스키마 검증기 |

## 사용 예 (예정)

```python
# Colab 첫 셀
!pip install -q git+https://github.com/Suntae-Kim2020/digital-curation.git
from utils.colab_setup import init
init()
```
