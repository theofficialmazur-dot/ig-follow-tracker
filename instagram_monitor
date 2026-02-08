import requests
import json
import os
from datetime import datetime

# --- настройки ---
INSTAGRAM_USER_ID = os.getenv("1546006357")
TELEGRAM_TOKEN = os.getenv("8217935040:AAEHAORrnUsJyTgQrCVHevru6ZVwOz2nIxs")
CHAT_ID = os.getenv("8450180980")

FOLLOWERS_FILE = "followers.json"
FOLLOWING_FILE = "following.json"


# --- telegram ---
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


# --- instagram ---
def get_followers(user_id):
    url = f"https://i.instagram.com/api/v1/friendships/{user_id}/followers/"
    headers = {"User-Agent": "Instagram 155.0.0.37.107"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []
    return [u["username"] for u in r.json().get("users", [])]


def get_following(user_id):
    url = f"https://i.instagram.com/api/v1/friendships/{user_id}/following/"
    headers = {"User-Agent": "Instagram 155.0.0.37.107"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []
    return [u["username"] for u in r.json().get("users", [])]


# --- файлы ---
def load_file(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# --- логика ---
def main():
    old_followers = load_file(FOLLOWERS_FILE)
    old_following = load_file(FOLLOWING_FILE)

    followers = get_followers(INSTAGRAM_USER_ID)
    following = get_following(INSTAGRAM_USER_ID)

    messages = []

    # новые подписчики
    new_followers = list(set(followers) - set(old_followers))
    if new_followers:
        messages.append("🟢 Новые подписчики:\n" + "\n".join(new_followers))

    # отписались
    lost_followers = list(set(old_followers) - set(followers))
    if lost_followers:
        messages.append("🔴 Отписались:\n" + "\n".join(lost_followers))

    # на кого подписался
    new_following = list(set(following) - set(old_following))
    if new_following:
        messages.append("➡️ Подписался:\n" + "\n".join(new_following))

    # от кого отписался
    lost_following = list(set(old_following) - set(following))
    if lost_following:
        messages.append("⬅️ Отписался от:\n" + "\n".join(lost_following))

    # отправка
    if messages:
        text = f"📊 Отчет Instagram {datetime.now().strftime('%d.%m %H:%M')}\n\n"
        text += "\n\n".join(messages)
        send_telegram(text)

    # сохранение истории
    save_file(FOLLOWERS_FILE, followers)
    save_file(FOLLOWING_FILE, following)


if __name__ == "__main__":
    main()
