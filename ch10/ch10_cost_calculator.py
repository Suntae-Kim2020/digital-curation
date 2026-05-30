# -*- coding: utf-8 -*-
r"""
ch10_cost_calculator.py — 자관 RAG 챗봇 월간 비용 추정기

『AI 레디 데이터와 디지털 큐레이션』 §10.3.1의 비용 추정 표를 코드로 옮긴 것.
요금은 공식 페이지에서 자주 갱신되므로 실 운영 시점에 RATES 값을 재확인한다.

사용:
  python ch10_cost_calculator.py

  또는 import해서:
    from ch10_cost_calculator import estimate
    breakdown = estimate(chunks=10_000, queries_per_day=100, days=30)
"""
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# =============================================================================
# 단가 (참고치, 2026-05 기준)
# 운영 시점 공식 페이지에서 재확인 권장:
# https://ai.google.dev/pricing
# =============================================================================
RATES = {
    "embedding_per_1m_tokens":   0.15,   # USD, 임베딩 호출
    "llm_input_per_1m_tokens":   0.30,   # USD, gemini-2.5-flash input
    "llm_output_per_1m_tokens":  2.50,   # USD, gemini-2.5-flash output
    "chromadb_monthly":          0.0,    # 로컬 운영 시 0
    "storage_per_gb_month":      0.0,    # 자관 서버 가정
}

# 기본 가정값
DEFAULT_TOKENS_PER_CHUNK     = 600    # 청크당 평균 토큰
DEFAULT_TOKENS_PER_QUERY     = 30     # 질의 본문
DEFAULT_TOKENS_PER_CONTEXT   = 1_800  # 컨텍스트 (청크 3개 평균)
DEFAULT_TOKENS_PER_ANSWER    = 250    # LLM 답변


# =============================================================================
# 추정 함수
# =============================================================================
def estimate(
    chunks: int,
    queries_per_day: int,
    days: int = 30,
    new_chunks_per_month: int = 0,
    *,
    tokens_per_chunk: int = DEFAULT_TOKENS_PER_CHUNK,
    tokens_per_query: int = DEFAULT_TOKENS_PER_QUERY,
    tokens_per_context: int = DEFAULT_TOKENS_PER_CONTEXT,
    tokens_per_answer: int = DEFAULT_TOKENS_PER_ANSWER,
) -> dict:
    """월간 운영 비용 추정 (USD).

    Parameters
    ----------
    chunks
        전체 청크 수 (1회성 임베딩 비용 계산용 — 첫 달에만 적용)
    queries_per_day
        일별 사용자 질의 수
    days
        월 기준 일 수 (기본 30)
    new_chunks_per_month
        매월 새로 추가되는 청크 수 (반복 임베딩 비용)
    """
    # 1) 임베딩 — 신규 청크에만 (첫 달의 chunks + 매월 new_chunks)
    embed_tokens_new = new_chunks_per_month * tokens_per_chunk
    embed_cost_monthly = (embed_tokens_new / 1_000_000) * RATES["embedding_per_1m_tokens"]

    # 첫 달 별도 (참고용)
    embed_tokens_initial = chunks * tokens_per_chunk
    embed_cost_initial = (embed_tokens_initial / 1_000_000) * RATES["embedding_per_1m_tokens"]

    # 2) LLM 입력 — 질의 + 컨텍스트
    total_queries = queries_per_day * days
    input_tokens = total_queries * (tokens_per_query + tokens_per_context)
    input_cost = (input_tokens / 1_000_000) * RATES["llm_input_per_1m_tokens"]

    # 3) LLM 출력 — 답변
    output_tokens = total_queries * tokens_per_answer
    output_cost = (output_tokens / 1_000_000) * RATES["llm_output_per_1m_tokens"]

    # 4) 질의별 임베딩 (검색용)
    query_embed_tokens = total_queries * tokens_per_query
    query_embed_cost = (query_embed_tokens / 1_000_000) * RATES["embedding_per_1m_tokens"]

    return {
        "embed_cost_initial":     embed_cost_initial,
        "embed_cost_monthly_new": embed_cost_monthly,
        "query_embed_cost":       query_embed_cost,
        "llm_input_cost":         input_cost,
        "llm_output_cost":        output_cost,
        "monthly_total":          embed_cost_monthly + query_embed_cost + input_cost + output_cost,
        "first_month_total":      embed_cost_initial + embed_cost_monthly + query_embed_cost + input_cost + output_cost,
        "queries_total":          total_queries,
        "tokens_total":           embed_tokens_initial + embed_tokens_new + input_tokens + output_tokens + query_embed_tokens,
    }


def print_breakdown(b: dict) -> None:
    print(f"  임베딩 (초기 적재, 첫 달):  ${b['embed_cost_initial']:>7.2f}")
    print(f"  임베딩 (월 신규 청크):      ${b['embed_cost_monthly_new']:>7.2f}")
    print(f"  임베딩 (질의 변환):         ${b['query_embed_cost']:>7.2f}")
    print(f"  LLM 입력 (질의+컨텍스트):   ${b['llm_input_cost']:>7.2f}")
    print(f"  LLM 출력 (답변):            ${b['llm_output_cost']:>7.2f}")
    print( "  " + "-" * 45)
    print(f"  월 운영 비용 (안정 상태):   ${b['monthly_total']:>7.2f}")
    print(f"  첫 달 비용 (초기 적재 포함):${b['first_month_total']:>7.2f}")
    print()
    print(f"  (참고) 월 질의 총수:        {b['queries_total']:>10,}")
    print(f"  (참고) 월 토큰 총소비:       {b['tokens_total']:>10,}")


# =============================================================================
# 데모 — 직접 실행 시 세 가지 시나리오
# =============================================================================
if __name__ == "__main__":
    scenarios = [
        ("[1] 소규모 자관 (학과 단위)",
         {"chunks": 1_000, "queries_per_day": 30, "new_chunks_per_month": 50}),
        ("[2] 중규모 자관 (대학도서관)",
         {"chunks": 10_000, "queries_per_day": 100, "new_chunks_per_month": 300}),
        ("[3] 대규모 자관 (국립기관)",
         {"chunks": 100_000, "queries_per_day": 500, "new_chunks_per_month": 2_000}),
    ]

    print("=" * 60)
    print(" 자관 RAG 챗봇 월간 비용 추정 (USD)")
    print(" 책 §10.3.1 — 단가 변동 가능, 운영 시점 재확인 필요")
    print("=" * 60)

    for name, params in scenarios:
        print(f"\n{name}")
        print(f"  청크 {params['chunks']:,}개 · 일 질의 {params['queries_per_day']}건 · "
              f"월 신규 청크 {params['new_chunks_per_month']}개")
        print()
        breakdown = estimate(**params)
        print_breakdown(breakdown)
