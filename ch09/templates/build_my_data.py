# -*- coding: utf-8 -*-
r"""
build_my_data.py — 팀 프로젝트용 데이터 빌더 템플릿

이 폴더 안의 `data/`에 있는 PDF들을 본서 표준 스키마로 매핑해
my_collected.jsonl로 저장한다. 책 §9.2.2 단계 2.

사용 흐름:
  1) my_project/data/ 폴더에 PDF 10~20개 복사
  2) (.venv 활성 상태에서) python build_my_data.py 실행
  3) my_collected.jsonl 생성 확인

수정 포인트(팀이 손볼 곳):
  - CREATOR_DEFAULT, LICENSE_DEFAULT: 자관 자료의 기본값으로
  - extract_metadata_from_filename(): 파일명 규칙에 맞춰 자관 ID·제목 추출
"""
import io
import os
import sys
import json
import glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import fitz  # PyMuPDF
except ImportError:
    print("[ERR] pymupdf가 설치되지 않았습니다. pip install pymupdf 후 다시 실행하세요.")
    sys.exit(1)


# =============================================================================
# 팀이 자관 환경에 맞춰 수정할 곳
# =============================================================================
CREATOR_DEFAULT = "미상"                # 저자 정보 없을 때 기본값
LICENSE_DEFAULT = "INTERNAL"            # 자관 내부 자료 라이선스 코드


def extract_metadata_from_filename(filename: str) -> dict:
    """파일명에서 ID·제목·일자를 뽑는다. 팀이 자관 규칙에 맞춰 수정.

    기본 동작: 파일명 그대로 ID, 언더스코어를 띄어쓰기로 바꾼 형태를 제목으로.
    예) 'thesis_2022_0314_natural_language.pdf' →
        id='my:thesis_2022_0314_natural_language',
        title='thesis 2022 0314 natural language'

    학위논문이라면 'thesis-{year}-{num}' 패턴으로 ID를 통일하는 식으로 손본다.
    """
    base = os.path.basename(filename).replace(".pdf", "")
    return {
        "id":    f"my:{base}",
        "title": base.replace("_", " ").replace("-", " "),
        "date":  "",      # 팀이 자관 규칙에서 추출
    }


# =============================================================================
# PDF 본문 추출
# =============================================================================
def extract_pdf_text(path: str) -> str:
    """모든 페이지를 [page N] 표시와 함께 이어 붙임 — 책 §5.2.2"""
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc, start=1):
        pages.append(f"[page {i}]\n{page.get_text()}")
    doc.close()
    return "\n\n".join(pages)


# =============================================================================
# 메인
# =============================================================================
def main():
    pdfs = sorted(glob.glob("data/*.pdf"))
    if not pdfs:
        print("[ERR] data/ 폴더에 PDF가 없습니다.")
        print("       10~20개의 PDF를 data/ 폴더에 복사한 뒤 다시 실행하세요.")
        sys.exit(1)

    print(f"[입력] data/ 폴더 PDF {len(pdfs)}개")

    records = []
    for path in pdfs:
        meta = extract_metadata_from_filename(path)
        description = extract_pdf_text(path)

        if not description.strip():
            print(f"  [경고] {path} — 본문 추출 실패. 스캔본 PDF일 가능성. OCR 필요 (책 §5.2 더 알아보기 ①)")
            continue

        record = {
            # Dublin Core 베이스
            "id":           meta["id"],
            "title":        meta["title"],
            "creator":      CREATOR_DEFAULT,
            "subject":      [],
            "description":  description,
            "publisher":    "",
            "contributor":  "",
            "date":         meta["date"],
            "type":         "Text",
            "format":       "application/pdf",
            "identifier":   "",
            "source":       "",
            "language":     "ko",
            "relation":     "",
            "coverage":     "",
            "rights":       "자관 내부 자료",
            # AI 6확장 (이후 단계에서 채움)
            "summary":      "",
            "keywords":     [],
            "source_url":   f"file://{os.path.abspath(path)}",
            "license_code": LICENSE_DEFAULT,
            "chunk_ids":    [],
            "embedding_flag": False,
        }
        records.append(record)
        print(f"  [OK]  {path}  ({len(description):,}자)")

    with open("my_collected.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n[저장] my_collected.jsonl ({len(records)} 레코드)")
    print()
    print("[다음 단계]")
    print("  Ch.5 build_ch05_files.py를 my_collected.jsonl로 입력 변경해 실행")
    print("  → my_chunks.jsonl + my_collected_filled.jsonl 생성됨")


if __name__ == "__main__":
    main()
