"""
search_reviews.py
====================
Tool 4: free-text semantic search over the review vector store (ChromaDB),
for fuzzy/meaning-based queries that don't map onto a structured field --
e.g. "are people complaining about a weird smell".

Complements, does NOT replace, the structured tools:
  - sentiment_trends / flagged_reviews / summary_report: exact, complete
    results over pandas -- right whenever "every matching row" matters.
  - search_reviews (this tool): approximate nearest-neighbor search over
    embeddings -- right for "find reviews about X" where X is a theme,
    symptom or complaint style rather than a tagged field.

A cosine-distance cutoff (constants.SEARCH_MAX_DISTANCE) drops weak
matches instead of always returning the top N regardless of relevance --
vector search always returns *something*, even when nothing in the store
is actually about the query.

What is in the vector store: one combined string per review
(Summary + ". " + Text), so results return a single `review_text` field.
"""

from datetime import datetime

from src.config import constants
from src.exceptions import InvalidInputError
from src.repositories.data_access import load_vectorstore
from src.schemas.request_schema import SearchReviewsRequest, validate_request
from src.utils.guardrails import flag_suspicious_reviews
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _date_to_epoch(date_str, arg_name):
    if not date_str:
        return None
    try:
        return int(datetime.fromisoformat(date_str).timestamp())
    except ValueError as error:
        raise InvalidInputError(f"Invalid {arg_name}: {date_str!r}. Use YYYY-MM-DD.") from error


def _build_where(aspect, sentiment, product_id, min_severity, start_date, end_date):
    clauses = []
    if aspect:
        clauses.append({"aspect": aspect})
    if sentiment:
        clauses.append({"sentiment": sentiment})
    if product_id:
        clauses.append({"product_id": product_id})
    if min_severity is not None:
        clauses.append({"severity": {"$gte": min_severity}})

    start_epoch = _date_to_epoch(start_date, "start_date")
    end_epoch = _date_to_epoch(end_date, "end_date")
    if start_epoch is not None:
        clauses.append({"time": {"$gte": start_epoch}})
    if end_epoch is not None:
        clauses.append({"time": {"$lte": end_epoch}})

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def _truncate(text):
    if len(text) <= constants.REVIEW_TEXT_MAX_CHARS:
        return text
    return text[:constants.REVIEW_TEXT_MAX_CHARS].rstrip() + "..."


def search_reviews(query, aspect=None, sentiment=None, min_severity=None,
                   product_id=None, product_name=None, start_date=None,
                   end_date=None, n_results=constants.SEARCH_DEFAULT_RESULTS):
    """
    Free-text semantic search over review content. Weak matches (cosine
    distance above constants.SEARCH_MAX_DISTANCE) are dropped rather than
    always returning n_results regardless of relevance.

    Use this when a question describes a theme, feeling or symptom that
    doesn't map to a fixed aspect/severity field -- e.g. "weird smell",
    "bottles arriving leaky". For exact aggregations or "every review where
    X" use sentiment_trends / flagged_reviews / summary_report instead.

    Args:
        query: natural-language description of what to search for.
        aspect / sentiment / product_id / min_severity: optional exact
            metadata filters, applied inside the vector search itself.
        product_name: case-insensitive substring match on product name,
            applied as a post-filter over a wider candidate pool. If several
            ProductIds match, a warning entry is prepended.
        start_date / end_date: ISO date strings. None = no bound.
        n_results: number of matches to return after filtering (max
            constants.MAX_SEARCH_RESULTS).

    Returns:
        List of review dicts ordered by relevance (best first), or
        [{"message": "..."}] if nothing matches or nothing is close enough.
    """
    request = validate_request(
        SearchReviewsRequest, query=query, aspect=aspect, sentiment=sentiment,
        min_severity=min_severity, product_id=product_id, product_name=product_name,
        start_date=start_date, end_date=end_date, n_results=n_results,
    )
    query, n_results, product_name = request.query, request.n_results, request.product_name

    collection = load_vectorstore()
    where = _build_where(
        request.aspect, request.sentiment, request.product_id,
        request.min_severity, request.start_date, request.end_date,
    )

    # Over-fetch when we still need to post-filter by product_name in Python
    # (Chroma metadata has no case-insensitive substring match), so the
    # final n_results is chosen from a wide enough candidate pool.
    fetch_n = n_results * 8 if product_name else n_results
    fetch_n = max(min(fetch_n, 100), n_results)

    query_kwargs = {"query_texts": [query], "n_results": fetch_n}
    if where:
        query_kwargs["where"] = where

    logger.info("search_reviews query=%r fetch_n=%s where=%s", query, fetch_n, where)
    raw = collection.query(**query_kwargs)

    if not raw["ids"][0]:
        return [{"message": "No reviews found matching this search and filters."}]

    rows = list(zip(
        raw["ids"][0], raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
    ))

    before_cutoff = len(rows)
    rows = [row for row in rows if row[3] <= constants.SEARCH_MAX_DISTANCE]
    if not rows:
        logger.info("search_reviews: all %s candidates were beyond the relevance cutoff (%.2f)",
                    before_cutoff, constants.SEARCH_MAX_DISTANCE)
        return [{"message": "No sufficiently relevant reviews found for this search. "
                            "Try a different phrasing, or widen the filters."}]

    warning = None
    if product_name:
        needle = product_name.lower()
        matched = [row for row in rows if needle in row[2]["product_name"].lower()]
        distinct_ids = {row[2]["product_id"] for row in matched}
        if len(distinct_ids) > 1:
            warning = (
                f"Note: '{product_name}' matches {len(distinct_ids)} different products "
                f"(ProductIds: {', '.join(sorted(distinct_ids))}). Results below combine "
                f"all of them. Ask by exact ProductId for a single specific product only."
            )
        rows = matched[:n_results]
    else:
        rows = rows[:n_results]

    if not rows:
        return [{"message": "No reviews found matching this search and filters."}]

    # Cast every value to a native Python type -- Chroma metadata can come
    # back as numpy.int64/float64, which the MCP JSON serializer rejects.
    results = [
        {
            "review_id": str(meta["review_id"]),
            "product_name": str(meta["product_name"]),
            "severity": int(meta["severity"]),
            "sentiment": str(meta["sentiment"]),
            "aspect": str(meta["aspect"]),
            "date": datetime.fromtimestamp(int(meta["time"])).strftime("%Y-%m-%d"),
            "review_text": _truncate(str(document)),
            "relevance_distance": round(float(distance), 4),
        }
        for _review_id, document, meta, distance in rows
    ]

    results = flag_suspicious_reviews(
        results, text_fields=("review_text",), context_query=f"semantic search: '{query}'"
    )

    if warning:
        results.insert(0, {"warning": warning})

    logger.info("search_reviews returned %s item(s)", len(results))
    return results
