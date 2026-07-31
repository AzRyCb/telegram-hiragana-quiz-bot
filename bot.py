import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from hiragana_data import generate_quiz_questions

# Muat konfigurasi environment (.env)
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary penyimpanan sesi user di memori: {user_id: {questions, current_idx, score}}
USER_SESSIONS = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /start"""
    user_name = update.effective_user.first_name
    welcome_text = (
        f" Konnichiwa, {user_name}!\n\n"
        f"Selamat datang di **Bot Quiz Hiragana Bahasa Jepang**!\n"
        f"Bot ini siap membantu Anda melatih dan mengingat huruf Hiragana setiap hari.\n\n"
        f"📌 **Menu Utama:**\n"
        f"• `/quiz` - Mulai sesi kuis 5 soal Hiragana\n"
        f"• `/help` - Petunjuk penggunaan bot\n\n"
        f"Ketik `/quiz` untuk memulai kuis sekarang! "
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /help"""
    help_text = (
        f"📖 **Petunjuk Penggunaan Bot Quiz Hiragana:**\n\n"
        f"1️⃣ Ketik `/quiz` untuk memulai 5 pertanyaan pilihan ganda.\n"
        f"2️⃣ Pilih jawaban Rōmaji yang tepat dengan menekan tombol.\n"
        f"3️⃣ Bot akan memberikan hasil secara *real-time* beserta jawaban yang benar.\n"
        f"4️⃣ Di akhir sesi, Anda dapat melihat total skor Anda dan mengulang kuis kembali!\n\n"
        f"💡 *Tips:* Latihan 5 soal setiap hari konsisten lebih efektif daripada belajar berjam-jam sekali waktu!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk memulai sesi 5 soal kuis (/quiz)"""
    user_id = update.effective_user.id
    
    # Buat 5 pertanyaan baru
    questions = generate_quiz_questions(num_questions=5)
    
    USER_SESSIONS[user_id] = {
        'questions': questions,
        'current_idx': 0,
        'score': 0
    }
    
    await send_question(update, context, user_id)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Mengirimkan pertanyaan kuis berdasarkan indeks sesi user"""
    session = USER_SESSIONS.get(user_id)
    if not session:
        return

    idx = session['current_idx']
    questions = session['questions']

    if idx >= len(questions):
        # Kuis Selesai! Tampilkan Ringkasan Skor
        score = session['score']
        total = len(questions)
        percentage = (score / total) * 100

        if percentage == 100:
            eval_text = " Sugoi! Nilai Sempurna! Hiragana Anda sangat mantap!"
        elif percentage >= 60:
            eval_text = " Yokatta! Hasil yang bagus! Tingkatkan lagi ya!"
        else:
            eval_text = " Ganbatte! Jangan menyerah, ayo latihan lagi!"

        result_text = (
            f"🎉 **KUIS SELESAI!** 🎉\n\n"
            f"📊 **Skor Anda:** `{score} / {total}` ({percentage:.0f}%)\n"
            f"{eval_text}\n\n"
            f"Ketik `/quiz` untuk mencoba kuis baru! "
        )
        
        # Hapus sesi setelah selesai
        del USER_SESSIONS[user_id]

        if update.callback_query:
            await update.callback_query.message.edit_text(result_text, parse_mode="Markdown")
        else:
            await update.message.reply_text(result_text, parse_mode="Markdown")
        return

    q = questions[idx]
    question_text = (
        f"❓ **Soal {q['q_num']} dari {len(questions)}**\n\n"
        f"Bagaimana cara membaca karakter Hiragana berikut?\n\n"
        f" #️⃣ **` {q['hiragana']} `**\n\n"
        f"Pilih jawaban Rōmaji yang tepat di bawah ini:"
    )

    # Buat tombol pilihan ganda (2 baris x 2 kolom)
    keyboard = [
        [
            InlineKeyboardButton(q['options'][0], callback_data=f"ans_{q['options'][0]}"),
            InlineKeyboardButton(q['options'][1], callback_data=f"ans_{q['options'][1]}"),
        ],
        [
            InlineKeyboardButton(q['options'][2], callback_data=f"ans_{q['options'][2]}"),
            InlineKeyboardButton(q['options'][3], callback_data=f"ans_{q['options'][3]}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.edit_text(question_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(question_text, reply_markup=reply_markup, parse_mode="Markdown")


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler ketika user menekan salah satu tombol jawaban"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = USER_SESSIONS.get(user_id)

    if not session:
        await query.message.edit_text("Sesi kuis telah berakhir. Ketik `/quiz` untuk memulai kuis baru!")
        return

    user_answer = query.data.replace("ans_", "")
    current_q = session['questions'][session['current_idx']]
    correct_ans = current_q['correct_romaji']

    # Cek Jawaban
    if user_answer == correct_ans:
        session['score'] += 1
        feedback = f"✅ **BENAR!** `{current_q['hiragana']}` dibaca `{correct_ans}`."
    else:
        feedback = f"❌ **SALAH!** Jawaban Anda: `{user_answer}`.\nYang benar: `{current_q['hiragana']}` dibaca `{correct_ans}`."

    # Lanjut ke pertanyaan berikutnya
    session['current_idx'] += 1

    # Kirim feedback sebentar & tampilkan soal berikutnya
    await query.message.edit_text(f"{feedback}\n\n⏳ *Memuat soal berikutnya...*", parse_mode="Markdown")
    await send_question(update, context, user_id)


def main():
    if not BOT_TOKEN or BOT_TOKEN == "ISIKAN_TOKEN_BOT_ANDA_DISINI":
        print("\n ERROR: Token Telegram Bot belum diisi!")
        print("Silakan masukkan Token dari @BotFather ke dalam file .env terlebih dahulu.")
        print("Buka file .env dan ganti TELEGRAM_BOT_TOKEN=ISIKAN_TOKEN_BOT_ANDA_DISINI dengan token asli Anda.\n")
        return

    print("[INFO] Bot Telegram Hiragana sedang berjalan...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quiz", start_quiz))
    app.add_handler(CallbackQueryHandler(handle_answer, pattern="^ans_"))

    app.run_polling()


if __name__ == "__main__":
    main()
