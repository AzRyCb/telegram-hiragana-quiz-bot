import random

# Database Karakter Hiragana Lengkap
HIRAGANA_DICT = {
    # Seion (Vokal dasar & Konsonan)
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo', 'ん': 'n',

    # Dakuon (Tenten)
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',

    # Handakuon (Maru)
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
}

# Database Kosakata Bahasa Jepang (Ditulis FULL Hiragana)
HIRAGANA_VOCAB = [
    {"hiragana": "ねこ", "romaji": "neko", "meaning": "Kucing"},
    {"hiragana": "いぬ", "romaji": "inu", "meaning": "Anjing"},
    {"hiragana": "さくら", "romaji": "sakura", "meaning": "Bunga Sakura"},
    {"hiragana": "ありがとう", "romaji": "arigatou", "meaning": "Terima Kasih"},
    {"hiragana": "おはよう", "romaji": "ohayou", "meaning": "Selamat Pagi"},
    {"hiragana": "さようなら", "romaji": "sayounara", "meaning": "Selamat Tinggal"},
    {"hiragana": "みず", "romaji": "mizu", "meaning": "Air"},
    {"hiragana": "たべもの", "romaji": "tabemono", "meaning": "Makanan"},
    {"hiragana": "のみもの", "romaji": "nomimono", "meaning": "Minuman"},
    {"hiragana": "ほん", "romaji": "hon", "meaning": "Buku"},
    {"hiragana": "せんせい", "romaji": "sensei", "meaning": "Guru"},
    {"hiragana": "がくせい", "romaji": "gakusei", "meaning": "Siswa / Pelajar"},
    {"hiragana": "ともだち", "romaji": "tomodachi", "meaning": "Teman"},
    {"hiragana": "わたし", "romaji": "watashi", "meaning": "Saya"},
    {"hiragana": "あなた", "romaji": "anata", "meaning": "Anda / Kamu"},
    {"hiragana": "やま", "romaji": "yama", "meaning": "Gunung"},
    {"hiragana": "川", "romaji": "kawa", "meaning": "Sungai"}, # Wait, full hiragana:
    {"hiragana": "かわ", "romaji": "kawa", "meaning": "Sungai"},
    {"hiragana": "そら", "romaji": "sora", "meaning": "Langit"},
    {"hiragana": "うみ", "romaji": "umi", "meaning": "Laut"},
    {"hiragana": "くるま", "romaji": "kuruma", "meaning": "Mobil"},
    {"hiragana": "でんしゃ", "romaji": "densha", "meaning": "Kereta"},
    {"hiragana": "すし", "romaji": "sushi", "meaning": "Sushi"},
    {"hiragana": "お茶", "romaji": "ocha", "meaning": "Teh Hijau"}, # Full hiragana:
    {"hiragana": "おちゃ", "romaji": "ocha", "meaning": "Teh Hijau"},
    {"hiragana": "りんご", "romaji": "ringo", "meaning": "Apel"},
    {"hiragana": "さかな", "romaji": "sakana", "meaning": "Ikan"},
    {"hiragana": "とり", "romaji": "tori", "meaning": "Burung"},
    {"hiragana": "はな", "romaji": "hana", "meaning": "Bunga"},
    {"hiragana": "あめ", "romaji": "ame", "meaning": "Hujan"},
    {"hiragana": "ゆき", "romaji": "yuki", "meaning": "Salju"},
    {"hiragana": "つき", "romaji": "tsuki", "meaning": "Bulan"},
    {"hiragana": "ひかり", "romaji": "hikari", "meaning": "Cahaya"},
    {"hiragana": "こころ", "romaji": "kokoro", "meaning": "Hati / Jiwa"},
    {"hiragana": "ゆめ", "romaji": "yume", "meaning": "Mimpi"},
]

ALL_ROMAJI_CHARS = list(set(HIRAGANA_DICT.values()))
ALL_ROMAJI_VOCAB = list(set([item['romaji'] + f" ({item['meaning']})" for item in HIRAGANA_VOCAB]))

def generate_char_quiz(num_questions=5):
    """Generator Kuis Karakter Hiragana"""
    selected_items = random.sample(list(HIRAGANA_DICT.items()), num_questions)
    questions = []

    for idx, (hiragana, correct_romaji) in enumerate(selected_items):
        other_romaji = [r for r in ALL_ROMAJI_CHARS if r != correct_romaji]
        distractors = random.sample(other_romaji, 3)
        
        options = distractors + [correct_romaji]
        random.shuffle(options)

        questions.append({
            'type': 'char',
            'q_num': idx + 1,
            'hiragana': hiragana,
            'correct_answer': correct_romaji,
            'display_prompt': f"Bagaimana cara membaca karakter Hiragana **` {hiragana} `**?",
            'options': options
        })

    return questions

def generate_vocab_quiz(num_questions=5):
    """Generator Kuis Kosakata Hiragana"""
    num_to_sample = min(num_questions, len(HIRAGANA_VOCAB))
    selected_items = random.sample(HIRAGANA_VOCAB, num_to_sample)
    questions = []

    for idx, item in enumerate(selected_items):
        correct_ans = f"{item['romaji']} ({item['meaning']})"
        
        other_options = [f"{v['romaji']} ({v['meaning']})" for v in HIRAGANA_VOCAB if v['romaji'] != item['romaji']]
        distractors = random.sample(other_options, 3)

        options = distractors + [correct_ans]
        random.shuffle(options)

        questions.append({
            'type': 'vocab',
            'q_num': idx + 1,
            'hiragana': item['hiragana'],
            'correct_answer': correct_ans,
            'display_prompt': f"Apa arti & cara baca kata Hiragana **` {item['hiragana']} `**?",
            'options': options
        })

    return questions

def generate_survival_question():
    """Generator Soal Tunggal untuk Mode Survival Hiragana (Karakter / Vocab acak)"""
    is_vocab = random.choice([True, False])
    if is_vocab:
        item = random.choice(HIRAGANA_VOCAB)
        correct_ans = f"{item['romaji']} ({item['meaning']})"
        other_options = [f"{v['romaji']} ({v['meaning']})" for v in HIRAGANA_VOCAB if v['romaji'] != item['romaji']]
        distractors = random.sample(other_options, 3)
        options = distractors + [correct_ans]
        random.shuffle(options)
        return {
            'type': 'survival',
            'hiragana': item['hiragana'],
            'correct_answer': correct_ans,
            'display_prompt': f"⚡ **[SURVIVAL]** Apa arti & cara baca kata Hiragana **` {item['hiragana']} `**?",
            'options': options
        }
    else:
        hiragana, correct_romaji = random.choice(list(HIRAGANA_DICT.items()))
        other_romaji = [r for r in ALL_ROMAJI_CHARS if r != correct_romaji]
        distractors = random.sample(other_romaji, 3)
        options = distractors + [correct_romaji]
        random.shuffle(options)
        return {
            'type': 'survival',
            'hiragana': hiragana,
            'correct_answer': correct_romaji,
            'display_prompt': f"⚡ **[SURVIVAL]** Bagaimana cara membaca karakter Hiragana **` {hiragana} `**?",
            'options': options
        }
