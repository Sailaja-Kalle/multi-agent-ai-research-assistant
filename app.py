import streamlit as st
from agents import manager_agent
from report_generator import create_pdf

st.set_page_config(
    page_title="Multi-Agent AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
    background: linear-gradient(135deg, #e0f7ff, #b3ecff, #d4b8ff, #ffb3de);
}
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(90deg, #00d2ff, #ff6ec7, #a855f7, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
    .subtitle {
    text-align: center;
    color: #6b21a8;
        font-size: 16px;
        margin-bottom: 30px;
    }
    .stTextInput > div > div > input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        background: rgba(15, 10, 40, 0.9) !important;
        border: 2px solid #a855f7 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        opacity: 1 !important;
        caret-color: #00d2ff !important;
    }
    .stTextInput > div > div > input:focus {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(200, 180, 255, 0.6) !important;
        -webkit-text-fill-color: rgba(200, 180, 255, 0.6) !important;
    }
    div[data-baseweb="input"] {
        background: rgba(15, 10, 40, 0.9) !important;
        border-radius: 12px !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #a855f7, #ec4899);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 16px;
        font-weight: bold;
        padding: 12px 24px;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #00d2ff, #a855f7);
        transform: scale(1.05);
    }
    .stDownloadButton > button {
        background: linear-gradient(90deg, #fbbf24, #f97316) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    .log-card {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(139, 92, 246, 0.5);
    border-radius: 12px;
    padding: 12px 16px;
    margin: 6px 0;
    color: #1e1b4b !important;
    font-size: 14px;
    font-weight: 600;
}
    .report-container {
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(139, 92, 246, 0.4);
    border-radius: 16px;
    padding: 24px;
    color: #1e1b4b !important;
    line-height: 1.8;
    font-weight: 500;
}
    .agent-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid;
    }
    .agent-card-blue {
        border-color: #00d2ff;
        background: rgba(0, 210, 255, 0.1);
    }
    .agent-card-pink {
        border-color: #ec4899;
        background: rgba(236, 72, 153, 0.1);
    }
    .agent-card-purple {
        border-color: #a855f7;
        background: rgba(168, 85, 247, 0.1);
    }
    .stMarkdown p { color: #1e1b4b; }
h1, h2, h3 { color: #1e1b4b !important; }
    hr { border-color: rgba(168, 85, 247, 0.3); }
    .stStatus > div > button > div > p {
        color: #00d2ff !important;
        font-weight: bold !important;
    }
    .stStatus > div > button {
        background: rgba(0, 210, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    [data-testid="stStatusWidget"] p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">🔬 Multi-Agent AI Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">⚡ Powered by Groq Llama 70B + Tavily Search — 100% Free & Fast</div>', unsafe_allow_html=True)
st.divider()

# Input
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "question",
        placeholder="Example: What are latest developments in AI agents 2025?",
        label_visibility="collapsed"
    )
with col2:
    search_btn = st.button("🔍 Research Now", use_container_width=True)

st.divider()

# Session state
if "report" not in st.session_state:
    st.session_state.report = None
if "logs" not in st.session_state:
    st.session_state.logs = []

# Run agents
if search_btn and query:
    st.session_state.report = None
    st.session_state.logs = []

    with st.status("🤖 AI Agents working...", expanded=True) as status:
        st.write("⚡ Getting quick answer...")
        st.write("🔍 Research Agent searching the web...")
        st.write("⚖️ Judge Agent checking quality...")
        st.write("✍️ Writer Agent creating report...")

        report, logs = manager_agent(query)
        st.session_state.report = report
        st.session_state.logs = logs

        status.update(label="✅ Research Complete!", state="complete")

elif search_btn and not query:
    st.warning("⚠️ Please enter a research question!")

# Show logs
if st.session_state.logs:
    st.markdown("### 📊 Agent Activity Log")
    for log in st.session_state.logs:
        if "✅" in log:
            st.markdown(f'<div class="log-card" style="border-color:rgba(16,185,129,0.5);">{log}</div>', unsafe_allow_html=True)
        elif "⚖️" in log:
            st.markdown(f'<div class="log-card" style="border-color:rgba(251,191,36,0.5);">{log}</div>', unsafe_allow_html=True)
        elif "🔍" in log:
            st.markdown(f'<div class="log-card" style="border-color:rgba(0,210,255,0.5);">{log}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="log-card">{log}</div>', unsafe_allow_html=True)

# Show report
if st.session_state.report:
    st.divider()
    st.markdown("### 📋 Research Report")
    st.markdown(
        f'<div class="report-container">{st.session_state.report}</div>',
        unsafe_allow_html=True
    )
    st.divider()

    pdf_file = create_pdf(st.session_state.report)
    with open(pdf_file, "rb") as f:
        pdf_data = f.read()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_data,
            file_name="research_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:10px; background:rgba(168,85,247,0.15); border-radius:12px;">
        <span style="font-size:36px;">🔬</span>
        <h2 style="color:#a855f7 !important; margin:0; font-size:18px; text-shadow:0 0 10px rgba(168,85,247,0.5);">AI Research Assistant</h2>
        <p style="color:#c4b5fd !important; font-size:12px; margin-top:4px;">Multi-Agent System</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="agent-card agent-card-blue"><b style="color:#00d2ff;">🔍 Research Agent</b><br><small style="color:#94a3b8;">Searches web + scrapes content</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-card agent-card-pink"><b style="color:#ec4899;">⚖️ Judge Agent</b><br><small style="color:#94a3b8;">Scores quality 0.0 → 1.0</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-card agent-card-purple"><b style="color:#a855f7;">✍️ Writer Agent</b><br><small style="color:#94a3b8;">Writes professional report</small></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div style="color:#94a3b8; font-size:13px;">
        <b style="color:#fbbf24;">⚡ Built with:</b><br><br>
        🟣 Groq Llama 70B<br>
        🔵 Tavily Search API<br>
        🟡 Streamlit UI<br>
        🟢 BeautifulSoup Scraper<br>
        🔴 ReportLab PDF
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown('<div style="text-align:center; color:#6b7280; font-size:12px;">100% Free • No GPU needed</div>', unsafe_allow_html=True)