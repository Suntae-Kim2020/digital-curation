# -*- coding: utf-8 -*-
r"""
ch08_rag.py — 본서 RAG 챗봇 통합 모듈

『AI 레디 데이터와 디지털 큐레이션』 Chapter 8의 §8.2~§8.5 내용을
재사용 가능한 한 파일로 묶었다. 사용 흐름:

    from ch08_rag import ask_rag, print_rag_result

    result = ask_rag("RAG가 환각을 줄이는 원리는?")
    print_rag_result(result)

[필수 사전 조건]
- GEMINI_API_KEY 환경변수 (책 §6.2.4 참조)
- Ch.6의 ChromaDB 컬렉션(../ch06/chroma_db)이 적재돼 있음
- 경로는 이 파일 위치를 기준으로 잡으므로 어느 폴더에서 실행해도 동작한다.
"""
import os
from pathlib import Path
import chromadb
from google import genai


# =============================================================================
# 설정
# =============================================================================
EMB_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash-lite"
COLLECTION_NAME = "ai_ready_chunks"
# 컬렉션은 Ch.6에서 ch06/chroma_db에 적재했다. 이 파일(ch08) 위치를 기준으로
# 경로를 잡으므로 어느 폴더에서 실행하든(예: C:\DC) 항상 ch06/chroma_db를 가리킨다.
_HERE = Path(__file__).resolve().parent
CHROMA_DB_PATH = str(_HERE.parent / "ch06" / "chroma_db")

DEFAULT_K = 3
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_OUTPUT_TOKENS = 600
# gemini-2.5 계열은 답하기 전 '생각(thinking)'에 토큰을 쓰며, 그 양이
# max_output_tokens 한도 안에 포함된다. 0으로 끄면 토큰 전부가 답변에 쓰여
# 답변 잘림(빈 답변)을 막고 더 빠르고 저렴하다. (책 §7.2.2 참조)
THINKING_BUDGET = 0


# =============================================================================
# 클라이언트 — 모듈 로드 시 한 번만 초기화
# =============================================================================
def _check_env():
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "GEMINI_API_KEY가 설정되지 않았습니다. "
            "https://aistudio.google.com 에서 발급 후 환경변수로 등록하세요. "
            "(책 §6.2.4)"
        )


_check_env()

ai = genai.Client()
db = chromadb.PersistentClient(path=CHROMA_DB_PATH)

try:
    collection = db.get_collection(COLLECTION_NAME)
except Exception:
    raise RuntimeError(
        f"ChromaDB 컬렉션 '{COLLECTION_NAME}'을 찾을 수 없습니다. "
        f"먼저 ch06/ch06_vector_search.ipynb를 실행해 컬렉션을 만드세요. "
        f"(책 §6.3)"
    )


# =============================================================================
# 4단계 함수
# =============================================================================
def retrieve(query: str, k: int = DEFAULT_K, where: dict | None = None):
    """질의 → 임베딩 → ChromaDB에서 가까운 청크 k개."""
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
    """검색 결과를 컨텍스트로 묶고 RAG 프롬프트 작성.

    빈 검색 결과면 None 반환 — 호출자가 안전 동작을 결정.
    """
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
4. 자료만으로 답할 수 없다면 \"제공된 자료에서는 확인되지 않습니다\"라고 답하세요.
"""


def generate(prompt: str) -> str:
    """Gemini LLM 호출."""
    resp = ai.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
        config={
            "temperature": DEFAULT_TEMPERATURE,
            "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
            "thinking_config": {"thinking_budget": THINKING_BUDGET},
        },
    )
    return resp.text


def ask_rag(query: str, k: int = DEFAULT_K, where: dict | None = None) -> dict:
    """4단계 통합 — query → retrieve → augment → generate.

    반환 dict 구조:
        query     원본 질의
        answer    LLM이 생성한 답변 (또는 안전 기본 응답)
        sources   인용된 청크 ID 리스트
        distances 청크별 코사인 거리 (작을수록 가까움)
    """
    retrieved = retrieve(query, k=k, where=where)
    prompt = build_prompt(query, retrieved)

    if prompt is None:
        return {
            "query":     query,
            "answer":    "제공된 자료에서는 관련 내용이 검색되지 않습니다.",
            "sources":   [],
            "distances": [],
        }

    answer = generate(prompt)
    return {
        "query":     query,
        "answer":    answer,
        "sources":   retrieved["ids"][0],
        "distances": retrieved["distances"][0],
    }


# =============================================================================
# 출력 보조
# =============================================================================
def print_rag_result(result: dict) -> None:
    """답변 + 출처를 한 화면에 보기 좋게 묶어 출력."""
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


def ask_rag_verbose(query: str, k: int = DEFAULT_K) -> None:
    """원본 청크까지 함께 표시하는 자세한 버전."""
    retrieved = retrieve(query, k=k)
    prompt = build_prompt(query, retrieved)
    if prompt is None:
        print(f"\n[질의] {query}")
        print("[답변] 관련 자료가 검색되지 않았습니다.")
        return
    answer = generate(prompt)

    print(f"\n[질의] {query}\n")
    print(f"[답변]\n{answer}\n")
    print("[참고 자료 원본]")
    for cid, doc, dist in zip(
        retrieved["ids"][0],
        retrieved["documents"][0],
        retrieved["distances"][0],
    ):
        print(f"\n  ⬩ {cid}  (거리 {dist:.3f})")
        print(f"    {doc[:200]}…")


# =============================================================================
# 데모 — 직접 실행 시 다섯 질의 시연
# =============================================================================
if __name__ == "__main__":
    DEMO_QUERIES = [
        "RAG가 환각을 줄이는 원리는?",
        "DPR과 BM25의 차이는?",
        "Active RAG는 일반 RAG와 무엇이 다른가?",
        "RAFT는 어떤 환경에 효과적인가?",
        "본서가 다루지 않는 주제 — 양자 컴퓨팅에 대해 알려 줘",  # 환각 방어 시험
    ]
    for q in DEMO_QUERIES:
        print_rag_result(ask_rag(q))
