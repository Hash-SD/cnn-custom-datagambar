# 🎓 Panduan Training Model

## Persiapan Dataset

### Struktur Folder Dataset

```
dataset_alat_tulis/
├── eraser/
│   ├── Image_1.jpg
│   ├── Image_2.jpg
│   └── ...
├── kertas/
│   ├── Image_1.jpg
│   ├── Image_2.jpg
│   └── ...
└── pensil/
    ├── Image_1.jpg
    ├── Image_2.jpg
    └── ...
```

### Tips Menyiapkan Dataset

1. **Jumlah Gambar**: Minimal 50-100 gambar per kelas
2. **Variasi**: Gunakan berbagai angle, pencahayaan, dan background
3. **Kualitas**: Gambar harus jelas dan fokus
4. **Format**: JPG, JPEG, atau PNG
5. **Ukuran**: Tidak perlu resize manual, akan di-handle otomatis

## Training via Google Colab

Gunakan notebook `ATK_Training_Colab.ipynb` untuk training di Google Colab:

1. Upload notebook ke Google Colab
2. Upload dataset ke Google Drive
3. Mount Google Drive di Colab
4. Jalankan semua cell

## Training Lokal

### Menggunakan Script

```python
from models.train_model import train_model_from_dataset, TrainingConfig

# Konfigurasi training
config = TrainingConfig(
    epochs=15,
    batch_size=15,
    learning_rate=0.001,
    early_stopping_patience=3,
    conv1_filters=32,
    conv2_filters=64,
    conv3_filters=128,
    dense_units=128,
    dropout_rate=0.5
)

# Jalankan training
result = train_model_from_dataset(
    dataset_dir="dataset_alat_tulis",
    model_save_path="models/best_model.keras",
    config=config
)

print(f"Akurasi: {result.accuracy:.2%}")
print(f"Val Akurasi: {result.val_accuracy:.2%}")
```

### Parameter Training

| Parameter | Default | Deskripsi |
|-----------|---------|-----------|
| epochs | 15 | Jumlah epoch training |
| batch_size | 15 | Ukuran batch |
| learning_rate | 0.001 | Learning rate optimizer |
| early_stopping_patience | 3 | Epoch tunggu sebelum stop |
| conv1_filters | 32 | Filter Conv layer 1 |
| conv2_filters | 64 | Filter Conv layer 2 |
| conv3_filters | 128 | Filter Conv layer 3 |
| dense_units | 128 | Unit Dense layer |
| dropout_rate | 0.5 | Dropout rate |

## Memperbaiki Model

### Jika Akurasi Rendah

1. **Tambah Data**: Lebih banyak gambar = model lebih baik
2. **Augmentasi**: Tambah variasi dengan flip, rotate, zoom
3. **Epoch Lebih Banyak**: Coba 20-30 epoch
4. **Learning Rate**: Coba 0.0001 atau 0.01

### Jika Overfitting

1. **Tambah Dropout**: Naikkan ke 0.6 atau 0.7
2. **Kurangi Model Size**: Kurangi filter atau dense units
3. **Early Stopping**: Kurangi patience ke 2
4. **Augmentasi Data**: Tambah variasi gambar

### Jika Underfitting

1. **Tambah Epoch**: Training lebih lama
2. **Tambah Model Size**: Naikkan filter atau dense units
3. **Kurangi Dropout**: Turunkan ke 0.3 atau 0.4
4. **Learning Rate**: Naikkan sedikit

## Menambah Kelas Baru

1. **Buat folder baru** di dataset dengan nama kelas
2. **Tambah gambar** minimal 50-100 gambar
3. **Update config.py**:
   ```python
   CLASS_NAMES: List[str] = field(default_factory=lambda: [
       "eraser",
       "kertas", 
       "pensil",
       "kelas_baru"  # Tambah di sini
   ])
   NUM_CLASSES: int = 4  # Update jumlah kelas
   ```
4. **Training ulang** model dari awal
5. **Update metadata** di `best_model.json`

## Menyimpan Model

Setelah training, model akan disimpan sebagai:
- `models/best_model.keras` - File model
- `models/best_model.json` - Metadata (class names, metrics)

### Format Metadata

```json
{
  "class_names": ["eraser", "kertas", "pensil"],
  "input_size": [300, 300],
  "metrics": {
    "accuracy": 0.88,
    "val_accuracy": 0.70
  },
  "timestamp": "2025-12-07T11:18:14"
}
```

## Deploy Model Baru

1. **Upload model** ke Google Drive
2. **Share file** dengan "Anyone with link"
3. **Copy file ID** dari URL
4. **Update `download_model.py`**:
   ```python
   GDRIVE_FILE_ID = "file_id_baru_anda"
   ```
5. **Commit dan push** ke GitHub
6. **Streamlit Cloud** akan otomatis redeploy

## Troubleshooting

### Error: Out of Memory
- Kurangi batch_size ke 8 atau 4
- Kurangi ukuran model

### Error: Model tidak konvergen
- Cek dataset apakah ada gambar corrupt
- Coba learning rate berbeda
- Pastikan gambar sudah benar labelnya

### Error: Akurasi tidak naik
- Cek apakah dataset seimbang (jumlah gambar per kelas mirip)
- Coba augmentasi data
- Tambah epoch
