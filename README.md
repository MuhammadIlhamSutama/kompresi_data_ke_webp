# 🖼️ Image Watcher & Uploader with Supabase

Proyek Python ini secara otomatis:
1. Memantau folder `images/` untuk file gambar baru.
2. Mengonversi gambar ke format `.webp` dengan kompresi.
3. Mengunggah gambar ke Supabase Storage.
4. Menyimpan metadata gambar (nama, tanggal, jam, URL) ke tabel Supabase (`fotos`).

---

## 🚀 Fitur

- 👀 Auto-folder watcher (`watchdog`)
- 📦 Kompresi & konversi gambar (Pillow)
- ☁️ Upload ke Supabase bucket
- 📝 Simpan metadata ke tabel Supabase
- ✅ Otomatis hapus gambar asli setelah konversi

---

## 🔧 Setup

### 1. Clone Repository

```bash
git clone https://github.com/username/image-uploader-supabase.git
cd image-uploader-supabase
```

### 2. Install Dependency

Pastikan sudah pakai Python 3.9+  
Install `pip` dependency:

```bash
pip install -r requirements.txt
```

### 3. Buat File `.env`

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
```

Contoh file tersedia di `.env.example`.

---

## 🗂️ Struktur Folder

```
images/
└── input-image.jpg
└── output/
    └── input-image.webp
```

---

## ▶️ Menjalankan Aplikasi

```bash
python app.py
```

Program akan memantau folder `images/`. Setiap ada file gambar baru, sistem akan memproses dan mengunggah otomatis.

---

## 📝 Tabel Supabase yang Digunakan

### Tabel: `fotos`

| Kolom     | Tipe      | Keterangan             |
|-----------|-----------|------------------------|
| name      | text      | Nama user/gambar       |
| tanggal   | text      | Format `YYYY-MM-DD`    |
| jam       | text      | Format `HH:MM:SS`      |
| url       | text      | URL publik Supabase    |

---

## 📦 Supabase Bucket

- **Bucket name:** `testfield`
- Pastikan file bersifat **public** agar URL bisa diakses.

---

## 📜 License

MIT License. Bebas digunakan dan dimodifikasi untuk keperluan pribadi atau komersial.

---

## 🙋‍♂️ Author

Made with ❤️ by [your name]
