# -*- coding: utf-8 -*-
r"""
my_rag.py — 팀 프로젝트용 RAG 모듈 템플릿

ch08_rag.py를 그대로 복사하되 두 곳을 자관용으로 바꾼다.
책 §9.2.4 단계 4.

수정 포인트:
  1) COLLECTION_NAME — 팀이 Ch.6 단계에서 만든 컬렉션 이름
  2) (선택) CHROMA_DB_PATH — 컬렉션을 저장한 경로 (기본 './chroma_db' 유지 가능)

나머지 코드는 ch08_rag.py와 동일하다.
"""
import os
import chromadb
from google import genai


# =============================================================================
# ⭐ 팀이 수정할 곳 — 두 줄
# =============================================================================
COLLECTION_NAME = "YOUR_TEAM_COLLECTION"   # 예: 'my_thesis_chunks'
CHROMA_DB_PATH  = "./chroma_db"            # 컬렉션 저장 경로


# =============================================================================
# 모델·기본값 (보통 그대로)
# =============================================================================
EMB_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash"

DEFAULT_K = 3
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_OUTPUT_TOKENS = 600


# =============================================================================
# 클라이언트 초기화
# =============================================================================
if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError(
        "GEMINI_API_KEY가 설정되지 않았습니다. 책 §6.2.4 참조."
    )

ai = genai.Client()
db = chromadb.PersistentClient(path=CHROMA_DB_PATH)

try:
    collection = db.get_collection(COLLECTION_NAME)
except Exception:
    raise RuntimeError(
        f"ChromaDB 컬렉션 '{COLLECTION_NAME}'을 찾을 수 없습니다. "
        f"COLLECTION_NAME을 팀이 만든 컬렉션 이름으로 수정했는지 확인하세요. "
        f"(예: 'my_thesis_chunks')"
    )


# =============================================================================
# 4단계 함수 — ch08_rag.py와 동일
# =============================================================================
def retrieve(query: str, k: int = DEFAULT_K, where: dict | None = None):
    q_resp = ai.models.embed_content(
        model=EMB_MODEL,
        contents=[query],
        config={"output_dimensionality": 768},
    )
    q_emb = q_resp.embeddings[0].values
    kwargs = {"query_embeddings": [q_emb], "n_results": k}
    if where:
        kwargs["where"] = where
    return collection.query(**kwargs)


def build_prompt(query: str, retrieved) -> str | None:
    ids = retrieved["ids"][0]
    docs = retrieved["documents"][0]
    if not ids:
        return None

    blocks = []
    for cid, doc_text in zip(ids, docs):
        blocks.append(f"[자료 ID: {cid}]\n{doc_text}")
    context = "\n\n---\n\n".join(blocks)

    return f"""다음 [참고 자료]만을 근거로 [사용자 질문]에 답해 주세요.

[참고 자료]
{context}

[사용자 질문]
{query}

다음 규칙을 반드시 지켜 주세요:
1. 참고 자료에 없는 사실은 절대 만들어 내지 마세요.
2. 답변 끝에 [출처: 자료ID] 형태로 인용한 자료 ID를 모두 표시하세요.
3. 한국어 존댓말로, 300자 이내로 답하세요.
4. 자료만으로 답할 수 없다면 "제공된 자료에서는 확인되지 않습니다"라고 답하세요.
"""


def generate(prompt: str) -> str:
    resp = ai.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
        config={
            "temperature": DEFAULT_TEMPERATURE,
            "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
        },
    )
    return resp.text


def ask_rag(query: str, k: int = DEFAULT_K, where: dict | None = None) -> dict:
    retrieved = retrieve(query, k=k, where=where)
    prompt = build_prompt(query, retrieved)
    if prompt is None:
        return {
            "query": query,
            "answer": "제공된 자료에서는 관련 내용이 검색되지 않습니다.",
            "sources": [],
            "distances": [],
        }
    answer = generate(prompt)
    return {
        "query": query,
        "answer": answer,
        "sources": retrieved["ids"][0],
        "distances": retrieved["distances"][0],
    }


def print_rag_result(result: dict) -> None:
    print("=" * 60)
    print(f"질의: {result['query']}")
    print("=" * 60)
    print()
    print("[답변]")
    print(result["answer"])
    print()
    if result["sources"]:
        print("[출처]")
        for cid, dist in zip(result["sources"], result["distances"]):
            print(f"  {cid}  (코사인 거리 {dist:.3f})")
    else:
        print("[출처] 검색 결과 없음")
    print()


# =============================================================================
# 데모
# =============================================================================
if __name__ == "__main__":
    import json

    # 시험 질의 5개를 ch09_demo_queries_template.json 또는 팀 직접 작성
    with open("../ch09_demo_queries_template.json", "r", encoding="utf-8") as f:
        template = json.load(f)
        queries = [q["your_query"] for q in template["queries"]
                   if q["your_query"] != "(여기에 팀 질의 작성)"]

    if not queries:
        print("[안내] ch09_demo_queries_template.json의 your_query 자리에")
        print("       팀 질의를 채워 넣은 뒤 다시 실행하세요.")
        sys.exit(0)

    for q in queries:
        print_rag_result(ask_rag(q))
