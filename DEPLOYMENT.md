# 🚀 Deployment Guide - ATK Classifier

Panduan lengkap untuk deploy aplikasi ke Streamlit Cloud.

## Prerequisites

- GitHub account dengan repository ini
- Streamlit Cloud account (gratis di https://streamlit.io/cloud)
- Model file sudah tersedia

## Step 1: Persiapan Repository

Pastikan repository sudah clean dan siap:

```bash
# Pastikan semua file sudah di-commit
git status

# Push ke GitHub
git push origin main
```

## Step 2: Setup Streamlit Cloud

### 2.1 Login ke Streamlit Cloud
1. Buka https://share.streamlit.io
2. Login dengan GitHub account
3. Klik "New app"

### 2.2 Konfigurasi Deployment
1. **Repository**: Pilih `Hash-SD/cnn-custom-datagambar`
2. **Branch**: Pilih `main`
3. **Main file path**: Masukkan `streamlit_app.py`
4. **App URL**: Biarkan default atau customize (misal: `atk-classifier-ai`)

### 2.3 Advanced Settings (Optional)
- **Python version**: 3.11
- **Secrets**: Kosongkan (tidak ada secrets yang diperlukan)

## Step 3: Deploy

Klik tombol "Deploy" dan tunggu proses selesai (~2-5 menit).

### Monitoring Deployment

```
✓ Installing dependencies
✓ Downloading model
✓ Starting app
✓ App is live!
```

## Step 4: Verifikasi

Setelah deployment selesai:

1. Buka URL aplikasi: `https://atk-classifier-ai.streamlit.app`
2. Test fitur:
   - Upload gambar di halaman Predict
   - Lihat Dashboard
   - Check Model Management

## Troubleshooting

### Issue: Model tidak terdownload

**Solusi:**
- Pastikan `download_model.py` ada di repository
- Check GitHub releases untuk model file
- Lihat logs di Streamlit Cloud dashboard

### Issue: Memory error

**Solusi:**
- Streamlit Cloud memiliki memory limit ~1GB
- Model sudah dioptimasi untuk ukuran kecil
- Jika masih error, gunakan model quantization

### Issue: Slow loading

**Solusi:**
- Model di-cache setelah first load
- Subsequent requests akan lebih cepat
- Streamlit Cloud auto-scales resources

## Update Aplikasi

Untuk update aplikasi:

```bash
# 1. Buat perubahan lokal
# 2. Commit dan push
git add .
git commit -m "Update: deskripsi perubahan"
git push origin main

# 3. Streamlit Cloud otomatis redeploy
# Cek status di dashboard
```

## Performance Tips

1. **Model Caching**: Model di-cache dengan `@st.cache_resource`
2. **Image Optimization**: Gambar di-resize ke 300x300 untuk inference cepat
3. **Lazy Loading**: Components di-load on-demand

## Security

- ✅ Tidak ada API keys di repository
- ✅ Secrets disimpan di Streamlit Cloud dashboard
- ✅ Model file tidak di-track di git (terlalu besar)
- ✅ Gambar user tidak disimpan

## Monitoring & Logs

Akses logs di Streamlit Cloud:
1. Buka dashboard aplikasi
2. Klik "Manage app"
3. Lihat "Logs" tab

## Rollback

Jika ada issue setelah deploy:

```bash
# Revert ke commit sebelumnya
git revert HEAD
git push origin main

# Streamlit Cloud otomatis redeploy dengan versi lama
```

## Custom Domain (Optional)

Untuk menggunakan custom domain:
1. Beli domain (misal: atk-classifier.com)
2. Setup DNS pointing ke Streamlit Cloud
3. Configure di Streamlit Cloud dashboard

## Scaling

Jika aplikasi mendapat traffic tinggi:
- Streamlit Cloud otomatis scale resources
- Tidak perlu konfigurasi manual
- Upgrade ke Pro plan jika diperlukan

## Support

- 📧 Streamlit Support: https://discuss.streamlit.io
- 🐛 Report issues: GitHub Issues
- 💬 Community: Streamlit Discord

---

**Last Updated**: December 2025
