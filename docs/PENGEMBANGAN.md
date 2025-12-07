# 🛠️ Panduan Pengembangan

## Persiapan Environment

```bash
# Clone repository
git clone https://github.com/Hash-SD/cnn-custom-datagambar.git
cd cnn-custom-datagambar

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Download model
python download_model.py
```

## Menjalankan Aplikasi

```bash
streamlit run streamlit_app.py
```

Aplikasi akan terbuka di `http://localhost:8501`

## Testing

```bash
# Jalankan semua tests
pytest tests/ -v

# Jalankan dengan coverage report
pytest tests/ --cov=models --cov=app

# Jalankan test spesifik
pytest tests/test_cnn_model.py -v
pytest tests/test_preprocessing.py -v
```

## Dependencies Utama

| Package | Fungsi |
|---------|--------|
| streamlit | Framework web |
| tensorflow | Deep learning |
| pillow | Pemrosesan gambar |
| numpy/pandas | Pemrosesan data |
| plotly | Visualisasi |
| pytest/hypothesis | Testing |

## Struktur Kode

### `app/`
- `main.py` - Entry point aplikasi Streamlit
- `config.py` - Konfigurasi (ukuran input, nama kelas, dll)
- `components/` - Komponen UI yang reusable

### `models/`
- `cnn_model.py` - Definisi arsitektur CNN
- `inference.py` - Pipeline inferensi
- `preprocessing.py` - Preprocessing gambar
- `train_model.py` - Script untuk training model

### `tests/`
- Unit tests menggunakan pytest dan hypothesis
- Property-based testing untuk validasi model

## Code Style

- Ikuti PEP 8
- Gunakan type hints
- Tulis docstring untuk semua fungsi
- Buat fungsi kecil dan fokus
- Gunakan nama variabel yang deskriptif

## Kontribusi

1. Fork repository
2. Buat branch fitur (`git checkout -b fitur/NamaFitur`)
3. Commit perubahan (`git commit -m 'Tambah fitur X'`)
4. Push ke branch (`git push origin fitur/NamaFitur`)
5. Buat Pull Request
