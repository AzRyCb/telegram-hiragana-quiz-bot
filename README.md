# 🤖 Bot Telegram Quiz Hiragana Interaktif v2

Bot Telegram interaktif untuk melatih hafalan karakter & kosakata Bahasa Jepang (Hiragana) dengan fitur statistik, daily streak, hint 50:50, dan mode survival.

---

## 🔥 Fitur-Fitur Utama

1. **🔤 Kuis Karakter Hiragana:** Melatih hafalan Rōmaji dari karakter Hiragana tunggal.
2. **💬 Kuis Kosakata Hiragana:** Melatih bacaan & arti kata-kata populer Bahasa Jepang yang ditulis full Hiragana (misal: `ねこ` = `neko` [kucing], `さくら` = `sakura`, `ありがとう` = `arigatou`).
3. **⚡ Mode Survival (Speed Run):** Tantangan menjawab soal secepat dan sebanyak mungkin tanpa boleh salah 1 kali pun!
4. **💡 Hint 50:50:** Tombol bantuan saat kuis yang mengeliminasi 2 opsi pilihan salah.
5. **📊 statistik & Daily Streak (`/stats`):** Mencatat total kuis, persentase akurasi, daily streak harian, dan badge peringkat (*Hiragana Pemula*, *Warrior*, *Ninja*, *Master*).

---

## 📌 Cara Mendapatkan Token Bot Telegram

1. Buka aplikasi **Telegram** di HP atau Laptop Anda.
2. Cari akun resmi Telegram: **`@BotFather`**
3. Ketik perintah: `/newbot`
4. Masukkan **Nama Bot** dan **Username Bot** Anda.
5. Salin **HTTP API Token** yang diberikan oleh `@BotFather`.

---

## ⚙️ Cara Menjalankan Bot di Komputer Anda

### 1. Masukkan Token ke File `.env`
Buka file [`.env`](file:///.env) di folder ini, lalu ganti tulisan `ISIKAN_TOKEN_BOT_ANDA_DISINI` dengan Token Anda:
```env
TELEGRAM_BOT_TOKEN=8804536537:AAHKgqlasvC9WmZLeI-Nmb2zeWRLSQ8wn1w
```

### 2. Install Dependensi
Buka Terminal/PowerShell di folder proyek ini dan jalankan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Bot
Jalankan perintah berikut di Terminal:
```bash
python bot.py
```

---

## 🎮 Command Bot di Telegram
* `/start` — Menampilkan Menu Utama Interaktif
* `/quiz` — Memulai sesi kuis
* `/stats` — Melihat statistik profil & Daily Streak
* `/help` — Panduan penggunaan bot
