# app.py
import streamlit as st
import json
import os
import datetime
import matplotlib.pyplot as plt
import io
from fpdf import FPDF

from agents.coordinator import Coordinator
from agents.llm_agent_cloud import LLMAgentCloud

st.set_page_config(page_title="Sleep Assistant", layout="wide")

# =====================================================================
#                               UI THEME
# =====================================================================
st.markdown(
    """
    <style>
        .stApp {
            background-color: #eef2f7;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3 {
            color: #0f172a;
            font-weight: 700;
        }

        .card {
            padding: 20px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .score-card {
            padding: 22px;
            border-radius: 15px;
            background: linear-gradient(135deg, #2563eb, #3b82f6, #60a5fa);
            color: white;
            text-align: center;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
            margin-bottom: 25px;
        }

        .score-value {
            font-size: 50px;
            font-weight: 900;
            margin-bottom: -5px;
        }

        .score-label {
            font-size: 20px;
            opacity: 0.95;
        }

        .info-card {
            padding: 18px;
            border-radius: 12px;
            background: #ffffff;
            border-left: 6px solid #38bdf8;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }

        .info-title {
            font-size: 22px;
            font-weight: 800;
        }

        .info-text {
            font-size: 16px;
            margin-top: 5px;
        }

        .center-btn {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================================
#                               HELPERS
# =====================================================================

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def sanitize_text(text):
    replacements = {
        "–": "-", "—": "-", "’": "'", "“": '"', "”": '"',
        "\u2013": "-", "\u2014": "-", "\u2019": "'",
        "\u201c": '"', "\u201d": '"'
    }
    for b, g in replacements.items():
        text = text.replace(b, g)
    return text

def save_json(report):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(DATA_DIR, f"report_{ts}.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return path

def generate_pdf(report):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, "Sleep Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, sanitize_text(f"Generated: {report['meta']['generated_at']}"), ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, "Metrics:", ln=True)
    for k, v in report["metrics"].items():
        pdf.cell(0, 7, sanitize_text(f" - {k}: {v}"), ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, "Recommendations:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, sanitize_text(report["recommendations"]))

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8,
        sanitize_text(f"Sleep Score: {report['score']['score']} ({report['score']['category']})"),
        ln=True
    )

    if "llm_summary" in report:
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, "AI Summary:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, sanitize_text(report.get("llm_summary", "")))

    return pdf.output(dest="S").encode("latin-1")

def plot_hr(hr_series):
    fig, ax = plt.subplots(figsize=(6, 2.2))
    ax.plot(hr_series, marker="o")
    ax.set_title("Heart Rate (Simulated)")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("BPM")
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def plot_hypnogram(stages):
    labels = ["W","N1","N2","N3","REM"]
    fig, ax = plt.subplots(figsize=(8, 1.6))
    ax.step(range(len(stages)), stages, where="post")
    ax.set_yticks([0,1,2,3,4])
    ax.set_yticklabels(labels)
    ax.set_title("Hypnogram (Simulated)")
    ax.set_xlabel("Epoch (30s)")
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


# -------------------------------------------------------------------
# Helper: Check API Key
# -------------------------------------------------------------------
def has_openai_key():
    """Check if OPENAI_API_KEY is set in system environment."""
    return os.getenv("OPENAI_API_KEY") is not None


# =====================================================================
#                             SIDEBAR
# =====================================================================
st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Home",
        "📊 Analysis",
        "🤖 AI Summary",
        "💬 Chat Coach",
        "📈 Charts",
        "💡 Recommendations",
        "🕒 History",
        "ℹ️ About"
    ]
)

# =====================================================================
#                                HOME
# =====================================================================
if menu == "🏠 Home":
    st.title("Welcome to Sleep Assistant 😴")
    st.markdown(
        """
        A smart multi-agent system that:

        ✔ Analyzes your sleep  
        ✔ Evaluates health parameters  
        ✔ Generates personalized recommendations  
        ✔ Produces charts & PDF reports  
        ✔ Tracks your sleep history  
        ✔ Uses Cloud LLM for AI Summary and Chat  

        Navigate using the sidebar.
        """
    )

# =====================================================================
#                               ANALYSIS
# =====================================================================
elif menu == "📊 Analysis":
    st.title("📊 Sleep Analysis")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Input Your Data")

    sleep_hours = st.number_input("Hours of Sleep", 0.0, 24.0, 7.0, 0.5)
    heart_rate = st.number_input("Average Heart Rate (BPM)", 30, 200, 72)
    stress_level = st.slider("Stress (1 to 10)", 1, 10, 3)

    st.markdown("<div class='center-btn'>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze Now", use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    if analyze_btn:

        if not has_openai_key():
            st.warning("⚠️ OpenAI API key not found. AI Summary and Chat will not work.")

        coordinator = Coordinator()
        try:
            sleep_res, health_res, advice, score, llm_summary, llm_trend = coordinator.process(
                sleep_hours, heart_rate, stress_level
            )
        except Exception as e:
            st.error(f"❌ Internal Error: {e}")
            sleep_res, health_res, advice, score = "Error", "Error", "Error", {"score": 0, "category": "Error"}
            llm_summary, llm_trend = "LLM failed", "LLM failed"

        import random
        epochs = max(4, int((sleep_hours * 60) / 30))
        hr_series = [int(max(35, heart_rate + random.randint(-6,6))) for _ in range(epochs)]
        stages = [random.choice([0,1,2,3,4]) for _ in range(epochs)]

        report = {
            "meta": {"generated_at": datetime.datetime.now().isoformat()},
            "metrics": {"sleep_analysis": sleep_res, "health_analysis": health_res},
            "recommendations": advice,
            "score": score,
            "hypnogram": stages,
            "hr_series": hr_series,
            "llm_summary": llm_summary,
            "llm_trend": llm_trend
        }

        save_json(report)

        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-value">{score['score']}</div>
                <div class="score-label">{score['category']} Sleep Quality</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">Sleep Analysis</div>
                <div class="info-text">{sleep_res}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">Health Analysis</div>
                <div class="info-text">{health_res}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🤖 AI Summary (Cloud LLM)")
        st.write(llm_summary)

        st.subheader("📈 AI 3-Day Trend Prediction")
        st.write(llm_trend)
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
#                           AI SUMMARY
# =====================================================================
elif menu == "🤖 AI Summary":
    st.title("🤖 AI-Generated Summary")

    files = sorted(os.listdir(DATA_DIR), reverse=True)
    if not files:
        st.warning("No reports found.")
    else:
        with open(os.path.join(DATA_DIR, files[0])) as f:
            report = json.load(f)

        st.subheader("Latest AI Summary")
        st.write(report.get("llm_summary", "No AI summary in last report."))

        st.subheader("AI Trend Prediction")
        st.write(report.get("llm_trend", "No trend prediction available."))

# =====================================================================
#                            CHAT COACH
# =====================================================================
elif menu == "💬 Chat Coach":
    st.title("💬 Chat with AI Sleep Coach")

    llm = LLMAgentCloud()

    if not has_openai_key():
        st.warning("⚠️ OpenAI API key missing. Chat will not work.")

    user_msg = st.text_input("Ask something about your sleep:")

    if st.button("Send") and user_msg.strip() != "":
        try:
            reply = llm.chat_with_user(user_msg)
        except Exception as e:
            reply = f"LLM Chat Error: {e}"

        st.write("### Coach:")
        st.write(reply)

# =====================================================================
#                               CHARTS
# =====================================================================
elif menu == "📈 Charts":
    st.title("📈 Sleep Charts")
    files = sorted(os.listdir(DATA_DIR), reverse=True)
    if not files:
        st.warning("No reports yet.")
    else:
        with open(os.path.join(DATA_DIR, files[0])) as f:
            report = json.load(f)

        st.subheader("Hypnogram")
        st.image(plot_hypnogram(report["hypnogram"]))

        st.subheader("Heart Rate")
        st.image(plot_hr(report["hr_series"]))

# =====================================================================
#                         RECOMMENDATIONS
# =====================================================================
elif menu == "💡 Recommendations":
    st.title("💡 Personalized Recommendations")
    files = sorted(os.listdir(DATA_DIR), reverse=True)
    if not files:
        st.warning("No reports yet.")
    else:
        with open(os.path.join(DATA_DIR, files[0])) as f:
            report = json.load(f)

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">Your Recommendations</div>
                <div class="info-text">{report["recommendations"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        pdf_bytes = generate_pdf(report)
        st.download_button("Download PDF Report", pdf_bytes, "sleep_report.pdf")

# =====================================================================
#                               HISTORY
# =====================================================================
elif menu == "🕒 History":
    st.title("🕒 Previous Reports")
    files = sorted(os.listdir(DATA_DIR), reverse=True)
    if not files:
        st.warning("No reports found.")
    else:
        for f in files:
            st.write(f)
            if st.button(f"Open {f}"):
                with open(os.path.join(DATA_DIR, f)) as fh:
                    st.json(json.load(fh))

# =====================================================================
#                                ABOUT
# =====================================================================
elif menu == "ℹ️ About":
    st.title("ℹ️ About This Project")
    st.markdown(
        """
        **Sleep Assistant Multi-Agent System**  
        B.Tech Final Year Project  

        Created using:
        - Python  
        - Streamlit  
        - Multi-Agent System  
        - Cloud LLM (OpenAI)  
        - Data Visualization  
        - ML-based Sleep Stages  
        - PDF Report Generation  

        Developer: **Sumit Barman**
        """
    )
