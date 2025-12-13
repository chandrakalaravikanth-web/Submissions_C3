# ⚡ AI Design Intelligence Suite

**Futuristic Multi-Agent Neural Network for Design Analysis**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B)
![LangGraph](https://img.shields.io/badge/AI-LangGraph-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A cutting-edge application that orchestrates a swarm of **7 specialized AI agents** to provide comprehensive analysis of UI/UX designs. Powered by **Claude 3.5 Sonnet** and **LangGraph**, it evaluates everything from aesthetic quality to ethical compliance in a futuristic Cyberpunk interface.

---

## 🌟 Features

### 🤖 The 7 Neural Agents
The system deploys seven distinct agents, each acting as a specialist:

1.  **🏷️ Brand Consistency Agent:** Evaluates alignment with brand values, color guidelines, and typography.
2.  **✨ Aesthetic Quality Agent:** Analyzes visual balance, harmony, modernity, and emotional impact.
3.  **💰 Conversion Optimization Agent:** Inspects CTA effectiveness, friction points, and trust signals.
4.  **💳 Monetization Agent:** Reviews ad intrusiveness, subscription flows, and pricing transparency.
5.  **🔒 Privacy & Security Agent:** Audits data transparency, GDPR compliance, and security patterns.
6.  **⚖️ Ethical Design Agent:** Detects dark patterns, manipulative UX, and inclusivity issues.
7.  **📈 Trend Analysis Agent:** Maps design against 2024-2025 industry trends and future-proofing.

### 🎨 Interface Highlights
* **Futuristic UI:** Custom CSS implementing a "Rajdhani" & "Orbitron" typography with neon aesthetics.
* **Real-time Dashboard:** Live processing updates and Plotly performance gauges.
* **Report Generation:** Automatic export of detailed Markdown reports.

---

## 🚀 Installation & Setup

**Prerequisites:** Python 3.12+ and an [OpenRouter API Key](https://openrouter.ai/).

### 1. Clone & Install Dependencies
Download the repository and install the required packages.

```bash
git clone <your-repo-url>
cd <your-repo-name>
pip install -r requirements.txt
2. ⚠️ Initialize Project Structure (CRITICAL STEP)
This project uses a self-generating architecture. You MUST run the setup script first to generate the agent files and folder structure.

Bash

python setup_project.py
This command creates the agents/, graph/, modules/, and utils/ directories and generates the necessary Python files.

3. Launch the Application
Run the Streamlit interface:

Bash

streamlit run app.py
⚙️ Configuration
API Key
You can enter your OpenRouter API Key directly in the application sidebar. Alternatively, create a .env file in the root directory:

Code snippet

OPENROUTER_API_KEY=sk-or-v1-your-key-here
Model Settings
The default model is configured in config.py:

Model: anthropic/claude-3.5-sonnet

Temperature: 0.7

Max Tokens: 2500

📂 Project Structure
After running setup_project.py, your directory will look like this:

Plaintext

├── agents/                 # Generated agent logic (brand, ethical, etc.)
├── graph/                  # LangGraph workflow orchestration
├── modules/                # LLM Factory and core modules
├── utils/                  # Logger and helpers
├── app.py                  # Main Streamlit application
├── config.py               # Configuration settings
├── setup_project.py        # System initialization script
└── requirements.txt        # Dependencies
🎯 Usage Guide
Authentication: Input your OpenRouter API key in the sidebar.

Agent Selection: Toggle specific agents on/off based on your needs (e.g., only "Design Agents" or "Security").

Upload: Drag and drop your UI mockup (PNG/JPG).

Context: Provide a brief description of the design (e.g., "E-commerce checkout flow for a luxury watch brand").

Scan: Click ⚡ INITIATE NEURAL SCAN.

Results: Review the scores, detailed feedback, and download the .md report.

📊 Scoring System
Each agent provides a score out of 10:

🟢 9-10 (Excellent): Industry leader, flawless execution.

🟡 7-8 (Good): Solid implementation, minor tweaks needed.

🟠 5-6 (Average): Functional but lacks polish or optimization.

🔴 < 5 (Critical): Significant issues requiring redesign.