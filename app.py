import streamlit as st
from google import genai
from PIL import Image
from pdf2image import convert_from_bytes
import io

# Initialize Gemini Client
client = genai.Client()

# Core Page Layout Configuration
st.set_page_config(
    page_title="MedBrief Pro — Smart Healthcare Assistant", 
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize single-page app router navigation state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Workspace"

# --- ADVANCED ULTRA-TRANSPARENT APPLE LIQUID GLASS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    /* Deep space fluid gradient background */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: -apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif !important;
        background: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 70%, #020617 100%) !important;
    }
    
    header, [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Liquid Frosted Glass Navigation Bar */
    .apple-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px;
        padding: 10px 24px;
        margin-bottom: 30px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Regulatory Notice Banner */
    .apple-disclaimer {
        background: rgba(255, 69, 58, 0.04) !important;
        backdrop-filter: blur(30px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(200%) !important;
        border: 1px solid rgba(255, 69, 58, 0.12) !important;
        border-radius: 16px;
        padding: 14px 20px;
        margin-bottom: 25px;
    }
    
    /* Typography Logic */
    .apple-title {
        font-size: clamp(2.0rem, 4.5vw, 3.0rem) !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px !important;
    }
    
    .apple-subtitle {
        font-size: clamp(0.95rem, 2vw, 1.15rem) !important;
        color: #94a3b8;
        font-weight: 400;
        letter-spacing: -0.01em;
        margin-bottom: 35px !important;
    }
    
    /* Cards and Feature Blocks */
    div[data-testid="stFileUploader"], .liquid-glass-card, .output-pane, .info-feature-card {
        background: rgba(255, 255, 255, 0.01) !important;
        backdrop-filter: blur(35px) saturate(210%) !important;
        -webkit-backdrop-filter: blur(35px) saturate(210%) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3), 
                    inset 0 1px 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
        padding: 24px;
    }
    
    /* Interactive States */
    div[data-testid="stFileUploader"]:hover, .liquid-glass-card:hover, .output-pane:hover, .info-feature-card:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 20px 50px 0 rgba(0, 0, 0, 0.4), 
                    inset 0 1px 2px 0 rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-4px);
    }
    
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    div[data-testid="stMarkdownText"] p {
        color: #cbd5e1 !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- 1. WEB APP TOP NAVIGATION BAR ---
nav_col1, nav_col2 = st.columns([2, 1])
with nav_col1:
    st.markdown("<p style='font-weight:700; font-size:1.2rem; color:#fff; margin:0; padding-top:4px;'>🍏 MedBrief <span style='font-weight:300; color:#64748b;'>Pro</span></p>", unsafe_allow_html=True)
with nav_col2:
    # Use clean button design structures side-by-side to act as navigation switches
    btn_space1, btn_space2 = st.columns(2)
    with btn_space1:
        if st.button("💻 Workspace", use_container_width=True, type="secondary" if st.session_state.current_page == "About" else "primary"):
            st.session_state.current_page = "Workspace"
            st.rerun()
    with btn_space2:
        if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.current_page == "About" else "secondary"):
            st.session_state.current_page = "About"
            st.rerun()

st.markdown("<hr style='margin-top:0; margin-bottom:25px; opacity:0.1;'>", unsafe_allow_html=True)


# --- 2. RENDER VIEWPORT: WORKSPACE PAGE ---
if st.session_state.current_page == "Workspace":
    
    # Regulatory Card
    st.markdown(
        """
        <div class="apple-disclaimer">
            <span style="color:#FF453A; font-weight:600; font-size:1rem; letter-spacing:-0.01em;">⚠️ Regulatory Notice & Medical Reference Disclaimer</span>
            <p style="margin-top: 4px; font-size:0.85rem; color:#ff9f0a; margin-bottom:0; opacity:0.9;">
                <b>Automated Context Architecture:</b> For administrative organization workflows. This portal does not issue diagnostics or medical evaluations. Verify all output elements directly against certified source records.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="apple-title">AI-Based Smart Healthcare Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="apple-subtitle">Unstructured clinical data. Structured medical clarity. Instantly.</p>', unsafe_allow_html=True)

    PROMPTS = {
        "Hospital Report": "You are an expert medical administrator. Analyze the provided document images and provide a structured summary with Patient Info, Primary Diagnosis, Test Results, Procedures, and Follow-up Instructions.",
        "Receipt / Invoice": "You are a medical billing expert. Analyze the provided document images and provide a structured breakdown of Billing Party, Patient Details, Itemized Charges, and Financial Summaries.",
        "Prescription": "You are a clinical pharmacist. Analyze the provided document images and extract the medication plan carefully including Name, Dosage, Frequency, Duration, and Special Warnings."
    }

    # Control Deck Row
    control_deck = st.container()
    with control_deck:
        col_select, col_dropzone = st.columns([1, 2], gap="large")
        
        with col_select:
            st.markdown("<p style='color:#94a3b8; font-size:0.85rem; font-weight: 500; margin-bottom:6px;'>1. SELECT WORKFLOW</p>", unsafe_allow_html=True)
            doc_type = st.selectbox("Select Document Type", list(PROMPTS.keys()), label_visibility="collapsed")

        with col_dropzone:
            st.markdown("<p style='color:#94a3b8; font-size:0.85rem; font-weight: 500; margin-bottom:6px;'>2. DROP PAPERS</p>", unsafe_allow_html=True)
            uploaded_files = st.file_uploader("Drag & Drop Files Here", type=["pdf", "png", "jpg", "jpeg", "webp"], accept_multiple_files=True, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Content File Processing Workspace
    if uploaded_files:
        pages_to_process = []
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                try:
                    with st.spinner("Decoding document frames..."):
                        pages_to_process.extend(convert_from_bytes(uploaded_file.read()))
                except Exception as e:
                    st.error(f"Failed decoding PDF ({uploaded_file.name}): {e}")
            else:
                try:
                    pages_to_process.append(Image.open(uploaded_file))
                except Exception as e:
                    st.error(f"Failed decoding image asset ({uploaded_file.name}): {e}")

        if pages_to_process:
            canvas_left, canvas_right = st.columns([1, 1], gap="large")
            
            with canvas_left:
                st.markdown(f"<h3 style='font-size:1.3rem; margin-bottom:15px; font-weight:500;'>Source Matrix <span style='color:#64748b;'>({len(pages_to_process)})</span></h3>", unsafe_allow_html=True)
                for idx, page_img in enumerate(pages_to_process):
                    st.markdown('<div class="liquid-glass-card" style="margin-bottom:15px;">', unsafe_allow_html=True)
                    st.image(page_img, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with canvas_right:
                st.markdown("<h3 style='font-size:1.3rem; margin-bottom:15px; font-weight:500;'>Synthesized Insights</h3>", unsafe_allow_html=True)
                st.markdown('<div class="output-pane">', unsafe_allow_html=True)
                with st.spinner("Synthesizing records..."):
                    try:
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=[PROMPTS[doc_type]] + pages_to_process)
                        st.markdown("<span style='color:#34c759; font-size:0.85rem; font-weight:600; letter-spacing:0.05em;'>✓ ANALYSIS FINALIZED</span>", unsafe_allow_html=True)
                        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.toast("Analysis complete.", icon="🍏")
                    except Exception as e:
                        st.error(f"Inference pipeline execution error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)


# --- 3. RENDER VIEWPORT: ABOUT PAGE ---
elif st.session_state.current_page == "About":
    st.markdown('<h1 class="apple-title">About the Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="apple-subtitle">Behind the architecture of MedBrief Pro.</p>', unsafe_allow_html=True)
    
    # Feature grid display using clean glass card columns
    col_feat1, col_feat2, col_feat3 = st.columns(3, gap="medium")
    
    with col_feat1:
        st.markdown("""
        <div class="info-feature-card">
            <h4 style="color:#007aff; margin-bottom:10px;">👁️ Multimodal Vision OCR</h4>
            <p style="font-size:0.9rem; line-height:1.5; color:#94a3b8;">
                Instead of processing fragile text streams, the platform vectorizes the absolute visual layout of reports, prescriptions, and scans. This ensures accurate reads of bad lighting, slanted photos, and complex tables.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_feat2:
        st.markdown("""
        <div class="info-feature-card">
            <h4 style="color:#34c759; margin-bottom:10px;">⚡ Local Processing Arrays</h4>
            <p style="font-size:0.9rem; line-height:1.5; color:#94a3b8;">
                Utilizes system-native memory buffering to transform multiple file variations chronologically. Drop PDFs, JPGs, and PNGs together—the engine parses them smoothly in a unified session.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_feat3:
        st.markdown("""
        <div class="info-feature-card">
            <h4 style="color:#af52de; margin-bottom:10px;">🧠 Context Synthesis</h4>
            <p style="font-size:0.9rem; line-height:1.5; color:#94a3b8;">
                Backed by foundational medical administrative parsing prompts, the application automatically isolates noise, bills, and unrelated numbers to structure only verified follow-ups and dosages.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Architecture Stack Details")
    
    # Deep Information layout
    st.markdown("""
    * **Frontend UI Engine:** Streamlit Framework with inline CSS glassmorphism injections.
    * **Core Intelligence Layer:** Google Gemini 2.5 Multimodal Foundation APIs.
    * **Vector Imaging Compiler:** `pdf2image` paired with Poppler System Binaries for rendering.
    """)