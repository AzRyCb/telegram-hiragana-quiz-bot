import random

# Database Karakter Hiragana Lengkap (Seion, Dakuon, Handakuon)
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

ALL_ROMAJI = list(set(HIRAGANA_DICT.values()))

def generate_quiz_questions(num_questions=5):
    """
    Menghasilkan list berisi `num_questions` soal acak.
    Setiap elemen berisi:
    - hiragana: Karakter Hiragana (misal: 'あ')
    - correct_romaji: Cara baca benar (misal: 'a')
    - options: List 4 pilihan rōmaji acak (1 benar, 3 salah)
    """
    selected_items = random.sample(list(HIRAGANA_DICT.items()), num_questions)
    questions = []

    for idx, (hiragana, correct_romaji) in enumerate(selected_items):
        # Pilih 3 distractor (pilihan salah) yang unik
        other_romaji = [r for r in ALL_ROMAJI if r != correct_romaji]
        distractors = random.sample(other_romaji, 3)
        
        # Gabungkan dan acak posisi pilihan
        options = distractors + [correct_romaji]
        random.shuffle(options)

        questions.append({
            'q_num': idx + 1,
            'hiragana': hiragana,
            'correct_romaji': correct_romaji,
            'options': options
        })

    return questions
