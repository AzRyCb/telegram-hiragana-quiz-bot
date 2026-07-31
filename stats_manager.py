import json
import os
from datetime import datetime, date

STATS_FILE = os.path.join(os.path.dirname(__file__), "user_stats.json")

def load_all_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_all_stats(data):
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving stats: {e}")

def get_user_stats(user_id: int, user_name: str = "User"):
    user_id_str = str(user_id)
    stats = load_all_stats()
    
    if user_id_str not in stats:
        stats[user_id_str] = {
            "name": user_name,
            "total_questions": 0,
            "correct_answers": 0,
            "survival_high_score": 0,
            "daily_streak": 0,
            "last_active_date": None,
            "created_at": str(date.today())
        }
        save_all_stats(stats)
        
    return stats[user_id_str]

def update_user_stats(user_id: int, user_name: str, questions_answered: int, correct_count: int, survival_score: int = 0):
    user_id_str = str(user_id)
    all_stats = load_all_stats()
    today_str = str(date.today())
    
    if user_id_str not in all_stats:
        u_stat = {
            "name": user_name,
            "total_questions": 0,
            "correct_answers": 0,
            "survival_high_score": 0,
            "daily_streak": 0,
            "last_active_date": None,
            "created_at": today_str
        }
    else:
        u_stat = all_stats[user_id_str]
        
    u_stat["name"] = user_name
    u_stat["total_questions"] += questions_answered
    u_stat["correct_answers"] += correct_count

    if survival_score > u_stat.get("survival_high_score", 0):
        u_stat["survival_high_score"] = survival_score

    # Hitung Daily Streak
    last_date_str = u_stat.get("last_active_date")
    if last_date_str:
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
        delta_days = (date.today() - last_date).days
        if delta_days == 1:
            u_stat["daily_streak"] += 1
        elif delta_days > 1:
            u_stat["daily_streak"] = 1
    else:
        u_stat["daily_streak"] = 1

    u_stat["last_active_date"] = today_str
    all_stats[user_id_str] = u_stat
    save_all_stats(all_stats)
    return u_stat

def get_badge(correct_count: int) -> str:
    if correct_count >= 250:
        return "👑 Hiragana Master"
    elif correct_count >= 100:
        return "🥷 Hiragana Ninja"
    elif correct_count >= 25:
        return "⚔️ Hiragana Warrior"
    else:
        return "🌱 Hiragana Pemula"
