"""
app.py
====================
Streamlit dashboard for the FMCG Consumer Sentiment & Review Intelligence
Agent. Calls the FastAPI backend (main.py, run via `uvicorn main:app`)
over HTTP -- does NOT import agent.py or analytics.py directly.

REQUIRES the FastAPI server running first

Then, in another terminal:
    streamlit run src/dashboard/app.py
"""

import os
os.environ.setdefault("LOG_FILE_NAME", "dashboard.log")

import sys
import time
import uuid
from datetime import date
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import streamlit.components.v1 as components

from src.config import constants
from src.utils.logger import get_logger

logger = get_logger(__name__)

API_BASE = constants.API_BASE_URL
COLOR_MAP = constants.SENTIMENT_COLOR_MAP

VIEW_DASHBOARD = "\U0001F4CA Dashboard"
VIEW_CHAT = "\U0001F4AC Chat"
VIEW_USAGE = "\U0001F9EE Model Usage"

st.set_page_config(
    page_title=constants.DASHBOARD_PAGE_TITLE,
    page_icon="\U0001F4CA",
    layout="wide",
)


st.markdown(
    """
    <style>
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1 {
        font-size: 1.35rem !important; margin: 0.6rem 0 0.3rem 0 !important; padding: 0 !important;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2 {
        font-size: 1.15rem !important; margin: 0.5rem 0 0.25rem 0 !important; padding: 0 !important;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h4 {
        font-size: 1.02rem !important; margin: 0.4rem 0 0.2rem 0 !important; padding: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


BACKEND_DOWN_MESSAGE = "Can't reach the API backend. Is `python main.py` running?"


def error_message_from(response_error):
    """Pulls the friendly message out of the backend's standard error
    envelope ({"success": false, "message": ...}); falls back to the raw
    error text."""
    response = getattr(response_error, "response", None)
    if response is not None:
        try:
            return response.json()["message"]
        except (ValueError, KeyError, TypeError):
            pass
    return f"API error: {response_error}"


@st.cache_data(ttl=constants.DASHBOARD_CACHE_TTL_SECONDS, show_spinner=False)
def _cached_get(path, params_key):
    """The actual HTTP call, cached on (path, params_key). Kept separate
    from api_get() because st.cache_data needs hashable arguments -- a dict
    isn't, so callers pass params as a sorted tuple of items instead."""
    params = dict(params_key) if params_key else None
    response = requests.get(f"{API_BASE}{path}", params=params,
                            timeout=constants.DASHBOARD_API_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()["data"]


def api_get(path, params=None):
    """Returns (data, error_message). error_message is None on success.
    Cached for DASHBOARD_CACHE_TTL_SECONDS so one page render (which calls
    this ~7 times) doesn't refire the same query, and rapid re-renders
    (e.g. dragging a date slider) don't hammer the backend."""
    params_key = tuple(sorted(params.items())) if params else None
    try:
        return _cached_get(path, params_key), None
    except requests.exceptions.ConnectionError:
        logger.error("Backend not reachable at %s", API_BASE)
        return None, BACKEND_DOWN_MESSAGE
    except requests.exceptions.RequestException as error:
        logger.error("GET %s failed: %s", path, error)
        return None, error_message_from(error)


def api_post(path, json_body, timeout=constants.CHAT_API_TIMEOUT_SECONDS, params=None):
    try:
        response = requests.post(
            f"{API_BASE}{path}", json=json_body, params=params, timeout=timeout
        )
        response.raise_for_status()
        return response.json()["data"], None
    except requests.exceptions.ConnectionError:
        logger.error("Backend not reachable at %s", API_BASE)
        return None, BACKEND_DOWN_MESSAGE
    except requests.exceptions.RequestException as error:
        logger.error("POST %s failed: %s", path, error)
        return None, error_message_from(error)



FALLBACK_MIN_DATE = constants.FALLBACK_MIN_DATE
FALLBACK_MAX_DATE = constants.FALLBACK_MAX_DATE


def get_date_bounds():
    """Returns (min_date, max_date, from_api). Cached in session_state once fetched."""
    cached = st.session_state.get("date_bounds")
    if cached:
        return cached
    data, err = api_get("/dashboard/date-range")
    if not err and data and data.get("min_date") and data.get("max_date"):
        bounds = (date.fromisoformat(data["min_date"]),
                  date.fromisoformat(data["max_date"]), True)
        st.session_state["date_bounds"] = bounds   # only cache real values
        return bounds
    return FALLBACK_MIN_DATE, FALLBACK_MAX_DATE, False


def render_generate_report_button():
    """Sidebar control that lets the user manually trigger one weekly
    brand-health report run (same code the scheduler/CLI script use) and
    view/download the result, instead of waiting for the schedule or
    running the script by hand."""
    st.sidebar.markdown("### \U0001F4C4 Weekly Report")
    generating = st.session_state.get("report_generating", False)
    if st.sidebar.button("Generate report now", width="stretch", disabled=generating):
        st.session_state["report_generating"] = True
        st.rerun()

    if generating:
        with st.sidebar:
            with st.spinner("Generating report..."):
                result, err = api_post("/dashboard/generate-report", {})
        st.session_state["report_generating"] = False
        if err:
            st.session_state["report_error"] = err
            st.session_state.pop("last_report", None)
        else:
            st.session_state["last_report"] = result
            st.session_state.pop("report_error", None)
        st.rerun()

    if st.session_state.get("report_error"):
        st.sidebar.error(st.session_state["report_error"])

    last_report = st.session_state.get("last_report")
    if last_report:
        st.sidebar.success(
            f"Report ready: {last_report['total_reviews']} reviews, "
            f"{last_report['start_date']} \u2192 {last_report['end_date']}"
        )
        st.sidebar.download_button(
            "Download Markdown",
            data=last_report["report_markdown"],
            file_name=f"weekly_report_{last_report['end_date']}.md",
            mime="text/markdown",
            width="stretch",
        )
        with st.sidebar.expander("Preview report"):
            st.markdown(last_report["report_markdown"])


def render_dashboard():
    st.sidebar.markdown("### :date: Dashboard Filters")

    aspects, err = api_get("/dashboard/aspects")
    if err:
        st.sidebar.warning(err)
        aspects = []

    min_d, max_d, bounds_from_api = get_date_bounds()
    date_help = (
        f"Only dates from {min_d:%d %b %Y} to {max_d:%d %b %Y} can be selected. "
        "The review dataset has no entries outside this window, so other "
        "dates are greyed out."
    )

    col1, col2 = st.sidebar.columns(2)
    start = col1.date_input("Start date", value=min_d, min_value=min_d,
                            max_value=max_d, help=date_help, key="start_date")
    end = col2.date_input("End date", value=max_d, min_value=min_d,
                          max_value=max_d, help=date_help, key="end_date")
    st.sidebar.caption(f"\U0001F4C5 Data available: {min_d:%d %b %Y} \u2013 {max_d:%d %b %Y}")
    if not bounds_from_api:
        st.sidebar.caption("\u26A0\uFE0F Using default date range (couldn't read it from the backend).")

    selected_aspect = st.sidebar.selectbox("Aspect", ["All"] + list(aspects))

    
    if isinstance(start, date) and isinstance(end, date) and start > end:
        st.toast("Start date is after the end date. Please pick a start date on or before the end date.",
                 icon="\u26A0\uFE0F")
        st.warning("Start date must be on or before the end date.")
        return

    
    params = {}
    if isinstance(start, date) and start != min_d:
        params["start_date"] = str(start)
    if isinstance(end, date) and end != max_d:
        params["end_date"] = str(end)
    if selected_aspect != "All":
        params["aspect"] = selected_aspect

    summary, err = api_get("/dashboard/summary", params)
    if err:
        st.error(err)
        return
    if not summary or summary.get("total_reviews", 0) == 0:
        st.warning("No reviews match the current filters.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reviews", f"{summary['total_reviews']:,}")
    c2.metric("Avg. Rating", f"{summary['avg_rating']:.2f} / 5")
    c3.metric("Negative %", f"{summary['negative_pct']:.1f}%")
    c4.metric("High-Severity (\u2265 3)", f"{summary['high_severity_count']}")

    st.markdown("---")
    col_left, col_right = st.columns([1, 2])

    trend, err = api_get("/dashboard/sentiment-trend", params)
    if err:
        st.error(err)
    elif trend:
        with col_left:
            st.subheader("Sentiment Split")
            split_df = pd.DataFrame(
                [{"sentiment": k, "count": v} for k, v in trend["split"].items()]
            )
            if not split_df.empty:
                fig = px.pie(split_df, names="sentiment", values="count",
                             color="sentiment", color_discrete_map=COLOR_MAP, hole=0.5)
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
                st.plotly_chart(fig, width="stretch")

        with col_right:
            st.subheader("Sentiment Trend Over Time")
            trend_df = pd.DataFrame(trend["trend"])
            if not trend_df.empty:
                fig = px.line(trend_df, x="month", y="count", color="sentiment",
                               color_discrete_map=COLOR_MAP, markers=True)
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300,
                                   xaxis_title="", yaxis_title="Reviews")
                st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    aspect_data, err = api_get("/dashboard/aspect-breakdown", params)
    if not err and aspect_data:
        with col_a:
            st.subheader("Aspect Breakdown")
            aspect_df = pd.DataFrame(aspect_data)
            if not aspect_df.empty:
                fig = px.bar(aspect_df, x="aspect", y="count", color="negative_pct",
                             color_continuous_scale="RdYlGn_r",
                             labels={"negative_pct": "Negative %"})
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, xaxis_title="")
                st.plotly_chart(fig, width="stretch")

    products, err = api_get("/dashboard/top-products", {**params, "limit": constants.DASHBOARD_TOP_PRODUCTS_LIMIT})
    if not err and products:
        with col_b:
            st.subheader("Most-Reviewed Products")
            prod_df = pd.DataFrame(products)
            if not prod_df.empty:
                fig = px.bar(prod_df.sort_values("reviews"), x="reviews", y="ProductName",
                             orientation="h", color="avg_score", color_continuous_scale="RdYlGn",
                             labels={"avg_score": "Avg Rating"})
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, yaxis_title="")
                st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("\U0001F6A9 Flagged Reviews!")
    search = st.text_input("Search flagged reviews (product or keyword)", "")
    flagged_params = {**params, "min_severity": constants.DEFAULT_MIN_SEVERITY}
    if search:
        flagged_params["search"] = search
    flagged, err = api_get("/dashboard/flagged-reviews", flagged_params)
    if err:
        st.error(err)
    elif not flagged:
        st.info("No high-severity reviews in the current filter range.")
    else:
        metadata, _meta_err = api_get("/dashboard/column-metadata")
        column_config = {
            column: st.column_config.Column(help=description)
            for column, description in (metadata or {}).items()
        }
        st.dataframe(pd.DataFrame(flagged), width="stretch", height=350,
                     column_config=column_config)
        if len(flagged) >= constants.DASHBOARD_FLAGGED_LIMIT:
            st.caption(
                f"Showing the {constants.DASHBOARD_FLAGGED_LIMIT} most severe matches. "
                "Narrow the filters or search to see the rest."
            )


USAGE_DAYS_KEY = "usage_days"


def render_usage():
    
    days = st.session_state.get(USAGE_DAYS_KEY, constants.USAGE_CHART_DAYS)

    usage, err = api_get("/dashboard/usage", {"days": days})
    if err:
        st.error(err)
        return
    if not usage or usage["total_calls"] == 0:
        st.info("No agent calls logged yet. Ask a question in the Chat tab, then come back here.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Questions Answered", f"{usage['total_calls']:,}")
    c2.metric("Total Tokens", f"{usage['total_tokens']:,}")
    c3.metric("Avg. Latency", f"{usage['avg_latency_ms']:,.0f} ms")
    if usage["cost_configured"]:
        c4.metric("Estimated Cost", f"${usage['estimated_cost_usd']:.4f}")
    else:
        c4.metric("Estimated Cost", "n/a")

    if not usage["cost_configured"]:
        st.caption(
            "Cost tracking isn't configured. Set COST_PER_1K_PROMPT_TOKENS and "
            "COST_PER_1K_COMPLETION_TOKENS in .env to your plan's rates to see "
            "an estimate here."
        )

    st.markdown("---")
    with st.container(border=True):
        st.slider(
            "Show last N days", min_value=1, max_value=90,
            value=constants.USAGE_CHART_DAYS, key=USAGE_DAYS_KEY,
            help=(
                "This slider changes the two charts below. "
                
            ),
        )

        col_left, col_right = st.columns(2)
        daily_df = pd.DataFrame(usage["daily"])

        with col_left:
            st.subheader("Tokens per Day")
            if daily_df.empty:
                st.info(f"No calls in the last {days} day(s).")
            else:
                fig = px.bar(daily_df, x="date", y="tokens")
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300,
                                   xaxis_title="", yaxis_title="Tokens")
                st.plotly_chart(fig, width="stretch")

        with col_right:
            st.subheader("Questions per Day")
            if daily_df.empty:
                st.info(f"No calls in the last {days} day(s).")
            else:
                fig = px.bar(daily_df, x="date", y="calls")
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300,
                                   xaxis_title="", yaxis_title="Questions")
                st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("Recent Calls")
    recent_df = pd.DataFrame(usage["recent_calls"])
    if not recent_df.empty:
        display_cols = [c for c in ["timestamp", "query", "tool_calls", "total_tokens",
                                    "latency_ms", "response_preview"] if c in recent_df.columns]
        st.dataframe(recent_df[display_cols], width="stretch", height=350)


with st.sidebar:
    st.markdown("### \U0001F4CA BrandEcho")
    st.markdown(
        "Hear what your customers are actually saying"
    )
    st.divider()

render_generate_report_button()
st.sidebar.divider()

st.title(constants.DASHBOARD_PAGE_TITLE)


view = st.radio(
    "View",
    [VIEW_DASHBOARD, VIEW_CHAT, VIEW_USAGE],
    horizontal=True,
    label_visibility="collapsed",
    key="view",
)

if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid.uuid4().hex   # one ID per browser session
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "pending" not in st.session_state:
    st.session_state["pending"] = None   
if "scroll_mode" not in st.session_state:
    st.session_state["scroll_mode"] = "bottom"


def scroll_chat(mode):
    """Scroll the page to the newest chat message.

    mode="bottom": newest message at the bottom of the screen (question + spinner).
    mode="answer": newest message starts at the top (read a long answer from line 1).

    Uses scrollIntoView on the last chat message, which scrolls whichever
    ancestor is the real scroll container -- no dependency on Streamlit's
    internal container names. It polls for ~1.8s because the message may not
    exist in the page yet when the script first runs.
    """
    js = """
    <script>
    // nonce: __NONCE__  (forces re-run on every Streamlit rerun)
    (function () {
      const doc = window.frameElement ? window.parent.document : document;
      const MODE = "__MODE__";
      let tries = 0;
      const timer = setInterval(function () {
        tries++;
        const msgs = doc.querySelectorAll('[data-testid="stChatMessage"]');
        const last = msgs[msgs.length - 1];
        if (last) {
          if (MODE === "answer") {
            last.style.scrollMarginTop = "80px";
            last.scrollIntoView({ block: "start" });
          } else {
            last.style.scrollMarginBottom = "130px";   // clear the pinned input box
            last.scrollIntoView({ block: "end" });
          }
        }
        if (tries === 1) console.log("[autoscroll]", MODE, "chat messages found:", msgs.length);
        if (tries >= 12) clearInterval(timer);
      }, 150);
    })();
    </script>
    """
    js = js.replace("__MODE__", mode).replace("__NONCE__", str(time.time()))
    try:
        
        st.html(js, unsafe_allow_javascript=True)
    except TypeError:
        
        components.html(js, height=0)


if view == VIEW_DASHBOARD:
    render_dashboard()

elif view == VIEW_USAGE:
    render_usage()

else:
    pending = st.session_state["pending"]

    st.markdown(
        "Analyze customer reviews instantly using conversational AI. "
        "Access real sentiment analytics, track high-severity escalations, "
        "and monitor brand-health performance with absolute fidelity to "
        "your underlying data."
    )

    col_spacer, col_clear = st.columns([5, 1])
    with col_clear:
        if st.button("Clear this chat", type="primary", width="stretch"):
            st.session_state["messages"] = []
            st.session_state["pending"] = None
            api_post(
                "/chat/history/clear", {},
                timeout=constants.DASHBOARD_API_TIMEOUT_SECONDS,
                params={"session_id": st.session_state["session_id"]},
            )
            st.rerun()

    example_questions = [
        "How did sentiment on packaging change in the year 2012?",
        "Show me the most severe flagged reviews right now.",
        "Give me a brand-health summary in Q1 2012.",
        "What do customers complain about regarding packaging? Give examples.",
        "Give me all of the reviews complaining about weird smell.",
    ]

    
    with st.expander("Try a question", expanded=not st.session_state["messages"]):
        for q in example_questions:
            if st.button(q, width="stretch", key=f"ex_{q}", disabled=bool(pending)):
                st.session_state["queued_question"] = q

    st.divider()

    
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    
    queued = st.session_state.pop("queued_question", None)
    user_input = st.chat_input("Ask about your reviews...", disabled=bool(pending))

    
    new_question = None if pending else (user_input or queued)
    if new_question:
        st.session_state["messages"].append({"role": "user", "content": new_question})
        st.session_state["pending"] = new_question
        st.session_state["scroll_mode"] = "bottom"
        st.rerun()

    
    if pending:
        scroll_chat("bottom")   
        with st.chat_message("assistant"):
            with st.spinner("Checking the reviews..."):
                result, err = api_post(
                    "/chat/ask",
                    {"question": pending, "session_id": st.session_state["session_id"]},
                )
                answer = f"Sorry, I ran into an error: {err}" if err else result["answer"]
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.session_state["pending"] = None
        st.session_state["scroll_mode"] = "answer"
        st.rerun()

    
    if st.session_state["messages"]:
        scroll_chat(st.session_state["scroll_mode"])

