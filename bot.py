import os
import random
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from hiragana_data import (
    generate_char_quiz,
    generate_vocab_quiz,
    generate_survival_question,
)
from stats_manager import get_user_stats, update_user_stats, get_badge

# Muat variabel environment (.env)
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Memori Sesi Pengguna: {user_id: {mode, questions, current_idx, score, hints_used, current_question}}
USER_SESSIONS = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler perintah /start - Menampilkan Menu Utama Interaktif"""
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    
    # Ambil data statistik untuk streak
    stat = get_user_stats(user_id, user_name)
    streak = stat.get("daily_streak", 0)
    badge = get_badge(stat.get("correct_answers", 0))

    welcome_text = (
        f" Konnichiwa, {user_name}!\n\n"
        f"Selamat datang di **Bot Kuis Hiragana Interaktif**!\n"
        f"Peringkat Anda: **{badge}** | 🔥 Daily Streak: **{streak} Hari**\n\n"
        f"Pilih mode latihan Hiragana yang ingin Anda mainkan di bawah ini:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🔤 Kuis Karakter Hiragana", callback_data="menu_mode_char"),
        ],
        [
            InlineKeyboardButton("💬 Kuis Kosakata Hiragana", callback_data="menu_mode_vocab"),
        ],
        [
            InlineKeyboardButton("⚡ Survival Mode (Speed Run)", callback_data="start_survival"),
        ],
        [
            InlineKeyboardButton("📊 Statistik & Streak Saya", callback_data="show_stats"),
            InlineKeyboardButton("📖 Petunjuk (/help)", callback_data="show_help"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler perintah /help"""
    help_text = (
        f"📖 **Panduan Fitur Bot Kuis Hiragana:**\n\n"
        f"1️⃣ **🔤 Kuis Karakter:** Melatih hafalan Rōmaji dari huruf Hiragana tunggal.\n"
        f"2️⃣ **💬 Kuis Kosakata:** Melatih bacaan & arti kata-kata Bahasa Jepang yang ditulis full Hiragana.\n"
        f"3️⃣ **⚡ Survival Mode:** Jawab soal secepat dan sebanyak mungkin tanpa boleh salah 1x pun!\n"
        f"4️⃣ **💡 Hint 50:50:** Tekan tombol Hint saat kuis untuk menghapus 2 opsi salah.\n"
        f"5️⃣ **📊 `/stats`:** Cek total kuis, akurasi jawaban, badge, dan streak latihan harian Anda.\n\n"
        f"Ketik `/start` kapan saja untuk kembali ke menu utama!"
    )
    if update.callback_query:
        keyboard = [[InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data="main_menu")]]
        await update.callback_query.message.edit_text(help_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.message.reply_text(help_text, parse_mode="Markdown")


async def show_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler perintah /stats - Menampilkan statistik profil pengguna"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    stat = get_user_stats(user_id, user_name)
    total_q = stat.get("total_questions", 0)
    correct_a = stat.get("correct_answers", 0)
    survival_hs = stat.get("survival_high_score", 0)
    streak = stat.get("daily_streak", 0)
    badge = get_badge(correct_a)
    
    acc = (correct_a / total_q * 100) if total_q > 0 else 0

    stats_text = (
        f"📊 **STATISTIK PROFIL HIRAGANA**\n\n"
        f"👤 **Nama:** {user_name}\n"
        f"🏆 **Peringkat:** {badge}\n"
        f"🔥 **Daily Streak:** `{streak} Hari Berturut-turut`\n\n"
        f"🎯 **Total Soal Dijawab:** `{total_q}`\n"
        f"✅ **Jawaban Benar:** `{correct_a}`\n"
        f"📈 **Akurasi Jawaban:** `{acc:.1f}%`\n"
        f"⚡ **Rekor High Score Survival:** `{survival_hs}` soal berturut-turut\n\n"
        f" Terus tingkatkan streak Anda dengan latihan setiap hari!"
    )
    
    keyboard = [[InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.edit_text(stats_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(stats_text, reply_markup=reply_markup, parse_mode="Markdown")


async def select_length_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan pilihan jumlah soal untuk mode kuis"""
    query = update.callback_query
    await query.answer()
    
    mode = "char" if query.data == "menu_mode_char" else "vocab"
    mode_name = "Karakter Hiragana" if mode == "char" else "Kosakata Hiragana"

    text = f"🎯 **Mode: Kuis {mode_name}**\n\nPilih jumlah soal yang ingin Anda kerjakan:"
    keyboard = [
        [
            InlineKeyboardButton("5 Soal (Cepat)", callback_data=f"start_{mode}_5"),
            InlineKeyboardButton("10 Soal (Standar)", callback_data=f"start_{mode}_10"),
            InlineKeyboardButton("15 Soal (Tantangan)", callback_data=f"start_{mode}_15"),
        ],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def start_quiz_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Memulai sesi kuis normal (Char atau Vocab)"""
    query = update.callback_query
    await query.answer()

    data_parts = query.data.split("_") # start_char_5 atau start_vocab_10
    mode = data_parts[1]
    num_q = int(data_parts[2])
    user_id = query.from_user.id

    if mode == "char":
        questions = generate_char_quiz(num_q)
    else:
        questions = generate_vocab_quiz(num_q)

    USER_SESSIONS[user_id] = {
        'mode': mode,
        'questions': questions,
        'current_idx': 0,
        'score': 0,
        'hints_remaining': 2 # Maksimal 2 kali hint per sesi
    }

    await send_normal_question(update, context, user_id)


async def send_normal_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Mengirim pertanyaan kuis normal"""
    session = USER_SESSIONS.get(user_id)
    if not session:
        return

    idx = session['current_idx']
    questions = session['questions']

    if idx >= len(questions):
        # Kuis Selesai! Update Stats & Tampilkan Hasil
        score = session['score']
        total = len(questions)
        percentage = (score / total) * 100
        user_name = update.effective_user.first_name

        # Simpan ke statistik
        u_stat = update_user_stats(user_id, user_name, questions_answered=total, correct_count=score)
        badge = get_badge(u_stat.get("correct_answers", 0))

        if percentage == 100:
            eval_text = " Sugoi! 100% Sempurna! Ingatan Hiragana Anda luar biasa!"
        elif percentage >= 70:
            eval_text = " Yokatta! Hasil sangat baik! Pertahankan!"
        else:
            eval_text = " Ganbatte! Terus berlatih agar semakin lancar!"

        result_text = (
            f"🎉 **KUIS SELESAI!** 🎉\n\n"
            f"📊 **Skor Anda:** `{score} / {total}` ({percentage:.0f}%)\n"
            f"🏆 **Peringkat Saat Ini:** {badge}\n"
            f"🔥 **Daily Streak:** `{u_stat.get('daily_streak', 1)} Hari`\n\n"
            f"{eval_text}"
        )

        keyboard = [
            [InlineKeyboardButton("🔄 Main Kuis Lagi", callback_data="main_menu")],
            [InlineKeyboardButton("📊 Lihat Statistik Lengkap", callback_data="show_stats")]
        ]
        
        del USER_SESSIONS[user_id]
        await update.callback_query.message.edit_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return

    q = questions[idx]
    session['current_question'] = q

    question_text = (
        f"❓ **Soal {q['q_num']} dari {len(questions)}**\n\n"
        f"{q['display_prompt']}\n\n"
        f"Pilih jawaban yang tepat di bawah ini:"
    )

    # Render Opsi Jawaban
    options = q['options']
    keyboard = []
    
    # 2x2 grid tombol pilihan
    row1 = [InlineKeyboardButton(opt, callback_data=f"ans_{i}") for i, opt in enumerate(options[:2])]
    row2 = [InlineKeyboardButton(opt, callback_data=f"ans_{i+2}") for i, opt in enumerate(options[2:])]
    keyboard.append(row1)
    keyboard.append(row2)

    # Tombol Hint jika masih ada sisa hint
    if session.get('hints_remaining', 0) > 0 and len(options) == 4:
        keyboard.append([InlineKeyboardButton(f"💡 Hint 50:50 (Sisa {session['hints_remaining']})", callback_data="use_hint")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.edit_text(question_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(question_text, reply_markup=reply_markup, parse_mode="Markdown")


async def handle_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler tombol 💡 Hint 50:50"""
    query = update.callback_query
    user_id = query.from_user.id
    session = USER_SESSIONS.get(user_id)

    if not session or session.get('hints_remaining', 0) <= 0:
        await query.answer("Kesempatan Hint 50:50 sudah habis untuk sesi ini!", show_alert=True)
        return

    session['hints_remaining'] -= 1
    q = session['current_question']
    correct_ans = q['correct_answer']
    options = q['options']

    # Cari opsi salah dan eliminasi 2 dari opsi salah
    wrong_indices = [i for i, opt in enumerate(options) if opt != correct_ans]
    to_remove = random.sample(wrong_indices, 2)

    new_options = []
    keyboard = []

    for i, opt in enumerate(options):
        if i in to_remove:
            new_options.append("❌ (Tereliminasi)")
        else:
            new_options.append(opt)

    row1 = [
        InlineKeyboardButton(new_options[0], callback_data="ans_0" if new_options[0] != "❌ (Tereliminasi)" else "ignore"),
        InlineKeyboardButton(new_options[1], callback_data="ans_1" if new_options[1] != "❌ (Tereliminasi)" else "ignore"),
    ]
    row2 = [
        InlineKeyboardButton(new_options[2], callback_data="ans_2" if new_options[2] != "❌ (Tereliminasi)" else "ignore"),
        InlineKeyboardButton(new_options[3], callback_data="ans_3" if new_options[3] != "❌ (Tereliminasi)" else "ignore"),
    ]
    keyboard.append(row1)
    keyboard.append(row2)

    await query.answer("💡 2 Pilihan salah berhasil dieliminasi!", show_alert=False)
    question_text = (
        f"❓ **Soal {q['q_num']} dari {len(session['questions'])}** *(Hint 50:50 Digunakan)*\n\n"
        f"{q['display_prompt']}\n\n"
        f"Pilih jawaban yang tepat di bawah ini:"
    )
    await query.message.edit_text(question_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def start_survival(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler memulai Survival Mode"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    USER_SESSIONS[user_id] = {
        'mode': 'survival',
        'score': 0,
        'current_question': generate_survival_question()
    }
    await send_survival_question(update, context, user_id)


async def send_survival_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Mengirim pertanyaan Survival Mode"""
    session = USER_SESSIONS.get(user_id)
    if not session:
        return

    q = session['current_question']
    score = session['score']

    question_text = (
        f"⚡ **SURVIVAL MODE (Streak: {score})**\n\n"
        f"{q['display_prompt']}\n\n"
        f"⚠️ *Hati-hati! 1 Kali salah kuis langsung berakhir!*"
    )

    options = q['options']
    row1 = [InlineKeyboardButton(opt, callback_data=f"surv_ans_{i}") for i, opt in enumerate(options[:2])]
    row2 = [InlineKeyboardButton(opt, callback_data=f"surv_ans_{i+2}") for i, opt in enumerate(options[2:])]
    reply_markup = InlineKeyboardMarkup([row1, row2])

    if update.callback_query:
        await update.callback_query.message.edit_text(question_text, reply_markup=reply_markup, parse_mode="Markdown")


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler jawaban kuis normal"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = USER_SESSIONS.get(user_id)

    if not session or query.data == "ignore":
        return

    ans_idx = int(query.data.replace("ans_", ""))
    q = session['current_question']
    selected_option = q['options'][ans_idx]
    correct_ans = q['correct_answer']

    if selected_option == correct_ans:
        session['score'] += 1
        feedback = f"✅ **BENAR!** Jawaban yang tepat: `{correct_ans}`."
    else:
        feedback = f"❌ **SALAH!** Anda memilih: `{selected_option}`.\nJawaban yang benar: `{correct_ans}`."

    session['current_idx'] += 1
    await query.message.edit_text(f"{feedback}\n\n⏳ *Memuat soal berikutnya...*", parse_mode="Markdown")
    await send_normal_question(update, context, user_id)


async def handle_survival_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler jawaban Survival Mode"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    session = USER_SESSIONS.get(user_id)

    if not session:
        return

    ans_idx = int(query.data.replace("surv_ans_", ""))
    q = session['current_question']
    selected_option = q['options'][ans_idx]
    correct_ans = q['correct_answer']

    if selected_option == correct_ans:
        session['score'] += 1
        # Lanjut ke soal survival berikutnya
        session['current_question'] = generate_survival_question()
        await send_survival_question(update, context, user_id)
    else:
        # Survival Berakhir!
        final_score = session['score']
        u_stat = update_user_stats(user_id, user_name, questions_answered=final_score+1, correct_count=final_score, survival_score=final_score)
        
        game_over_text = (
            f"💥 **GAME OVER SURVIVAL!** 💥\n\n"
            f"❌ Jawaban Anda salah (`{selected_option}`).\n"
            f"Jawaban yang benar: `{correct_ans}`.\n\n"
            f"⚡ **Skor Survival Sesi Ini:** `{final_score}` Soal Benar\n"
            f"🏆 **High Score Survival Anda:** `{u_stat.get('survival_high_score', 0)}` Soal\n"
        )
        keyboard = [
            [InlineKeyboardButton("⚡ Coba Survival Lagi", callback_data="start_survival")],
            [InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data="main_menu")]
        ]
        del USER_SESSIONS[user_id]
        await query.message.edit_text(game_over_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


def main():
    if not BOT_TOKEN or BOT_TOKEN == "ISIKAN_TOKEN_BOT_ANDA_DISINI":
        print("[ERROR] Token Telegram Bot belum diisi di file .env!")
        return

    print("[INFO] Bot Telegram Hiragana Interaktif v2 sedang berjalan...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", show_stats_command))
    app.add_handler(CommandHandler("quiz", start))

    # Callbacks Menu & Modus
    app.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(help_command, pattern="^show_help$"))
    app.add_handler(CallbackQueryHandler(show_stats_command, pattern="^show_stats$"))
    app.add_handler(CallbackQueryHandler(select_length_menu, pattern="^menu_mode_"))
    app.add_handler(CallbackQueryHandler(start_quiz_session, pattern="^start_(char|vocab)_"))
    app.add_handler(CallbackQueryHandler(start_survival, pattern="^start_survival$"))
    app.add_handler(CallbackQueryHandler(handle_hint, pattern="^use_hint$"))
    app.add_handler(CallbackQueryHandler(handle_answer, pattern="^ans_"))
    app.add_handler(CallbackQueryHandler(handle_survival_answer, pattern="^surv_ans_"))

    app.run_polling()


if __name__ == "__main__":
    main()
