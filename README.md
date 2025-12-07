# ✏️ ATK Classifier

Klasifikasi Alat Tulis Kantor dengan AI - Powered by Deep Learning

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cnn-atk.streamlit.app)

## 🎯 Fitur

Upload atau foto gambar ATK, langsung dapat hasil klasifikasi:

| Kategori | Deskripsi |
|----------|-----------|
| 🧹 **Eraser** | Penghapus |
| 📄 **Kertas** | Paper |
| ✏️ **Pensil** | Pencil |

## 🚀 Demo Online

Langsung coba: **[cnn-atk.streamlit.app](https://cnn-atk.streamlit.app)**

## 💻 Jalankan Lokal

```bash
# Clone
git clone https://github.com/Hash-SD/cnn-custom-datagambar.git
cd cnn-custom-datagambar

# Install
pip install -r requirements.txt

# Download model (pertama kali)
python download_model.py

# Jalankan
streamlit run streamlit_app.py
```

## 🧠 Model

- **Arsitektur**: CNN (3 Conv layers)
- **Input**: 300×300 pixels
- **Akurasi**: ~88%

## 📁 Struktur

```
├── app/                    # Aplikasi Streamlit
├── models/                 # Model ML
├── tests/                  # Unit tests
├── samples/               # Contoh gambar
├── docs/                  # Dokumentasi
└── streamlit_app.py       # Entry point
```

## 📚 Dokumentasi

| Dokumen | Deskripsi |
|---------|-----------|
| [Arsitektur](docs/ARSITEKTUR.md) | Struktur model & project |
| [Pengembangan](docs/PENGEMBANGAN.md) | Panduan setup & testing |
| [Training](docs/TRAINING.md) | Panduan melatih/memperbaiki model |

## 🛠️ Tech Stack

- Streamlit
- TensorFlow/Keras
- Pillow
- Plotly

## 📄 Lisensi

MIT

---

**Dibuat dengan ❤️ oleh Hash-SD**
