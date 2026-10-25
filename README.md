# 🌐 byprhmniTranslate Studio

> Mesin penerjemah mandiri dua arah (Inggris ↔ Indonesia) lokal bertenaga Transformer MarianMT dengan decoding 5-Beams.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=flat&logo=flask&logoColor=white)
![Transformers](https://img.shields.io/badge/Hugging%20Face-MarianMT-FFD21E?style=flat&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Fitur Utama

* **100% Offline & Privat:** Semua inferensi diproses langsung di mesin komputer lokal tanpa kirim teks ke server luar.
* **Dua Arah Instan:** Menerjemahkan bolak-balik English ↔ Indonesia dengan satu tombol swap.
* **Optimalisasi Beam Search:** Menggunakan 5-beams decoding agar struktur kalimat terjemahan rapi dan tidak kaku.
* **Fitur Lengkap:** Text-to-Speech (suara audio), riwayat sesi lokal, salin teks kilat, dan unduh file `.txt`.
* **Desain Responsif:** Tampilan modern dan rapi di layar monitor PC maupun HP.

---

## 🛠️ Cara Install & Menjalankan

Ikuti langkah-langkah di bawah ini di terminal / command prompt:

### 1. Kloning Repositori
```bash
git clone [https://github.com/prhmni/byprhmniTranslate-Studio.git](https://github.com/prhmni/byprhmniTranslate-Studio.git)
cd byprhmniTranslate-Studio
```

### 2. Buat & Aktifkan Virtual Environment
```bash
# Buat environment
python -m venv venv

# Aktifkan di Windows:
venv\Scripts\activate

# Atau aktifkan di Linux / macOS:
# source venv/bin/activate
```

### 3. Install Seluruh Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Web Penerjemah
```bash
python app.py
```

Setelah server aktif, buka browser dan kunjungi:
```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)
```

---

## 👨‍💻 Profil Pengembang

Dibuat oleh **Ipar Hamni**:
* GitHub: [@prhmni](https://github.com/prhmni)
* Instagram: [@prhmni__](https://www.instagram.com/prhmni__?dlrf=MTM5d3lrMG40OWdncg%3D%3D&utm_source=qr)