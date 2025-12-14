import streamlit as st
import time
import pandas as pd
from core.api_registry import APIRegistry
from core.schema import ResearchState
from core.graph import build_graph

# --- Page Config ---
st.set_page_config(page_title="DeepTrace Researcher", page_icon="🕵️‍♂️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stExpander"] { background-color: white; border: 1px solid #e5e7eb; border-radius: 8px; }
    .wizard-step { font-size: 1.2rem; font-weight: 600; color: #1f2937; margin-bottom: 20px; }
    
    /* New Summary Card Styles */
    .summary-card {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .summary-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .summary-value {
        font-size: 1.1rem;
        color: #0f172a;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- Helpers ---
def draw_card(label, value):
    st.markdown(f"""
    <div class='summary-card'>
        <div class='summary-label'>{label}</div>
        <div class='summary-value'>{value}</div>
    </div>
    """, unsafe_allow_html=True)

# --- Session State ---
if 'research_state' not in st.session_state: st.session_state.research_state = None
if 'graph_running' not in st.session_state: st.session_state.graph_running = False
if 'wizard_done' not in st.session_state: st.session_state.wizard_done = False
if 'config' not in st.session_state: st.session_state.config = {}

from tools.env_manager import load_from_env, save_to_env

# --- Security Functions ---
def persist_session():
    keys = APIRegistry._get_store()
    if not keys: return
    save_to_env(keys)
    st.success("Keys saved to .env (GitIgnored).")

def load_session():
    keys = load_from_env()
    if keys:
        for k, v in keys.items(): APIRegistry.register_key(k, v)
        st.toast("Restored API keys from .env", icon="🔐")

if 'loaded_session' not in st.session_state:
    load_session()
    st.session_state.loaded_session = True

def forget_session():
    # Clear session and overwrite .env with empty
    APIRegistry.clear_all()
    # Optional: We could delete .env or just empty it.
    save_to_env({}) 
    st.rerun()

# --- Main Layout ---
# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🔑 API Keys", expanded=False):
        # LLM Provider Selection
        st.caption("Core Model")
        llm_provider = st.selectbox("LLM Provider", ["OpenAI", "Anthropic", "OpenRouter"], index=0)
        APIRegistry.register_key("llm_provider", llm_provider)

        llm_model = ""
        if llm_provider == "OpenAI":
             llm_key = st.text_input("OpenAI API Key", type="password", value=APIRegistry.get_key("llm") or "")
             if llm_key: APIRegistry.register_key("llm", llm_key)
             llm_model = "gpt-4o" # Default
        
        elif llm_provider == "Anthropic":
             anth_key = st.text_input("Anthropic API Key", type="password", value=APIRegistry.get_key("anthropic_key") or "")
             if anth_key: APIRegistry.register_key("anthropic_key", anth_key)
             llm_model = "claude-3-5-sonnet-latest"

        elif llm_provider == "OpenRouter":
             or_key = st.text_input("OpenRouter API Key", type="password", value=APIRegistry.get_key("openrouter_key") or "")
             if or_key: APIRegistry.register_key("openrouter_key", or_key)
             llm_model = st.text_input("Model Name", value=APIRegistry.get_key("llm_model") or "anthropic/claude-3.5-sonnet")
             if llm_model: APIRegistry.register_key("llm_model", llm_model)

        # Search
        st.caption("Search Engine")
        search_key = st.text_input("Tavily API Key", type="password", value=APIRegistry.get_key("search") or "")
        if search_key: APIRegistry.register_key("search", search_key)

        st.caption("Domain Specific")
        # Perplexity
        pplx_key = st.text_input("Perplexity API Key", type="password", 
                               help="Leave blank to use OpenRouter Key instead.",
                               value=APIRegistry.get_key("perplexity") or "")
        if pplx_key: APIRegistry.register_key("perplexity", pplx_key)
        
        # Semantic Scholar
        ss_key = st.text_input("Semantic Scholar Key", type="password", value=APIRegistry.get_key("semanticscholar") or "")
        if ss_key: APIRegistry.register_key("semanticscholar", ss_key)
        
        # Community
        st.caption("Social")
        r_id = st.text_input("Reddit Client ID", type="password", value=APIRegistry.get_key("reddit_client_id") or "")
        if r_id: APIRegistry.register_key("reddit_client_id", r_id)
        r_sec = st.text_input("Reddit Secret", type="password", value=APIRegistry.get_key("reddit_client_secret") or "")
        if r_sec: APIRegistry.register_key("reddit_client_secret", r_sec)
        
        yt_key = st.text_input("YouTube API Key", type="password", value=APIRegistry.get_key("youtube_api_key") or "")
        if yt_key: APIRegistry.register_key("youtube_api_key", yt_key)
        
        gh_token = st.text_input("GitHub Token", type="password", value=APIRegistry.get_key("github_token") or "")
        if gh_token: APIRegistry.register_key("github_token", gh_token)

        if st.button("Save Keys"): persist_session()
        
    st.divider()
    
    st.subheader("📚 Research Discipline")
    domain = st.selectbox("Select Discipline", 
                          ["Scientific & Academic Research", "Financial Analysis", "Medical Research", "Product Comparison", "General Knowledge"],
                          index=0)
    
    # Map friendly names to internal keys
    domain_map = {
        "Scientific & Academic Research": "Academic",
        "Financial Analysis": "Finance",
        "Medical Research": "Medical",
        "Product Comparison": "Product/Tool Comparison",
        "General Knowledge": "General"
    }
    internal_domain = domain_map[domain]

    st.subheader("⚖️ Evaluation Mode")
    eval_mode_ui = st.selectbox("Mode", ["Standard", "Judge Mode (Critique)", "Debate Mode (Pro/Con)"])
    mode_map = {
        "Standard": "Standard",
        "Judge Mode (Critique)": "Judge",
        "Debate Mode (Pro/Con)": "Debate"
    }
    eval_mode = mode_map[eval_mode_ui]

# Main Content
st.title("🕵️‍♂️ Multi-Agent Deep Researcher")
st.markdown("#### Deep, multi-hop, multi-modal research with iterative reasoning.")

# Placeholder for Active Agents Banner
agent_status_container = st.empty()

# Input Layout
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### Research Query")
    question = st.text_area("Enter your complex research question here...", height=200, placeholder="e.g., Analyze the impact of GLP-1 agonists on global healthcare costs over the next decade.")

with c2:
    st.markdown("### Additional Context")
    uploaded_file = st.file_uploader("Upload Notes/Docs (PDF, md, txt)", type=['pdf', 'txt', 'md'])
    
    st.markdown("Or provide links:")
    arxiv_id = st.text_input("DOI or arXiv ID (Optional)")
    video_url = st.text_input("YouTube Video URL (Optional)")

# Dynamic Agent Detection
active_agents = []

# Core Logic
if APIRegistry.get_key("llm"): 
    active_agents.append("🧠 LLM Core")

if APIRegistry.get_key("search"):
    active_agents.append("🔍 Tavily Search")

# Domain Specific
if internal_domain == "Academic":
    active_agents.append("🎓 Arxiv") # Always on
    if APIRegistry.get_key("semanticscholar"): active_agents.append("📚 Semantic Scholar")
    
elif internal_domain == "Medical":
    active_agents.append("🏥 PubMed") # Always on
    active_agents.append("💊 ClinicalTrials") # Always on
    
elif internal_domain == "Finance":
    active_agents.append("📈 Yahoo Finance") # Mock/Basic
    if APIRegistry.get_key("perplexity") or APIRegistry.get_key("openrouter_key"): active_agents.append("🧠 Perplexity")
    
elif internal_domain == "Product/Tool Comparison":
    if APIRegistry.get_key("reddit_client_id"): active_agents.append("👽 Reddit")
    if APIRegistry.get_key("youtube_api_key"): active_agents.append("📺 YouTube Data")
    if APIRegistry.get_key("github_token"): active_agents.append("🐙 GitHub")

# RAG / Context
if uploaded_file or video_url:
    active_agents.append("📂 Context Analyzer")

if not active_agents:
    agent_status_container.warning("⚠️ No active agents detected. Please add API keys in the sidebar.")
else:
    agent_status_container.success(f"✅ Active Agents: {', '.join(active_agents)}")

# Action
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Start Deep Research", type="primary", use_container_width=True):
    # Enforce API Keys
    llm_provider = APIRegistry.get_key("llm_provider") or "OpenAI"
    has_valid_key = False
    
    if llm_provider == "OpenAI" and APIRegistry.get_key("llm"):
        has_valid_key = True
    elif llm_provider == "Anthropic" and APIRegistry.get_key("anthropic_key"):
        has_valid_key = True
    elif llm_provider == "OpenRouter" and APIRegistry.get_key("openrouter_key"):
        has_valid_key = True
        
    if not has_valid_key:
        st.error(f"⚠️ Critical Error: Missing API Key for **{llm_provider}**. Please configure it in the Sidebar.")
        st.stop()

    from tools.context_processing import process_context
    
    # Process Context
    with st.spinner("Processing context..."):
        context_data = process_context(uploaded_file, video_url)
        if arxiv_id: context_data += f"\n[User provided ID: {arxiv_id}]"

    # Build State
    initial_state = ResearchState(
        question=question if question else "Research",
        domain=internal_domain,
        evaluation_mode=eval_mode,
        context_data=context_data, # NEW
        demo_mode=False, # Forced off as requested
        research_objective="Deep Dive"
    )
    
    st.session_state.graph_running = True
    
    app = build_graph()
    
    st.divider()
    st.subheader("🔬 Research Plan Execution")
    
    with st.status("Initializing Agents...", expanded=True) as status:
        current_state = initial_state.model_dump()
        
        for output in app.stream(initial_state, config={"recursion_limit": 100}):
             for node_name, state_update in output.items():
                 if 'logs' in state_update:
                     for log in state_update['logs']:
                         status.write(f"**{log.agent_name}**: {log.message}")
                 current_state.update(state_update)
        
        status.update(label="Research Complete!", state="complete", expanded=False)
        st.session_state.research_state = current_state
        st.session_state.graph_running = False

# --- Results ---
if st.session_state.research_state:
    r = st.session_state.research_state # Dict
    
    tabs = ["📄 Report", "📚 Sources"]
    if r.get('judge_scorecard'): tabs.insert(1, "⚖️ Critique")
    if r.get('debate_transcript'): tabs.insert(1, "🗣️ Debate")
    
    st_tabs = st.tabs(tabs)
    
    # 1. Report
    with st_tabs[0]:
        st.markdown(r.get('templated_output') or r.get('report_md'))
        st.download_button("Download", r.get('templated_output') or r.get('report_md'), "report.md")

    # Dynamic Tabs
    idx = 1
    if r.get('debate_transcript'):
        with st_tabs[idx]:
            for turn in r['debate_transcript']:
                role = turn['role']
                is_pro = "Pro" in role
                with st.chat_message(role, avatar="🟢" if is_pro else "🔴"):
                    st.write(turn['content'])
        idx += 1
        
    if r.get('judge_scorecard'):
        with st_tabs[idx]:
            sc = r['judge_scorecard']
            c1, c2 = st.columns(2)
            c1.metric("Overall Score", f"{sc.get('overall_score')}/10")
            c2.write("**Requirements:**")
            c2.write(sc.get('required_fixes'))
            st.json(sc)
        idx += 1

    # Sources
    with st_tabs[idx]:
        st_sources = r.get('sources', [])
        if st_sources:
            df_data = []
            for s in st_sources:
                 if isinstance(s, dict):
                     title = s.get('title')
                     source = s.get('venue') or s.get('domain')
                     url = s.get('url')
                 else:
                     title = getattr(s, 'title', None)
                     source = getattr(s, 'venue', None) or getattr(s, 'domain', None)
                     url = getattr(s, 'url', None)
                 df_data.append({"Title": title, "Source": source, "URL": url})
            st.dataframe(df_data, use_container_width=True, column_config={"URL": st.column_config.LinkColumn()})
        else:
            st.write("No sources found.")
