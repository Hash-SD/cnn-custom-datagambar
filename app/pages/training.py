"""
Training page for ATK Classifier Streamlit app.
"""
import streamlit as st
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.config import settings

try:
    from models.train_model import (
        DatasetManager, ATKModelTrainer, TrainingConfig, train_model_from_dataset
    )
    TRAINING_AVAILABLE = True
except ImportError as e:
    TRAINING_AVAILABLE = False
    IMPORT_ERROR = str(e)

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def render_training_page():
    st.title("Model Training")
    
    if not TRAINING_AVAILABLE:
        st.error(f"Training module not available: {IMPORT_ERROR}")
        return
    
    tab1, tab2, tab3 = st.tabs(["Dataset", "Training", "Results"])
    
    with tab1:
        render_dataset_section()
    with tab2:
        render_training_section()
    with tab3:
        render_results_section()


def render_dataset_section():
    st.subheader("Dataset Management")
    
    dataset_dir = st.text_input("Dataset Directory", value=str(settings.DATASET_DIR))
    
    if st.button("Check Dataset"):
        manager = DatasetManager(dataset_dir)
        info = manager.get_dataset_info()
        
        if not info["exists"]:
            st.error(f"Dataset not found: {dataset_dir}")
        else:
            st.success(f"Found {info['total_images']} images")
            for cls in info["classes"]:
                st.write(f"- {cls}: {info['class_counts'][cls]} images")
            st.session_state['dataset_info'] = info
            st.session_state['dataset_dir'] = dataset_dir


def render_training_section():
    st.subheader("Training Configuration")
    
    if 'dataset_info' not in st.session_state:
        st.warning("Check dataset first")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        epochs = st.slider("Epochs", 5, 50, 15)
        batch_size = st.slider("Batch Size", 8, 32, 15)
        learning_rate = st.select_slider("Learning Rate", [0.0001, 0.001, 0.01], 0.001)
    
    with col2:
        conv1 = st.selectbox("Conv1 Filters", [16, 32, 64, 128], 1)
        conv2 = st.selectbox("Conv2 Filters", [32, 64, 128], 1)
        conv3 = st.selectbox("Conv3 Filters", [64, 128, 256], 1)
        dense = st.selectbox("Dense Units", [64, 128, 256], 1)
        dropout = st.slider("Dropout", 0.2, 0.5, 0.5, 0.1)
    
    patience = st.slider("Early Stopping Patience", 2, 10, 3)
    model_path = st.text_input("Model Save Path", "models/best_model.keras")
    
    if st.button("Start Training", type="primary"):
        config = TrainingConfig(
            epochs=epochs, batch_size=batch_size, learning_rate=learning_rate,
            early_stopping_patience=patience, conv1_filters=conv1,
            conv2_filters=conv2, conv3_filters=conv3,
            dense_units=dense, dropout_rate=dropout
        )
        
        progress = st.progress(0)
        status = st.empty()
        metrics = []
        
        def callback(epoch, logs):
            progress.progress(epoch / epochs)
            status.text(f"Epoch {epoch}/{epochs} - Acc: {logs['accuracy']:.4f}")
            metrics.append({'epoch': epoch, **logs})
        
        try:
            result = train_model_from_dataset(
                st.session_state['dataset_dir'], model_path, config, callback
            )
            st.success("Training complete!")
            st.session_state['training_result'] = result
            
            c1, c2 = st.columns(2)
            c1.metric("Accuracy", f"{result.accuracy:.2%}")
            c2.metric("Val Accuracy", f"{result.val_accuracy:.2%}")
        except Exception as e:
            st.error(f"Training failed: {e}")


def render_results_section():
    st.subheader("Training Results")
    
    if 'training_result' not in st.session_state:
        metadata_path = Path("models/best_model.json")
        if metadata_path.exists():
            with open(metadata_path) as f:
                st.json(json.load(f))
        else:
            st.info("No results yet")
        return
    
    result = st.session_state['training_result']
    c1, c2, c3 = st.columns(3)
    c1.metric("Accuracy", f"{result.accuracy:.2%}")
    c2.metric("Val Accuracy", f"{result.val_accuracy:.2%}")
    c3.metric("Epochs", result.epochs_trained)
    
    if PLOTLY_AVAILABLE and result.history:
        fig = make_subplots(1, 2, subplot_titles=('Accuracy', 'Loss'))
        epochs = list(range(1, len(result.history['accuracy']) + 1))
        fig.add_trace(go.Scatter(x=epochs, y=result.history['accuracy'], name='Train'), 1, 1)
        fig.add_trace(go.Scatter(x=epochs, y=result.history['val_accuracy'], name='Val'), 1, 1)
        fig.add_trace(go.Scatter(x=epochs, y=result.history['loss'], name='Train'), 1, 2)
        fig.add_trace(go.Scatter(x=epochs, y=result.history['val_loss'], name='Val'), 1, 2)
        st.plotly_chart(fig, use_container_width=True)
