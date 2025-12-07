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
    """Inject CSS untuk UI yang bersih dan eye-catching."""
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
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #0083B8 0%, #00B4DB 50%, #48C6EF 100%);
            border-radius: 20px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(0, 131, 184, 0.3);
        }
        
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.95;
            margin-top: 0.8rem;
            font-weight: 300;
        }
        
        /* Upload Card - Affordance dengan shadow dan border-radius */
        .upload-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 2px dashed #E2E8F0;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .upload-card:hover {
            border-color: #0083B8;
            box-shadow: 0 8px 30px rgba(0, 131, 184, 0.15);
            transform: translateY(-2px);
        }
        
        /* Result Card - Elevation untuk menonjol */
        .result-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .result-success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 8px 30px rgba(17, 153, 142, 0.3);
        }
        
        .result-warning {
            background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
            color: white;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        }
        
        /* Category Cards - Gestalt Proximity */
        .category-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        
        .category-card:hover {
            border-color: #0083B8;
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0, 131, 184, 0.2);
        }
        
        .category-emoji {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        
        .category-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #1A202C;
            margin: 0.5rem 0 0.3rem 0;
        }
        
        .category-subtitle {
            font-size: 0.9rem;
            color: #718096;
        }
        
        /* Custom Button - Clickable Affordance */
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            height: 3.2em;
            font-weight: 600;
            font-size: 1rem;
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
        
        /* File Uploader Styling */
        .stFileUploader > div > div {
            border-radius: 12px;
        }
        
        /* Progress Bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #0083B8 0%, #00B4DB 100%);
            border-radius: 10px;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #0083B8;
        }
        
        /* Info/Warning/Success boxes */
        .stAlert {
            border-radius: 12px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 10px 20px;
        }
        
        /* Confidence Bar Container */
        .confidence-bar {
            background: #E2E8F0;
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            margin: 0.5rem 0;
        }
        
        .confidence-fill {
            height: 100%;
            border-radius: 10px;
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
        
        /* Fun Fact Card */
        .fun-fact-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-top: 1rem;
            font-size: 0.95rem;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #718096;
            font-size: 0.85rem;
            padding: 2rem 0 1rem 0;
            margin-top: 2rem;
            border-top: 1px solid #E2E8F0;
        }
        
        .footer a {
            color: #0083B8;
            text-decoration: none;
        }
        
        /* Waiting State */
        .waiting-state {
            text-align: center;
            padding: 3rem 2rem;
            color: #718096;
        }
        
        .waiting-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        /* Step Indicator */
        .step-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .step-number {
            background: #0083B8;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.9rem;
        }
        
        .step-text {
            font-weight: 600;
            color: #1A202C;
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
    """Process dan prediksi gambar dengan layout side-by-side (Gestalt)."""
    try:
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("""
            <div class="step-indicator">
                <div class="step-number">1</div>
                <span class="step-text">Gambar Anda</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.image(image, caption=source_name, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
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
        col_upload, col_preview = st.columns([1, 1], gap="large")
        
        with col_upload:
            st.markdown('<div class="upload-card">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Seret & lepas gambar di sini",
                type=["jpg", "jpeg", "png"],
                help="Format: JPG, JPEG, PNG. Maksimal: 5MB",
                label_visibility="visible"
            )
            st.caption("📌 Tip: Gunakan gambar dengan pencahayaan yang baik")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_preview:
            if uploaded_file:
                try:
                    image = Image.open(uploaded_file)
                    process_image(image, uploaded_file.name)
                except Exception as e:
                    st.error("😕 Ups, sepertinya itu bukan gambar yang valid. Silakan coba format JPG atau PNG.")
            else:
                st.markdown("""
                <div class="waiting-state">
                    <div class="waiting-icon">🖼️</div>
                    <p>Preview gambar akan muncul di sini</p>
                    <p style="font-size: 0.85rem;">Unggah gambar untuk memulai analisis</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        col_cam, col_result = st.columns([1, 1], gap="large")
        
        with col_cam:
            st.caption("📷 Arahkan kamera ke alat tulis dan ambil foto")
            camera_image = st.camera_input(
                "Ambil foto",
                label_visibility="collapsed"
            )
        
        with col_result:
            if camera_image:
                try:
                    image = Image.open(camera_image)
                    process_image(image, "Foto Kamera")
                except Exception as e:
                    st.error("😕 Gagal memproses foto dari kamera. Silakan coba lagi.")
            else:
                st.markdown("""
                <div class="waiting-state">
                    <div class="waiting-icon">📷</div>
                    <p>Hasil analisis akan muncul di sini</p>
                    <p style="font-size: 0.85rem;">Ambil foto untuk memulai</p>
                </div>
                """, unsafe_allow_html=True)


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
