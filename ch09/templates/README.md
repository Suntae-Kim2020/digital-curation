# 팀 프로젝트 템플릿

본서 Ch.9 미니 프로젝트용 템플릿. 자기 폴더에 복사해 사용한다.

## 사용 흐름

```
# 🪟 Windows (PowerShell)
cd C:\DC\digital-curation
xcopy /e /i ch09\templates my_project
cd my_project
mkdir data
# data\ 폴더에 자관 PDF 10~20개 복사

# 🍎 Mac (zsh/bash)
cd ~/dc/digital-curation
cp -r ch09/templates my_project
cd my_project
mkdir data
# data/ 폴더에 자관 PDF 10~20개 복사
```

## 파일

| 파일 | 용도 |
|------|------|
| `build_my_data.py` | data/의 PDF → my_collected.jsonl (본서 스키마) |
| `my_rag.py` | ch08_rag.py 복사본, COLLECTION_NAME만 자관용으로 수정 |

## 4단계 빠른 진행 (책 §9.2)

```
[15분] 단계 1 — PDF 10~20개를 data/에 모음
[20분] 단계 2 — python build_my_data.py
                → my_collected.jsonl
[30분] 단계 3 — Ch.5/Ch.6/Ch.7 코드를 입력 파일·컬렉션 이름만 바꿔 실행
                → my_chunks.jsonl
                → ChromaDB 컬렉션 (이름은 자관용으로)
                → my_collected_filled.jsonl
[25분] 단계 4 — my_rag.py에서 COLLECTION_NAME 수정 후 실행
                → 시험 질의 5건 (마지막은 환각 방어)
```

## 자주 만나는 문제

- **PDF 본문 빈 문자열**: 스캔본일 가능성 → OCR 필요 (책 §5.2 더 알아보기 ①)
- **컬렉션 없음 에러**: my_rag.py의 COLLECTION_NAME이 Ch.6에서 만든 이름과 일치하는지 확인
- **검색 결과 엉뚱**: 청크 너무 길거나 짧을 수 있음 → max_chars 조정 (책 §5.4.2)
- **환각**: 자료에 없는 답이 그럴듯하게 나옴 → build_prompt 규칙 1번 강조 (책 §7.3.5)

상세는 책 Ch.9 §9.2~§9.3과 부록 더 알아보기 ① 참조.
