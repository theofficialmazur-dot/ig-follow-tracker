import requests
import json
import os
from time import sleep

# --- Настройки ---
USERNAME = "1546006357"  # Instagram user ID (не ник, нужен numeric ID)
TELEGRAM_TOKEN = os.getenv("8217935040:AAEHAORrnUsJyTgQrCVHevru6ZVwOz2nIxs")
CHAT_ID = os.getenv("1546006357")

FOLLOWING_FILE = "following.json"
FOLLOWERS_FILE = "followers.json"

HEADERS = {
    "User-Agent": "Instagram 155.0.0.37.107"
}

# --- Функции ---
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
        print("Telegram status:", resp.status_code)
    except Exception as e:
        print("Ошибка отправки Telegram:", e)

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def get_following(user_id):
    url = f"https://i.instagram.com/api/v1/friendships/{user_id}/following/"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print("Ошибка получения following:", r.status_code)
        return []
    data = r.json()
    return [u["username"] for u in data.get("users", [])]

def get_followers(user_id):
    url = f"https://i.instagram.com/api/v1/friendships/{user_id}/followers/"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print("Ошибка получения followers:", r.status_code)
        return []
    data = r.json()
    return [u["username"] for u in data.get("users", [])]

# --- Основная логика ---
def main():
    old_following = load_data(FOLLOWING_FILE)
    old_followers = load_data(FOLLOWERS_FILE)

    current_following = get_following(USERNAME)
    current_followers = get_followers(USERNAME)

    # --- Проверка новых подписок ---
    new_following = list(set(current_following) - set(old_following))
    unfollowed = list(set(old_following) - set(current_following))

    # --- Проверка новых подписчиков ---
    new_followers = list(set(current_followers) - set(old_followers))
    lost_followers = list(set(old_followers) - set(current_followers))

    messages = []

    if new_following:
        messages.append("➡️ Новые подписки:\n" + "\n".join(new_following))
    if unfollowed:
        messages.append("⬅️ Отписались от вас:\n" + "\n".join(unfollowed))
    if new_followers:
        messages.append("🆕 Новые подписчики:\n" + "\n".join(new_followers))
    if lost_followers:
        messages.append("❌ Потерянные подписчики:\n" + "\n".join(lost_followers))

    if messages:
        send_telegram("\n\n".join(messages))
    else:
        send_telegram("ℹ️ Проверка выполнена, изменений нет.")

    save_data(FOLLOWING_FILE, current_following)
    save_data(FOLLOWERS_FILE, current_followers)

if __name__ == "__main__":
    main()
