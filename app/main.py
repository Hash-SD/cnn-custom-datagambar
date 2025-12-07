"""
ATK Classifier - Eye-Catching & User-Friendly Interface
Menerapkan prinsip psikologi pengguna: Hick's Law, Gestalt, Doherty Threshold
"""
import streamlit as st
from PIL import Image
from pathlib import Path

from app.config import settings
from app.components.predictor import PredictionEngine


# Page configuration - HARUS di baris pertama
st.set_page_config(
    page_title="Deteksi Alat Tulis Pintar",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def inject_custom_css():
    """Inject CSS untuk UI yang bersih, eye-catching, dan responsive."""
    st.markdown("""
    <style>
        /* Hide Streamlit branding untuk tampilan profesional */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main container styling */
        .main {
            background: linear-gradient(180deg, #FAFBFC 0%, #F0F4F8 100%);
        }
        
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 1200px;
        }
        
        /* ============ RESPONSIVE HERO SECTION ============ */
        .hero-container {
            text-align: center;
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #0083B8 0%, #00B4DB 50%, #48C6EF 100%);
            border-radius: 16px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 40px rgba(0, 131, 184, 0.3);
        }
        
        .hero-title {
            font-size: clamp(1.5rem, 5vw, 2.8rem);
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            line-height: 1.2;
        }
        
        .hero-subtitle {
            font-size: clamp(0.9rem, 2.5vw, 1.2rem);
            opacity: 0.95;
            margin-top: 0.8rem;
            font-weight: 300;
            line-height: 1.4;
        }
        
        /* ============ RESPONSIVE UPLOAD CARD ============ */
        .upload-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 2px dashed #E2E8F0;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .upload-card:hover {
            border-color: #0083B8;
            box-shadow: 0 8px 30px rgba(0, 131, 184, 0.15);
        }
        
        /* ============ RESPONSIVE RESULT CARD ============ */
        .result-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem 1rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .result-success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem 1rem;
            text-align: center;
            box-shadow: 0 8px 30px rgba(17, 153, 142, 0.3);
        }
        
        .result-success div:first-child {
            font-size: clamp(2.5rem, 8vw, 4rem);
        }
        
        .result-success div:nth-child(2) {
            font-size: clamp(1.3rem, 4vw, 2rem) !important;
        }
        
        .result-success div:nth-child(3) {
            font-size: clamp(1rem, 3vw, 1.3rem) !important;
        }
        
        .result-warning {
            background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem 1rem;
            text-align: center;
        }
        
        .result-warning div:first-child {
            font-size: clamp(2.5rem, 8vw, 4rem);
        }
        
        .result-warning div:nth-child(2) {
            font-size: clamp(1.3rem, 4vw, 2rem) !important;
        }
        
        .result-warning div:nth-child(3) {
            font-size: clamp(1rem, 3vw, 1.3rem) !important;
        }
        
        /* ============ RESPONSIVE CATEGORY CARDS ============ */
        .category-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            min-height: 100px;
        }
        
        .category-card:hover {
            border-color: #0083B8;
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0, 131, 184, 0.2);
        }
        
        .category-emoji {
            font-size: clamp(2rem, 6vw, 3rem);
            margin-bottom: 0.3rem;
        }
        
        .category-title {
            font-size: clamp(0.9rem, 2.5vw, 1.2rem);
            font-weight: 700;
            color: #1A202C;
            margin: 0.3rem 0 0.2rem 0;
        }
        
        .category-subtitle {
            font-size: clamp(0.75rem, 2vw, 0.9rem);
            color: #718096;
        }
        
        /* ============ RESPONSIVE BUTTONS ============ */
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            height: auto;
            min-height: 2.8em;
            padding: 0.6rem 1rem;
            font-weight: 600;
            font-size: clamp(0.85rem, 2.5vw, 1rem);
            background: linear-gradient(135deg, #0083B8 0%, #00B4DB 100%);
            color: white;
            border: none;
            box-shadow: 0 4px 15px rgba(0, 131, 184, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 131, 184, 0.4);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* ============ FILE UPLOADER RESPONSIVE ============ */
        .stFileUploader > div > div {
            border-radius: 10px;
        }
        
        .stFileUploader label {
            font-size: clamp(0.85rem, 2.5vw, 1rem) !important;
        }
        
        /* ============ PROGRESS BAR ============ */
        .stProgress > div > div {
            background: linear-gradient(90deg, #0083B8 0%, #00B4DB 100%);
            border-radius: 10px;
        }
        
        /* ============ RESPONSIVE METRICS ============ */
        [data-testid="stMetricValue"] {
            font-size: clamp(1.2rem, 4vw, 2rem);
            font-weight: 700;
            color: #0083B8;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: clamp(0.75rem, 2vw, 0.9rem);
        }
        
        /* ============ ALERTS ============ */
        .stAlert {
            border-radius: 10px;
            font-size: clamp(0.85rem, 2.5vw, 1rem);
        }
        
        /* ============ RESPONSIVE TABS ============ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            flex-wrap: wrap;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 8px 12px;
            font-size: clamp(0.8rem, 2.5vw, 1rem);
        }
        
        /* ============ CONFIDENCE BAR ============ */
        .confidence-bar {
            background: #E2E8F0;
            border-radius: 8px;
            height: 10px;
            overflow: hidden;
            margin: 0.4rem 0;
        }
        
        .confidence-fill {
            height: 100%;
            border-radius: 8px;
            transition: width 0.5s ease;
        }
        
        .confidence-high {
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        }
        
        .confidence-medium {
            background: linear-gradient(90deg, #f39c12 0%, #f1c40f 100%);
        }
        
        .confidence-low {
            background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
        }
        
        /* ============ RESPONSIVE FUN FACT CARD ============ */
        .fun-fact-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 0.8rem 1rem;
            margin-top: 1rem;
            font-size: clamp(0.8rem, 2.5vw, 0.95rem);
            line-height: 1.4;
        }
        
        /* ============ RESPONSIVE FOOTER ============ */
        .footer {
            text-align: center;
            color: #718096;
            font-size: clamp(0.75rem, 2vw, 0.85rem);
            padding: 1.5rem 0 1rem 0;
            margin-top: 1.5rem;
            border-top: 1px solid #E2E8F0;
        }
        
        .footer a {
            color: #0083B8;
            text-decoration: none;
        }
        
        /* ============ RESPONSIVE WAITING STATE ============ */
        .waiting-state {
            text-align: center;
            padding: 2rem 1rem;
            color: #718096;
        }
        
        .waiting-icon {
            font-size: clamp(2.5rem, 8vw, 4rem);
            margin-bottom: 0.8rem;
            opacity: 0.5;
        }
        
        .waiting-state p {
            font-size: clamp(0.85rem, 2.5vw, 1rem);
            margin: 0.3rem 0;
        }
        
        /* ============ RESPONSIVE STEP INDICATOR ============ */
        .step-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.8rem;
            flex-wrap: wrap;
        }
        
        .step-number {
            background: #0083B8;
            color: white;
            width: clamp(24px, 5vw, 28px);
            height: clamp(24px, 5vw, 28px);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: clamp(0.75rem, 2vw, 0.9rem);
            flex-shrink: 0;
        }
        
        .step-text {
            font-weight: 600;
            color: #1A202C;
            font-size: clamp(0.9rem, 2.5vw, 1rem);
        }
        
        /* ============ MOBILE SPECIFIC (< 768px) ============ */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            
            .hero-container {
                padding: 1.5rem 0.8rem;
                border-radius: 12px;
                margin-bottom: 1rem;
            }
            
            .category-card {
                padding: 0.8rem 0.5rem;
                min-height: 80px;
            }
            
            .upload-card {
                padding: 1rem 0.8rem;
            }
            
            .result-card, .result-success, .result-warning {
                padding: 1.2rem 0.8rem;
            }
            
            .fun-fact-card {
                padding: 0.7rem 0.8rem;
            }
            
            /* Stack columns on mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        
        /* ============ SMALL MOBILE (< 480px) ============ */
        @media (max-width: 480px) {
            .hero-container {
                padding: 1.2rem 0.6rem;
                margin-bottom: 0.8rem;
            }
            
            .category-card {
                padding: 0.6rem 0.4rem;
                min-height: 70px;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 6px 10px;
            }
        }
        
        /* ============ TABLET (768px - 1024px) ============ */
        @media (min-width: 768px) and (max-width: 1024px) {
            .block-container {
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }
        }
        
        /* ============ LARGE SCREENS (> 1200px) ============ */
        @media (min-width: 1200px) {
            .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
            }
            
            .hero-container {
                padding: 3rem 2rem;
            }
        }
        
        /* ============ CAMERA INPUT RESPONSIVE ============ */
        .stCameraInput > div {
            border-radius: 10px;
        }
        
        .stCameraInput video {
            border-radius: 10px;
            max-width: 100%;
        }
        
        /* ============ IMAGE RESPONSIVE ============ */
        .stImage img {
            border-radius: 10px;
            max-width: 100%;
            height: auto;
        }
        
        /* ============ EXPANDER RESPONSIVE ============ */
        .streamlit-expanderHeader {
            font-size: clamp(0.9rem, 2.5vw, 1rem);
        }
        
        .streamlit-expanderContent {
            font-size: clamp(0.85rem, 2.5vw, 0.95rem);
        }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def get_prediction_engine():
    """Get cached prediction engine."""
    return PredictionEngine()


def render_hero():
    """Render hero section - fokus pada satu aksi utama."""
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">✏️ Deteksi Alat Tulis Pintar</h1>
        <p class="hero-subtitle">
            Identifikasi Pensil, Penghapus, atau Kertas dalam Hitungan Detik dengan AI
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_categories():
    """Show supported categories - Gestalt principle."""
    col1, col2, col3 = st.columns(3)
    
    categories = [
        {"emoji": "🧹", "title": "Eraser", "subtitle": "Penghapus"},
        {"emoji": "📄", "title": "Kertas", "subtitle": "Paper"},
        {"emoji": "✏️", "title": "Pensil", "subtitle": "Pencil"}
    ]
    
    for col, cat in zip([col1, col2, col3], categories):
        with col:
            st.markdown(f"""
            <div class="category-card">
                <div class="category-emoji">{cat['emoji']}</div>
                <div class="category-title">{cat['title']}</div>
                <div class="category-subtitle">{cat['subtitle']}</div>
            </div>
            """, unsafe_allow_html=True)


def get_fun_fact(predicted_class: str) -> str:
    """Get fun fact berdasarkan hasil prediksi - Delight Factor."""
    facts = {
        "pensil": "💡 Tahukah kamu? Satu pensil bisa menulis sekitar 45.000 kata atau menarik garis sepanjang 56 km!",
        "eraser": "💡 Tahukah kamu? Sebelum penghapus ditemukan, orang menggunakan roti untuk menghapus tulisan pensil!",
        "kertas": "💡 Tahukah kamu? Kertas pertama kali ditemukan di Tiongkok sekitar tahun 105 Masehi oleh Cai Lun!"
    }
    return facts.get(predicted_class.lower(), "")


def render_result_card(result, emoji: str):
    """Render hasil prediksi dengan visualisasi menarik."""
    # Determine confidence level untuk warna
    conf_class = "confidence-high" if result.percentage >= 80 else "confidence-medium" if result.percentage >= 50 else "confidence-low"
    card_class = "result-success" if not result.is_low_confidence else "result-warning"
    
    st.markdown(f"""
    <div class="{card_class}">
        <div style="font-size: 4rem; margin-bottom: 0.5rem;">{emoji}</div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">
            {result.predicted_class.upper()}
        </div>
        <div style="font-size: 1.3rem; opacity: 0.95;">
            Tingkat Keyakinan: {result.percentage:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fun fact - Delight factor
    fun_fact = get_fun_fact(result.predicted_class)
    if fun_fact and not result.is_low_confidence:
        st.markdown(f"""
        <div class="fun-fact-card">
            {fun_fact}
        </div>
        """, unsafe_allow_html=True)


def render_prediction_details(result):
    """Render detail prediksi dengan progress bars."""
    emoji_map = {"eraser": "🧹", "kertas": "📄", "pensil": "✏️"}
    
    st.markdown("##### 📊 Detail Semua Prediksi")
    
    for pred in result.top_predictions:
        emoji = emoji_map.get(pred["class"].lower(), "🏷️")
        conf = pred["confidence"]
        pct = pred["percentage"]
        
        # Determine color class
        if pct >= 80:
            color = "#11998e"
        elif pct >= 50:
            color = "#f39c12"
        else:
            color = "#e74c3c"
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-weight: 600;">{emoji} {pred['class']}</span>
                    <span style="color: {color}; font-weight: 700;">{pct:.1f}%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {pct}%; background: {color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def process_image(image: Image.Image, source_name: str = ""):
    """Process dan prediksi gambar dengan layout responsive."""
    try:
        # Gambar yang diupload
        st.markdown("""
        <div class="step-indicator">
            <div class="step-number">1</div>
            <span class="step-text">Gambar Anda</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.image(image, caption=source_name, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hasil Analisis
        st.markdown("""
        <div class="step-indicator">
            <div class="step-number">2</div>
            <span class="step-text">Hasil Analisis</span>
        </div>
        """, unsafe_allow_html=True)
        
        engine = get_prediction_engine()
        
        # Spinner dengan pesan yang manusiawi - Doherty Threshold
        with st.spinner("🤖 Sedang menganalisis gambar..."):
            result = engine.predict(image, top_k=3)
        
        # Demo mode warning
        if result.is_demo:
            st.warning("⚠️ Mode Demo - Model sedang dimuat, hasil adalah simulasi")
            return
        
        # Get emoji for result
        emoji_map = {"eraser": "🧹", "kertas": "📄", "pensil": "✏️"}
        result_emoji = emoji_map.get(result.predicted_class.lower(), "🏷️")
        
        # Render result card
        render_result_card(result, result_emoji)
        
        # Low confidence warning dengan pesan manusiawi
        if result.is_low_confidence:
            st.warning("🤔 Hmm, saya kurang yakin dengan hasil ini. Coba gunakan gambar yang lebih jelas ya!")
        
        # Detail predictions
        st.markdown("<br>", unsafe_allow_html=True)
        render_prediction_details(result)
                    
    except Exception as e:
        # Error handling yang manusiawi
        st.error(f"😅 Ups, terjadi kesalahan: {str(e)}")
        st.info("💡 Tips: Pastikan gambar dalam format JPG atau PNG dan tidak corrupt.")


def render_upload_section():
    """Render upload section - Hick's Law: fokus pada satu aksi."""
    st.markdown("---")
    
    # Step indicator
    st.markdown("""
    <div class="step-indicator">
        <div class="step-number">📸</div>
        <span class="step-text">Upload atau Ambil Foto Alat Tulis</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📁 Upload File", "📷 Gunakan Kamera"])
    
    with tab1:
        # Upload area
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Seret & lepas gambar di sini",
            type=["jpg", "jpeg", "png"],
            help="Format: JPG, JPEG, PNG. Maksimal: 5MB",
            label_visibility="visible"
        )
        st.caption("📌 Tip: Gunakan gambar dengan pencahayaan yang baik")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Result area
        if uploaded_file:
            st.markdown("<br>", unsafe_allow_html=True)
            try:
                image = Image.open(uploaded_file)
                process_image(image, uploaded_file.name)
            except Exception as e:
                st.error("😕 Ups, sepertinya itu bukan gambar yang valid. Silakan coba format JPG atau PNG.")
    
    with tab2:
        st.caption("📷 Arahkan kamera ke alat tulis dan ambil foto")
        camera_image = st.camera_input(
            "Ambil foto",
            label_visibility="collapsed"
        )
        
        # Result area
        if camera_image:
            st.markdown("<br>", unsafe_allow_html=True)
            try:
                image = Image.open(camera_image)
                process_image(image, "Foto Kamera")
            except Exception as e:
                st.error("😕 Gagal memproses foto dari kamera. Silakan coba lagi.")


def render_sample_section():
    """Render sample images section."""
    st.markdown("---")
    
    with st.expander("🎯 Coba dengan Contoh Gambar", expanded=False):
        samples_dir = Path("samples")
        
        if not samples_dir.exists():
            st.info("Folder samples tidak ditemukan")
            return
        
        col1, col2, col3 = st.columns(3)
        
        sample_files = {
            "eraser": ("eraser_sample.jpg", "🧹 Eraser"),
            "kertas": ("kertas_sample.jpg", "📄 Kertas"),
            "pensil": ("pensil_sample.jpg", "✏️ Pensil")
        }
        
        for col, (key, (filename, label)) in zip([col1, col2, col3], sample_files.items()):
            filepath = samples_dir / filename
            if filepath.exists():
                with col:
                    img = Image.open(filepath)
                    st.image(img, caption=label, use_container_width=True)
                    if st.button(f"Coba {label}", key=f"try_{key}", use_container_width=True):
                        st.session_state.selected_sample = key
                        st.session_state.sample_image = img
        
        # Process selected sample
        if "sample_image" in st.session_state and st.session_state.sample_image is not None:
            st.markdown("---")
            process_image(st.session_state.sample_image, f"Contoh {st.session_state.selected_sample}")
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.sample_image = None
                st.session_state.selected_sample = None
                st.rerun()


def render_tips():
    """Render tips section."""
    with st.expander("💡 Tips untuk Hasil Terbaik"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📸 Kualitas Gambar**
            - Pastikan pencahayaan cukup terang
            - Hindari gambar blur atau buram
            - Gunakan background polos jika memungkinkan
            """)
        
        with col2:
            st.markdown("""
            **🎯 Posisi Objek**
            - Letakkan objek di tengah frame
            - Satu objek per gambar untuk hasil optimal
            - Pastikan objek terlihat jelas seluruhnya
            """)


def render_footer():
    """Render footer."""
    st.markdown("""
    <div class="footer">
        <p>🤖 Powered by Deep Learning CNN Model</p>
        <p>Made with ❤️ by <a href="https://github.com/Hash-SD" target="_blank">Hash-SD</a></p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main app entry point."""
    inject_custom_css()
    render_hero()
    render_categories()
    render_upload_section()
    render_sample_section()
    render_tips()
    render_footer()


if __name__ == "__main__":
    main()
