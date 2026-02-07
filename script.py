import requests
import json
import os

USERNAME = "_inna__ta"
TELEGRAM_TOKEN = os.getenv("8217935040:AAEHAORrnUsJyTgQrCVHevru6ZVwOz2nIxs")
CHAT_ID = os.getenv("8450180980")

DATA_FILE = "following.json"


def get_following(username):
    url = f"https://i.instagram.com/api/v1/friendships/{username}/following/"
    headers = {
        "User-Agent": "Instagram 155.0.0.37.107",
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []

    data = r.json()
    return [user["username"] for user in data.get("users", [])]


def load_old():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def main():
    current = get_following(USERNAME)
    old = load_old()

    new = list(set(current) - set(old))

    if new:
        msg = "Новые подписки:\n" + "\n".join(new)
        send_telegram(msg)

    save(current)


if __name__ == "__main__":
    main()
