"""
Multimodal AI Design Analysis Suite - ULTIMATE FUTURISTIC EDITION
Multi-Agent System with LangGraph
Python Version: 3.12+
"""

import subprocess
import sys

def install_dependencies():
    """Install all required packages automatically"""
    print("🔧 Installing dependencies...")
    packages = ["streamlit", "langgraph", "langchain", "langchain-core", "openai", "pillow", "plotly", "python-dotenv", "pydantic"]
    for pkg in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
            print(f"✅ {pkg}")
        except:
            pass
    print("✅ Installation complete!\n")

install_dependencies()

import streamlit as st
from PIL import Image
import plotly.graph_objects as go
from datetime import datetime
import base64
from io import BytesIO

# Import our modules
from config import config, set_api_key, get_api_key
from graph.workflow import DesignAnalysisWorkflow
from utils.logger import setup_logger

# Setup logger
logger = setup_logger()

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON, layout="wide")

# ULTIMATE FUTURISTIC CSS
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');
* { font-family: 'Rajdhani', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0a0e27 100%); }
.stApp::before { content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(circle at 20% 50%, rgba(0,255,255,0.08) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(138,43,226,0.08) 0%, transparent 50%);
  animation: pulse 15s ease-in-out infinite; pointer-events: none; z-index: 0; }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.7; } }
.header-title { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; font-weight: 900;
  background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  animation: glow 3s ease-in-out infinite; letter-spacing: 3px; text-align: center;
  text-transform: uppercase; margin-bottom: 0.5rem; position: relative; z-index: 1; }
@keyframes glow { 0%,100% { text-shadow: 0 0 20px rgba(0,255,255,0.8); }
  50% { text-shadow: 0 0 40px rgba(0,255,255,1); } }
.subtitle { font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; color: #00ffff;
  text-align: center; margin-bottom: 2rem; text-shadow: 0 0 10px rgba(0,255,255,0.5);
  letter-spacing: 2px; position: relative; z-index: 1; }
.stButton>button { width: 100%; background: linear-gradient(135deg, #00ffff, #ff00ff);
  color: #000; border-radius: 0; padding: 1rem 2rem; font-weight: 700; font-size: 1.1rem;
  border: 2px solid #00ffff; font-family: 'Orbitron', sans-serif; text-transform: uppercase;
  letter-spacing: 2px; box-shadow: 0 0 20px rgba(0,255,255,0.5); transition: all 0.3s; }
.stButton>button:hover { transform: translateY(-3px);
  box-shadow: 0 0 30px rgba(255,0,255,1); border-color: #ff00ff; }
.agent-card { background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(138,43,226,0.1));
  padding: 2rem; border-radius: 15px; border: 2px solid rgba(0,255,255,0.3); margin: 1.5rem 0;
  backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0,255,255,0.2); transition: all 0.3s; }
.agent-card:hover { transform: translateY(-5px); border-color: rgba(255,0,255,0.5);
  box-shadow: 0 12px 40px rgba(0,255,255,0.4); }
.agent-card h3 { font-family: 'Orbitron', sans-serif; color: #00ffff; font-size: 1.5rem;
  margin-bottom: 1rem; text-shadow: 0 0 10px rgba(0,255,255,0.8); letter-spacing: 2px; }
.result-box { background: rgba(10,14,39,0.8); padding: 2rem; border-radius: 10px;
  border-left: 4px solid #00ffff; border-right: 4px solid #ff00ff; margin: 1rem 0;
  backdrop-filter: blur(5px); box-shadow: 0 4px 20px rgba(0,255,255,0.2); color: #b0e0ff;
  line-height: 1.8; font-size: 1.05rem; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0a0e27, #1a1f3a);
  border-right: 2px solid rgba(0,255,255,0.3); box-shadow: 5px 0 20px rgba(0,255,255,0.2); }
section[data-testid="stSidebar"] * { color: #00ffff !important; }
section[data-testid="stSidebar"] label { color: #00bfff !important; }
.stCheckbox:hover { background: rgba(0,255,255,0.1); border-left: 3px solid #00ffff;
  padding-left: 0.7rem; transition: all 0.3s; }
.category-header { font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: 600;
  color: #00ffff; margin-top: 1.5rem; margin-bottom: 1rem; text-transform: uppercase;
  letter-spacing: 2px; border-bottom: 2px solid rgba(0,255,255,0.3); padding-bottom: 0.5rem;
  text-shadow: 0 0 10px rgba(0,255,255,0.5); }
.stTextInput input, .stTextArea textarea { background: rgba(10,14,39,0.8) !important;
  border: 2px solid rgba(0,255,255,0.3) !important; color: #e0e0e0 !important;
  border-radius: 5px !important; transition: all 0.3s !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #00ffff !important;
  box-shadow: 0 0 15px rgba(0,255,255,0.5) !important; }
.stProgress > div > div { background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
  box-shadow: 0 0 20px rgba(0,255,255,0.8); }
.stat-card { background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(255,0,255,0.1));
  border: 2px solid rgba(0,255,255,0.3); border-radius: 10px; padding: 1.5rem; text-align: center;
  backdrop-filter: blur(10px); transition: all 0.3s; }
.stat-card:hover { transform: translateY(-5px); border-color: rgba(255,0,255,0.5);
  box-shadow: 0 10px 30px rgba(0,255,255,0.3); }
.stat-number { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 700;
  color: #00ffff; text-shadow: 0 0 15px rgba(0,255,255,0.8); }
.stat-label { font-size: 1rem; color: #00bfff; text-transform: uppercase; letter-spacing: 1px;
  margin-top: 0.5rem; }
img { border: 2px solid rgba(0,255,255,0.3); border-radius: 10px;
  box-shadow: 0 8px 30px rgba(0,255,255,0.2); }
#MainMenu, footer, header {visibility: hidden;}
::-webkit-scrollbar { width: 10px; background: rgba(10,14,39,0.8); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #00ffff, #ff00ff); border-radius: 5px; }
</style>""", unsafe_allow_html=True)

def image_to_base64(image):
    """Convert PIL Image to base64"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def create_gauge(score, title):
    """Create performance gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title, 'font': {'size': 16, 'color': '#00ffff', 'family': 'Orbitron'}},
        gauge={'axis': {'range': [0, 10], 'tickcolor': "#00ffff"},
               'bar': {'color': "#ff00ff"},
               'bgcolor': "rgba(0,0,0,0)",
               'bordercolor': "#00ffff",
               'steps': [{'range': [0, 5], 'color': 'rgba(255,0,0,0.2)'},
                        {'range': [5, 7], 'color': 'rgba(255,165,0,0.2)'},
                        {'range': [7, 10], 'color': 'rgba(0,255,0,0.2)'}]}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                     font={'color': "#00ffff", 'family': "Orbitron"}, height=220)
    return fig

def main():
    """Main application"""
    
    st.markdown('<h1 class="header-title">⚡ AI DESIGN INTELLIGENCE ⚡</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">MULTI-AGENT NEURAL NETWORK POWERED DESIGN ANALYSIS</p>', unsafe_allow_html=True)
    
    # API Key Configuration
    with st.sidebar:
        st.markdown("### 🔑 API CONFIGURATION")
        api_key = st.text_input("OpenRouter API Key", type="password",
                                value=get_api_key() or "",
                                help="Get key from https://openrouter.ai/")
        if api_key:
            set_api_key(api_key)
            st.success("✅ NEURAL LINK ESTABLISHED")
        else:
            st.warning("⚠️ API AUTHENTICATION REQUIRED")
            st.markdown("[🔗 Obtain Credentials](https://openrouter.ai/keys)")
    
    if not get_api_key():
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🎨 DESIGN AGENTS")
            st.markdown("• Brand Consistency\n• Aesthetic Quality")
        with col2:
            st.markdown("### 📊 BUSINESS AGENTS")
            st.markdown("• Conversion Optimization\n• Monetization Analysis")
        with col3:
            st.markdown("### 🔒 SECURITY AGENTS")
            st.markdown("• Privacy & Security\n• Ethical Design\n• Trend Analysis")
        return
    
    # Agent Selection
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🤖 SELECT AGENTS")
        
        st.markdown('<div class="category-header">DESIGN AGENTS</div>', unsafe_allow_html=True)
        agent_brand = st.checkbox("🏷️ Brand Consistency", True)
        agent_aesthetic = st.checkbox("✨ Aesthetic Quality", True)
        
        st.markdown('<div class="category-header">BUSINESS AGENTS</div>', unsafe_allow_html=True)
        agent_conversion = st.checkbox("💰 Conversion Optimization", True)
        agent_monetization = st.checkbox("💳 Monetization", False)
        
        st.markdown('<div class="category-header">SECURITY & COMPLIANCE</div>', unsafe_allow_html=True)
        agent_privacy = st.checkbox("🔒 Privacy & Security", False)
        agent_ethical = st.checkbox("⚖️ Ethical Design", False)
        agent_trends = st.checkbox("📈 Trend Analysis", True)
        
        st.markdown("---")
        total = sum([agent_brand, agent_aesthetic, agent_conversion, agent_monetization,
                    agent_privacy, agent_ethical, agent_trends])
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total}</div><div class="stat-label">AGENTS ACTIVE</div></div>', unsafe_allow_html=True)
    
    # Main Interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 UPLOAD DESIGN")
        st.markdown('<p style="color:#00bfff;font-size:0.9rem;margin-bottom:1rem;">Upload design mockup (PNG/JPG)</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Select Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        
        if uploaded:
            with st.spinner('⚡ Processing image...'):
                img = Image.open(uploaded)
            st.success("✅ Image loaded successfully!")
            st.image(img, caption="⚡ DESIGN LOADED", use_container_width=True)
            
            st.markdown("### 📝 DESIGN CONTEXT")
            context = st.text_area("Describe Your Design",
                placeholder="E.g., E-commerce product page targeting tech enthusiasts...",
                height=120, label_visibility="collapsed")
    
    with col2:
        st.markdown("### 🎯 ANALYSIS DASHBOARD")
        if not uploaded:
            st.markdown('<p style="color:#00bfff;font-size:0.9rem;">Upload a design to initiate neural analysis</p>', unsafe_allow_html=True)
        
        if uploaded:
            if st.button("⚡ INITIATE NEURAL SCAN", type="primary"):
                st.markdown("---")
                st.markdown('<p style="color:#00ffff;font-family:Orbitron;font-size:1.3rem;text-align:center;">🔄 MULTI-AGENT SYSTEM ACTIVATED...</p>', unsafe_allow_html=True)
                
                # Prepare agent list
                agent_map = {
                    "brand": agent_brand,
                    "aesthetic": agent_aesthetic,
                    "conversion": agent_conversion,
                    "monetization": agent_monetization,
                    "privacy": agent_privacy,
                    "ethical": agent_ethical,
                    "trends": agent_trends
                }
                
                selected = [k for k, v in agent_map.items() if v]
                
                if not selected:
                    st.warning("⚠️ SELECT AT LEAST ONE AGENT")
                else:
                    # Initialize workflow
                    workflow = DesignAnalysisWorkflow()
                    
                    # Convert image
                    img_base64 = image_to_base64(img)
                    
                    # Progress tracking
                    progress = st.progress(0)
                    status = st.empty()
                    
                    # Run analysis
                    try:
                        results = []
                        for idx, agent_type in enumerate(selected):
                            status.markdown(f'''<div style="background:rgba(0,255,255,0.1);padding:1rem;border-radius:10px;border:2px solid rgba(0,255,255,0.3);margin:1rem 0;">
                                <p style="color:#00ffff;font-family:Orbitron;font-size:1.2rem;text-align:center;">
                                🤖 AGENT: {agent_type.upper()}<br/>
                                <span style="font-size:0.9rem;color:#00bfff;">Progress: {idx+1} of {len(selected)}</span>
                                </p></div>''', unsafe_allow_html=True)
                            progress.progress((idx+1)/len(selected))
                            
                            # Run agent
                            result = workflow.run_agent(agent_type, img_base64, context if 'context' in locals() else "")
                            results.append(result)
                        
                        status.markdown('''<div style="background:rgba(0,255,0,0.15);padding:1.5rem;border-radius:10px;border:2px solid rgba(0,255,0,0.5);margin:1rem 0;">
                            <p style="color:#00ff00;font-family:Orbitron;font-size:1.8rem;text-align:center;">
                            ✅ ANALYSIS COMPLETE!<br/>
                            <span style="font-size:1rem;color:#00ffff;">All agents executed successfully</span>
                            </p></div>''', unsafe_allow_html=True)
                        progress.empty()
                        
                        # Calculate scores
                        scores = [r.get('score', 7.5) for r in results]
                        avg = sum(scores) / len(scores) if scores else 0
                        
                        # FULL WIDTH RESULTS
                        st.markdown("---")
                        st.markdown("### 📊 INTELLIGENCE DASHBOARD")
                        
                        cols = st.columns(4)
                        with cols[0]:
                            st.markdown(f'<div class="stat-card"><div class="stat-number">{len(selected)}</div><div class="stat-label">AGENTS</div></div>', unsafe_allow_html=True)
                        with cols[1]:
                            st.markdown(f'<div class="stat-card"><div class="stat-number">{avg:.1f}</div><div class="stat-label">AVG SCORE</div></div>', unsafe_allow_html=True)
                        with cols[2]:
                            status_txt = "EXCELLENT" if avg >= 7 else "GOOD" if avg >= 5 else "NEEDS WORK"
                            color = "#00ff00" if avg >= 7 else "#ffa500" if avg >= 5 else "#ff0000"
                            st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:{color};">{status_txt}</div><div class="stat-label">STATUS</div></div>', unsafe_allow_html=True)
                        with cols[3]:
                            st.markdown(f'<div class="stat-card"><div class="stat-number">{datetime.now().strftime("%H:%M")}</div><div class="stat-label">SCAN TIME</div></div>', unsafe_allow_html=True)
                        
                        st.markdown("### 📈 PERFORMANCE METRICS")
                        g_cols = st.columns(min(3, len(results)))
                        for idx, r in enumerate(results[:3]):
                            with g_cols[idx]:
                                st.plotly_chart(create_gauge(r.get('score', 7.5), r.get('agent', 'Agent')), use_container_width=True)
                        
                        st.markdown("---")
                        st.markdown("### 🤖 AGENT REPORTS")
                        
                        for r in results:
                            st.markdown(f'<div class="agent-card"><h3>{r.get("agent", "Agent")}</h3></div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="result-box">{r.get("analysis", "No analysis available")}</div>', unsafe_allow_html=True)
                        
                        st.markdown("---")
                        st.markdown("### 📥 EXPORT INTELLIGENCE REPORT")
                        
                        report = f"""# 🤖 AI DESIGN INTELLIGENCE REPORT
**Multi-Agent Analysis System**

**Context:** {context if 'context' in locals() else 'N/A'}
**Agents:** {len(selected)}
**Avg Score:** {avg:.1f}/10
**Timestamp:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""
                        for r in results:
                            report += f"""## {r.get('agent', 'Agent')}
**Score:** {r.get('score', 7.5)}/10

{r.get('analysis', 'No analysis')}

---

"""
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.download_button("📥 DOWNLOAD REPORT",
                                data=report,
                                file_name=f"Design_Intelligence_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown")
                        with c2:
                            st.markdown('<div style="padding:1rem;text-align:center;"><p style="color:#00ffff;font-family:Orbitron;">REPORT READY</p></div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"❌ Analysis Error: {str(e)}")
                        logger.error(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()