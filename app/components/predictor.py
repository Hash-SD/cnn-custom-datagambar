"""
Predictor component for ATK Classifier.
Provides prediction engine with caching and result display.
Enhanced dengan visualisasi yang menarik.
"""
from typing import Optional
from PIL import Image

import streamlit as st

from models.inference import InferencePipeline
from models.cnn_model import PredictionResult
from app.config import settings


class PredictionEngine:
    """
    Prediction engine with Streamlit caching support.
    Uses st.cache_resource for model caching.
    """
    
    def __init__(self):
        """Initialize prediction engine."""
        self._pipeline = self._get_cached_pipeline()
    
    @staticmethod
    @st.cache_resource
    def _get_cached_pipeline() -> InferencePipeline:
        """
        Get cached inference pipeline.
        Uses st.cache_resource to cache the model across sessions.
        
        Returns:
            Cached InferencePipeline instance
        """
        return InferencePipeline(
            model_path=str(settings.MODEL_PATH),
            input_size=settings.INPUT_SIZE,
            class_names=settings.CLASS_NAMES,
            low_confidence_threshold=settings.LOW_CONFIDENCE_THRESHOLD
        )
    
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode."""
        return self._pipeline.is_demo_mode()
    
    def predict(self, image: Image.Image, top_k: int = None) -> PredictionResult:
        """
        Run prediction on an image.
        
        Args:
            image: PIL Image to classify
            top_k: Number of top predictions (default from settings)
            
        Returns:
            PredictionResult with classification results
        """
        top_k = top_k or settings.TOP_K_PREDICTIONS
        return self._pipeline.predict(image, top_k=top_k)


def get_confidence_color(percentage: float) -> str:
    """Get color based on confidence level."""
    if percentage >= 80:
        return "#11998e"  # Green
    elif percentage >= 50:
        return "#f39c12"  # Orange
    else:
        return "#e74c3c"  # Red


def get_emoji_for_class(class_name: str) -> str:
    """Get emoji for predicted class."""
    emoji_map = {
        "eraser": "🧹",
        "kertas": "📄",
        "pensil": "✏️"
    }
    return emoji_map.get(class_name.lower(), "🏷️")


def display_results(result: PredictionResult) -> None:
    """
    Display prediction results in Streamlit dengan visualisasi menarik.
    
    Args:
        result: PredictionResult to display
    """
    # Demo mode indicator
    if result.is_demo:
        st.warning(f"⚠️ {settings.DEMO_MODE_MESSAGE}")
        return
    
    emoji = get_emoji_for_class(result.predicted_class)
    color = get_confidence_color(result.percentage)
    
    # Main result card dengan gradient
    if result.is_low_confidence:
        gradient = "linear-gradient(135deg, #f39c12 0%, #f1c40f 100%)"
    else:
        gradient = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
    
    st.markdown(f"""
    <div style="
        background: {gradient};
        color: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
    ">
        <div style="font-size: 4rem; margin-bottom: 0.5rem;">{emoji}</div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">
            {result.predicted_class.upper()}
        </div>
        <div style="font-size: 1.3rem; opacity: 0.95;">
            Tingkat Keyakinan: {result.percentage:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Low confidence warning dengan pesan manusiawi
    if result.is_low_confidence:
        st.warning(
            "🤔 Hmm, saya kurang yakin dengan hasil ini. "
            "Coba gunakan gambar yang lebih jelas ya!"
        )
    
    # Top-K predictions dengan progress bars
    st.markdown("##### 📊 Detail Prediksi")
    
    for pred in result.top_predictions:
        pred_emoji = get_emoji_for_class(pred["class"])
        pred_color = get_confidence_color(pred["percentage"])
        pct = pred["percentage"]
        
        st.markdown(f"""
        <div style="margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600;">{pred_emoji} {pred['class']}</span>
                <span style="color: {pred_color}; font-weight: 700;">{pct:.1f}%</span>
            </div>
            <div style="background: #E2E8F0; border-radius: 10px; height: 10px; overflow: hidden;">
                <div style="width: {pct}%; height: 100%; background: {pred_color}; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_results_compact(result: PredictionResult) -> None:
    """
    Display prediction results in a compact format.
    
    Args:
        result: PredictionResult to display
    """
    # Demo mode indicator
    if result.is_demo:
        st.caption(f"⚠️ Demo mode - predictions are simulated")
        return
    
    emoji = get_emoji_for_class(result.predicted_class)
    color = get_confidence_color(result.percentage)
    
    # Compact result dengan metric
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Terdeteksi Sebagai",
            value=f"{emoji} {result.predicted_class}"
        )
    
    with col2:
        delta_color = "normal" if result.percentage >= 70 else "off"
        st.metric(
            label="Keyakinan",
            value=f"{result.percentage:.1f}%",
            delta="Tinggi" if result.percentage >= 80 else "Rendah" if result.percentage < 50 else "Sedang"
        )
    
    # Progress bar
    st.progress(result.confidence)
    
    # Low confidence warning
    if result.is_low_confidence:
        st.caption("⚠️ Confidence rendah - coba gambar yang lebih jelas")


def display_results_card(result: PredictionResult) -> None:
    """
    Display prediction results as a beautiful card.
    
    Args:
        result: PredictionResult to display
    """
    if result.is_demo:
        st.info("🔄 Mode Demo - Model sedang dimuat")
        return
    
    emoji = get_emoji_for_class(result.predicted_class)
    
    # Card dengan styling
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    ">
        <div style="font-size: 3rem;">{emoji}</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #1A202C; margin: 0.5rem 0;">
            {result.predicted_class}
        </div>
        <div style="
            background: linear-gradient(90deg, #0083B8 0%, #00B4DB 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-block;
            font-weight: 600;
        ">
            {result.percentage:.1f}% yakin
        </div>
    </div>
    """, unsafe_allow_html=True)
