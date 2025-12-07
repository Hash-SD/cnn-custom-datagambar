# 🏗️ Dokumentasi Arsitektur

## Arsitektur Model CNN

```
Input (300x300x3)
    ↓
Rescaling Layer (normalisasi 0-1)
    ↓
Conv2D (32 filter, 3x3) → ReLU → MaxPool
    ↓
Conv2D (64 filter, 3x3) → ReLU → MaxPool
    ↓
Conv2D (128 filter, 3x3) → ReLU → MaxPool
    ↓
Flatten
    ↓
Dense (128) → ReLU → Dropout (0.5)
    ↓
Dense (3, softmax) → Output
```

## Struktur Project

```
├── app/                    # Aplikasi Streamlit
│   ├── main.py            # Entry point utama
│   ├── config.py          # Konfigurasi
│   └── components/        # Komponen UI
│       ├── predictor.py   # Engine prediksi
│       └── image_uploader.py
├── models/                 # Model ML
│   ├── best_model.keras   # Model terlatih
│   ├── best_model.json    # Metadata model
│   ├── cnn_model.py       # Arsitektur CNN
│   ├── inference.py       # Pipeline inferensi
│   ├── preprocessing.py   # Preprocessing gambar
│   └── train_model.py     # Script training
├── tests/                  # Unit tests
├── samples/               # Contoh gambar
├── docs/                  # Dokumentasi
└── streamlit_app.py       # Entry point cloud
```

## Alur Data

1. **Input**: User upload gambar via Streamlit
2. **Preprocessing**: Gambar di-resize ke 300x300, konversi ke RGB
3. **Inferensi**: Model memprediksi probabilitas kelas
4. **Output**: Top-K prediksi dengan confidence score

## Kelas yang Didukung

| Kelas | Deskripsi |
|-------|-----------|
| eraser | Penghapus |
| kertas | Kertas/Paper |
| pensil | Pensil |

## Metrik Model

| Metrik | Nilai |
|--------|-------|
| Training Accuracy | ~88% |
| Validation Accuracy | ~70% |
| Input Size | 300×300 |
| Jumlah Kelas | 3 |
