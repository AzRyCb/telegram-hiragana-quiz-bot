# 🤖 Bot Telegram Quiz Bahasa Jepang (Hiragana)

Bot Telegram interaktif untuk melatih ingatan karakter Hiragana Bahasa Jepang dengan kuis 5 soal pilihan ganda setiap sesi.

---

## 🛠️ Persiapan Awal (Hanya Perlu Sekali)

### Langkah 1: Pastikan Python Terpasang di Komputer Anda
Jika komputer Anda belum memiliki Python:
1. Download & Install Python dari [python.org/downloads](https://www.python.org/downloads/) (atau cari **Python** di Microsoft Store).
2. ⚠️ **PENTING:** Saat menginstal, pastikan centang opsi **"Add Python to PATH"**.

---

## 📌 Cara Mendapatkan Token Bot Telegram (Hanya 1 Menit)

1. Buka aplikasi **Telegram** di HP atau Laptop Anda.
2. Cari akun resmi Telegram: **`@BotFather`**
3. Ketik perintah: `/newbot`
4. Masukkan **Nama Bot** Anda (misalnya: `Kuis Hiragana Bot`).
5. Masukkan **Username Bot** Anda (harus diakhiri dengan kata `bot`, misalnya: `my_hiragana_quiz_bot`).
6. `@BotFather` akan memberikan **HTTP API Token** (contoh: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
7. Salin Token tersebut!

---

## ⚙️ Cara Menjalankan Bot di Komputer Anda

### 1. Masukkan Token ke File `.env`
Buka file [`.env`](file:///C:/Users/azry6/.gemini/antigravity/scratch/telegram_hiragana_bot/.env) di folder ini, lalu ganti tulisan `ISIKAN_TOKEN_BOT_ANDA_DISINI` dengan Token Anda:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
```

### 2. Install Dependensi
Buka Terminal/PowerShell di folder proyek `telegram_hiragana_bot` dan jalankan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Bot
Jalankan perintah berikut di Terminal:
```bash
python bot.py
```

---

## 🎮 Cara Menggunakan di Telegram HP Anda
1. Buka Telegram di HP Anda.
2. Cari nama Username bot Anda (misalnya `@my_hiragana_quiz_bot`).
3. Ketik **/start**
4. Ketik **/quiz** untuk mulai menjawab 5 soal kuis Hiragana!

