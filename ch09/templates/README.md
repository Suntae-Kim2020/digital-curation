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

모두 파일 위치(this folder) 기준으로 경로를 잡으므로 어느 폴더에서 실행해도 동작하고,
컬렉션 이름·경로가 서로 맞춰져 있어 **순서대로 실행만** 하면 된다(추가 수정 불필요).

| 파일 | 용도 | 입력 → 출력 |
|------|------|------|
| `build_my_data.py` | data/의 PDF → 본서 스키마 매핑 | `data/*.pdf` → `my_collected.jsonl` |
| `build_my_chunks.py` | 청킹 + 키워드 (API 불필요) | `my_collected.jsonl` → `my_chunks.jsonl`, `my_collected_filled.jsonl` |
| `build_my_embed.py` | 임베딩 + ChromaDB 적재 (Gemini) | `my_chunks.jsonl` → `chroma_db/`(컬렉션 `my_thesis_chunks`), `my_collected_embedded.jsonl` |
| `build_my_summary.py` | LLM 요약 → 스키마 완성 (Gemini) | `my_collected_embedded.jsonl` → `my_collected_complete.jsonl` |
| `my_rag.py` | RAG 챗봇 모듈 (ch08_rag.py 기반) | `chroma_db/` 컬렉션 → 답변+출처 |

## 4단계 빠른 진행 (책 §9.2)

```
[15분] 단계 1 — PDF 10~20개를 data/에 모음
[20분] 단계 2 — python build_my_data.py        → my_collected.jsonl
[30분] 단계 3 — python build_my_chunks.py       → my_chunks.jsonl, my_collected_filled.jsonl
                python build_my_embed.py        → chroma_db/ 컬렉션, my_collected_embedded.jsonl
                python build_my_summary.py      → my_collected_complete.jsonl (AI 6필드 완성)
[25분] 단계 4 — python -c "from my_rag import ask_rag, print_rag_result; print_rag_result(ask_rag('질문'))"
                → 시험 질의 5건 (마지막은 환각 방어)
```

## 자주 만나는 문제

- **PDF 본문 빈 문자열**: 스캔본일 가능성 → OCR 필요 (책 Ch.5 끝 '더 알아보기 ①')
- **컬렉션 없음 에러**: my_rag.py의 COLLECTION_NAME이 Ch.6에서 만든 이름과 일치하는지 확인
- **검색 결과 엉뚱**: 청크 너무 길거나 짧을 수 있음 → max_chars 조정 (책 §5.4.2)
- **환각**: 자료에 없는 답이 그럴듯하게 나옴 → build_prompt 규칙 1번 강조 (책 §7.3.5)

상세는 책 Ch.9 §9.2~§9.3과 부록 더 알아보기 ① 참조.
