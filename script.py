import requests
import json
import os
from time import sleep

# --- Настройки ---
USERNAME = "_inna__ta"  # аккаунт для мониторинга
TELEGRAM_TOKEN = os.getenv("8217935040:AAEHAORrnUsJyTgQrCVHevru6ZVwOz2nIxs")
CHAT_ID = os.getenv("8450180980")
DATA_FILE = "posts.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36"
}

# --- Функции ---
def send_telegram(message):
    """Отправка сообщения в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        resp = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
        print("Telegram status:", resp.status_code, resp.text[:200])
    except Exception as e:
        print("Ошибка отправки Telegram:", e)

def load_posts():
    """Загрузка старых данных постов"""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_posts(data):
    """Сохранение текущих данных постов"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_posts(username):
    """Получение постов с открытого аккаунта Instagram"""
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print("Instagram status:", r.status_code)
        print("Content preview:", r.text[:500])  # первые 500 символов для проверки

        if r.status_code != 200:
            raise Exception(f"Status code {r.status_code}")

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

    # Проверка новых постов
    for pid, info in current_posts.items():
        if pid not in old_posts:
            messages.append(f"🆕 Новый пост: {info['link']}")
            sleep(0.3)

    # Проверка роста лайков
    for pid, info in current_posts.items():
        if pid in old_posts:
            old_likes = old_posts[pid]["likes"]
            new_likes = info["likes"]
            if new_likes > old_likes:
                messages.append(f"❤️ Лайки выросли: {info['link']} {old_likes} → {new_likes} (+{new_likes-old_likes})")
                sleep(0.3)

    # Отправка уведомлений
    if messages:
        send_telegram("\n".join(messages))
    else:
        send_telegram("ℹ️ Проверка выполнена, новых постов или изменений лайков нет.")

    # Сохраняем текущее состояние
    save_posts(current_posts)

if __name__ == "__main__":
    main()
