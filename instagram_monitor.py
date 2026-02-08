from instagrapi import Client
import os
import json

TARGET_USERNAME = "_inna__ta"

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

FOLLOWERS_FILE = "followers.json"
FOLLOWING_FILE = "following.json"


def send_telegram(message):
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


def main():
    cl = Client()

    # логин
    cl.login(IG_USERNAME, IG_PASSWORD)

    user_id = cl.user_id_from_username(TARGET_USERNAME)

    followers = cl.user_followers(user_id)
    following = cl.user_following(user_id)

    current_followers = [u.username for u in followers.values()]
    current_following = [u.username for u in following.values()]

    old_followers = load_data(FOLLOWERS_FILE)
    old_following = load_data(FOLLOWING_FILE)

    new_followers = list(set(current_followers) - set(old_followers))
    lost_followers = list(set(old_followers) - set(current_followers))

    new_following = list(set(current_following) - set(old_following))
    lost_following = list(set(old_following) - set(current_following))

    messages = []

    if new_followers:
        messages.append("🟢 Подписались:\n" + "\n".join(new_followers))

    if lost_followers:
        messages.append("🔴 Отписались:\n" + "\n".join(lost_followers))

    if new_following:
        messages.append("📌 Цель подписалась:\n" + "\n".join(new_following))

    if lost_following:
        messages.append("❌ Цель отписалась:\n" + "\n".join(lost_following))

    if messages:
        send_telegram("\n\n".join(messages))
    else:
        send_telegram("Изменений нет")

    save_data(FOLLOWERS_FILE, current_followers)
    save_data(FOLLOWING_FILE, current_following)


if __name__ == "__main__":
    main()
