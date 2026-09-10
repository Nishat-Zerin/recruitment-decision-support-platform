"""
AI-Assisted Recruitment Decision Support Platform - Demo Prototype
Run with: streamlit run app.py
"""

import streamlit as st
from groq import Groq
from data import (
    get_main_list,
    get_review_list,
    get_candidate_by_id,
    get_tracker_candidates,
    REVIEW_POLICY,
)

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(page_title="ScreenAI", layout="wide")

# Paste your Groq API key below (keep this file private / do not commit the key to GitHub)
GROQ_API_KEY = "PASTE_YOUR_GROQ_API_KEY_HERE"
MODEL_NAME = "openai/gpt-oss-20b"

# ----------------------------------------------------------------------------
# STYLING - loads the icon font + card/pill styling matching the wireframes
# ----------------------------------------------------------------------------
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tabler-icons/2.44.0/iconfont/tabler-icons.min.css">
<style>
.candidate-card {
    background-color: #151B2C;
    border: 1px solid #232B40;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 8px;
    color: #F1F5F9;
}
.candidate-card b { color: #F1F5F9; }
.reason-box {
    background-color: #1A2032;
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 13px;
    color: #9CA3AF !important;
    margin-top: 8px;
    display: flex;
    gap: 6px;
}
.reason-box span { color: #9CA3AF !important; }
.warning-banner {
    background-color: #2A2313;
    color: #FACC75 !important;
    border-radius: 10px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.warning-banner span { color: #FACC75 !important; }
.row-flex { display: flex; align-items: center; gap: 14px; }
.contact-line { font-size: 11px; color: #9CA3AF !important; display:flex; align-items:center; gap:6px; }
/* Force readable text on Streamlit's native widgets against the dark background */
.stTextInput input, .stTextArea textarea { color: #F1F5F9 !important; background-color: #1A2032 !important; }
.stTabs [data-baseweb="tab"] { color: #9CA3AF !important; }
.stTabs [aria-selected="true"] { color: #5EEAD4 !important; }
hr { border-color: #232B40 !important; }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# SCORE RING (SVG, matches the wireframe's circular progress indicator)
# ----------------------------------------------------------------------------
def score_ring_svg(percent, size=44):
    if percent is None:
        return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
            <circle cx="{size/2}" cy="{size/2}" r="{size/2-4}" fill="none" stroke="#232B40" stroke-width="4"/>
            <text x="{size/2}" y="{size/2+4}" text-anchor="middle" font-size="11" fill="#FACC75" font-weight="500">?</text>
            </svg>"""
    color = "#5EEAD4" if percent >= 85 else ("#FACC75" if percent >= 70 else "#A3E635")
    r = size / 2 - 4
    circumference = 2 * 3.14159 * r
    offset = circumference * (1 - percent / 100)
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
        <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="#232B40" stroke-width="4"/>
        <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" stroke-width="4"
                stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
                stroke-linecap="round" transform="rotate(-90 {size/2} {size/2})"/>
        <text x="{size/2}" y="{size/2+4}" text-anchor="middle" font-size="11" fill="{color}" font-weight="500">{percent}%</text>
        </svg>"""


# ----------------------------------------------------------------------------
# THE AGENTIC EXPLANATION WORKFLOW (the one real LLM call in the app)
# ----------------------------------------------------------------------------
def get_agentic_explanation(candidate):
    if not GROQ_API_KEY or GROQ_API_KEY == "PASTE_YOUR_GROQ_API_KEY_HERE":
        return {"error": "No Groq API key set. Paste your key into app.py (GROQ_API_KEY)."}

    confidence = candidate["extraction_confidence"]
    missing = candidate["missing_skills"]
    matched = candidate["matched_skills"]
    required = candidate["required_skills"]
    policy = REVIEW_POLICY

    grounded_facts = f"""
Candidate: {candidate['name']} - {candidate['title']}
Extraction confidence: {confidence}
Required skills: {', '.join(required)}
Matched skills: {', '.join(matched) if matched else 'none reliably extracted'}
Missing/unclear skills: {', '.join(missing) if missing else 'none'}
Relevant project note: {candidate['relevant_project']}
Routing policy: {policy}
"""
    prompt = f"""You are a recruitment assistant. Using ONLY the grounded facts below,
explain why this candidate is routed to their current segment and what the
recruiter should know. Do not invent facts not present below.

Format your answer as 3-4 short bullet points (each under 15 words, start each
line with "- "). No long paragraphs.

{grounded_facts}

End with a final bullet: "- Recommendation: Review" or "- Recommendation: Proceed".
"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_completion_tokens=700,
            reasoning_effort="low",
        )
        content = response.choices[0].message.content
        if not content:
            return {"error": "The model returned an empty response (ran out of reasoning budget). Try again."}
        return {"explanation": content}
    except Exception as e:
        return {"error": f"Groq API call failed: {e}"}


# ----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------------
st.sidebar.markdown("### ScreenAI")
page = st.sidebar.radio(
    "Navigate",
    ["New Screening", "Candidates", "Hiring Tracker"],
    label_visibility="collapsed",
)

# ----------------------------------------------------------------------------
# PAGE 1: NEW SCREENING
# ----------------------------------------------------------------------------
if page == "New Screening":
    st.title("New screening job")
    st.caption("Upload a job description and candidate CVs to generate ranked results.")
    st.text_area("Job description", placeholder="Paste JD text here...", height=120)
    st.file_uploader("Candidate CVs", accept_multiple_files=True, type=["pdf"])
    if st.button("Run screening", type="primary"):
        st.success("Screening complete (using pre-loaded mock data). Go to Candidates to view results.")

# ----------------------------------------------------------------------------
# PAGE 2: CANDIDATES
# ----------------------------------------------------------------------------
elif page == "Candidates":
    st.title("Candidates")
    search = st.text_input("Search skills, projects, past roles", "", label_visibility="collapsed",
                            placeholder="Search skills, projects, past roles")

    st.pills("Filters", ["Skills", "Experience", "Institution", "Previous employer", "Projects"],
             selection_mode="multi", default=["Skills"], label_visibility="collapsed")

    def matches_search(candidate, query):
        if not query:
            return True
        query = query.lower()
        haystack = " ".join(candidate["matched_skills"] + [candidate["relevant_project"], candidate["title"]]).lower()
        return query in haystack

    tab1, tab2 = st.tabs([f"Main list ({len(get_main_list())})", f"Needs manual review ({len(get_review_list())})"])

    if "explanations" not in st.session_state:
        st.session_state.explanations = {}
    if "explanation_visible" not in st.session_state:
        st.session_state.explanation_visible = {}

    with tab1:
        for c in get_main_list():
            if not matches_search(c, search):
                continue
            missing_txt = (f'Missing: {", ".join(c["missing_skills"])}. ') if c["missing_skills"] else ""
            ring = score_ring_svg(c["match_score"])
            st.markdown(
                '<div class="candidate-card"><div class="row-flex">'
                f'<div>{ring}</div>'
                '<div style="flex:1;">'
                f'<b>{c["name"]} - {c["title"]}</b>'
                f'<div class="reason-box"><i class="ti ti-message-circle"></i>'
                f'<span>Matched {len(c["matched_skills"])}/{len(c["required_skills"])} skills. '
                f'{missing_txt}{c["relevant_project"]}</span></div>'
                '</div></div></div>',
                unsafe_allow_html=True,
            )
            col1, col2, col3, col4 = st.columns([1.3, 1.3, 5, 1])
            with col1:
                is_visible = st.session_state.explanation_visible.get(c["id"], False)
                btn_label = "Hide explanation" if is_visible else "Why this rank?"
                if st.button(btn_label, key=f"why_{c['id']}"):
                    if c["id"] not in st.session_state.explanations:
                        with st.spinner("Running agentic explanation chain..."):
                            st.session_state.explanations[c["id"]] = get_agentic_explanation(c)
                        st.session_state.explanation_visible[c["id"]] = True
                    else:
                        st.session_state.explanation_visible[c["id"]] = not is_visible
                    st.rerun()
            with col2:
                st.button("Download CV", key=f"cv_{c['id']}", icon=":material/download:")
            with col4:
                with st.popover("⋮"):
                    st.button("Schedule interview", key=f"si_{c['id']}")
                    st.button("Reject", key=f"rj_{c['id']}")
                    st.button("Compare with others", key=f"cmp_{c['id']}")

            # Render the explanation full-width, below the button row (not inside a column)
            if st.session_state.explanation_visible.get(c["id"], False) and c["id"] in st.session_state.explanations:
                result = st.session_state.explanations[c["id"]]
                if "error" in result:
                    st.warning(result["error"])
                else:
                    formatted = result["explanation"].replace("\n", "<br>")
                    st.markdown(
                        f'<div class="candidate-card" style="border-color:#5EEAD4;">{formatted}</div>',
                        unsafe_allow_html=True,
                    )

    with tab2:
        st.markdown(
            '<div class="warning-banner"><i class="ti ti-alert-triangle"></i>'
            '<span>These CVs need manual review — low extraction confidence, not low quality.</span></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        for c in get_review_list():
            if not matches_search(c, search):
                continue
            ring = score_ring_svg(c["match_score"])
            st.markdown(
                '<div class="candidate-card"><div class="row-flex">'
                f'<div>{ring}</div>'
                '<div style="flex:1;">'
                f'<b>{c["name"]} - {c["title"]}</b>'
                f'<div class="reason-box"><i class="ti ti-message-circle"></i>'
                f'<span>{c["relevant_project"]}</span></div>'
                '</div></div></div>',
                unsafe_allow_html=True,
            )
            is_visible = st.session_state.explanation_visible.get(c["id"], False)
            btn_label = "Hide explanation" if is_visible else "Why does this need review?"
            if st.button(btn_label, key=f"whyrev_{c['id']}"):
                if c["id"] not in st.session_state.explanations:
                    with st.spinner("Running agentic explanation chain..."):
                        st.session_state.explanations[c["id"]] = get_agentic_explanation(c)
                    st.session_state.explanation_visible[c["id"]] = True
                else:
                    st.session_state.explanation_visible[c["id"]] = not is_visible
                st.rerun()

            if st.session_state.explanation_visible.get(c["id"], False) and c["id"] in st.session_state.explanations:
                result = st.session_state.explanations[c["id"]]
                if "error" in result:
                    st.warning(result["error"])
                else:
                    formatted = result["explanation"].replace("\n", "<br>")
                    st.markdown(
                        f'<div class="candidate-card" style="border-color:#FACC75;">{formatted}</div>',
                        unsafe_allow_html=True,
                    )

# ----------------------------------------------------------------------------
# PAGE 3: HIRING TRACKER
# ----------------------------------------------------------------------------
elif page == "Hiring Tracker":
    st.title("Hiring tracker")
    stages = get_tracker_candidates()
    col1, col2, col3 = st.columns(3)

    def render_stage(col, label, candidates):
        with col:
            st.markdown(f"**{label.upper()} &middot; {len(candidates)}**", unsafe_allow_html=True)
            for c in candidates:
                st.markdown(
                    '<div class="candidate-card">'
                    f'<b>{c["name"]}</b><br>'
                    f'<span style="font-size:12px;color:#9CA3AF;">'
                    f'{c["match_score"]}% match &middot; {c["applied_days_ago"]}d ago</span>'
                    '<hr style="border-color:#232B40;margin:8px 0;">'
                    f'<div class="contact-line"><i class="ti ti-phone"></i>{c["phone"]}</div>'
                    f'<div class="contact-line"><i class="ti ti-mail"></i>{c["email"]}</div>'
                    f'<div class="contact-line"><i class="ti ti-map-pin"></i>{c["address"]}</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                with st.popover("⋮ Options", use_container_width=True):
                    st.button("View original CV", key=f"tcv_{c['id']}")
                    st.button("Move back a stage", key=f"tmv_{c['id']}")

    render_stage(col1, "Shortlisted", stages["shortlisted"])
    render_stage(col2, "Interview", stages["interview"])
    render_stage(col3, "Hired", stages["hired"])
