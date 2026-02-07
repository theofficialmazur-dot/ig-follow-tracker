import requests
import json
import os

# Настройки
USERNAME = "_inna__ta"  # аккаунт для мониторинга
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("8450180980")
DATA_FILE = "posts.json"

# --- Функции ---
def send_telegram(message):
    url = f"https://api.telegram.org/bot{8217935040:AAEHAORrnUsJyTgQrCVHevru6ZVwOz2nIxs}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def load_posts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_posts(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_posts(username):
    """Получаем последние посты с аккаунта через публичный endpoint Instagram"""
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        edges = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
        posts = {}
        for edge in edges:
            node = edge["node"]
            posts[node["id"]] = {
                "link": f"https://instagram.com/p/{node['shortcode']}/",
                "likes": node["edge_liked_by"]["count"]
            }
        return posts
    except Exception as e:
        send_telegram(f"Ошибка при получении постов: {e}")
        return {}

def main():
    old_posts = load_posts()
    current_posts = get_posts(USERNAME)
    messages = []

    # Новые посты
    for pid, info in current_posts.items():
        if pid not in old_posts:
            messages.append(f"🆕 Новый пост: {info['link']}")

    # Рост лайков
    for pid, info in current_posts.items():
        if pid in old_posts:
            old_likes = old_posts[pid]["likes"]
            new_likes = info["likes"]
            if new_likes > old_likes:
                messages.append(f"❤️ Лайки выросли: {info['link']} {old_likes} → {new_likes} (+{new_likes-old_likes})")

    # Отправка уведомлений
    if messages:
        send_telegram("\n".join(messages))

    # Сохраняем текущие данные
    save_posts(current_posts)

if name == "__main__":
    main()
