import hashlib
import os
import sys
from datetime import datetime, timezone, timedelta

import anthropic
import requests

JST = timezone(timedelta(hours=9))

BASE_IMAGE_URL = "https://raw.githubusercontent.com/searge/tarot/master/assets/img/big"

# タロット78枚（カード名・画像ファイル名）
TAROT_CARDS = [
    # 大アルカナ (22枚)
    ("愚者",          "maj00.jpg"),
    ("魔術師",        "maj01.jpg"),
    ("女教皇",        "maj02.jpg"),
    ("女帝",          "maj03.jpg"),
    ("皇帝",          "maj04.jpg"),
    ("教皇",          "maj05.jpg"),
    ("恋人",          "maj06.jpg"),
    ("戦車",          "maj07.jpg"),
    ("力",            "maj08.jpg"),
    ("隠者",          "maj09.jpg"),
    ("運命の輪",      "maj10.jpg"),
    ("正義",          "maj11.jpg"),
    ("吊るされた男",  "maj12.jpg"),
    ("死神",          "maj13.jpg"),
    ("節制",          "maj14.jpg"),
    ("悪魔",          "maj15.jpg"),
    ("塔",            "maj16.jpg"),
    ("星",            "maj17.jpg"),
    ("月",            "maj18.jpg"),
    ("太陽",          "maj19.jpg"),
    ("審判",          "maj20.jpg"),
    ("世界",          "maj21.jpg"),
    # カップ (14枚)
    ("カップのエース",   "cups01.jpg"),
    ("カップの2",        "cups02.jpg"),
    ("カップの3",        "cups03.jpg"),
    ("カップの4",        "cups04.jpg"),
    ("カップの5",        "cups05.jpg"),
    ("カップの6",        "cups06.jpg"),
    ("カップの7",        "cups07.jpg"),
    ("カップの8",        "cups08.jpg"),
    ("カップの9",        "cups09.jpg"),
    ("カップの10",       "cups10.jpg"),
    ("カップのペイジ",   "cups11.jpg"),
    ("カップのナイト",   "cups12.jpg"),
    ("カップのクイーン", "cups13.jpg"),
    ("カップのキング",   "cups14.jpg"),
    # ペンタクル (14枚)
    ("ペンタクルのエース",   "pents01.jpg"),
    ("ペンタクルの2",        "pents02.jpg"),
    ("ペンタクルの3",        "pents03.jpg"),
    ("ペンタクルの4",        "pents04.jpg"),
    ("ペンタクルの5",        "pents05.jpg"),
    ("ペンタクルの6",        "pents06.jpg"),
    ("ペンタクルの7",        "pents07.jpg"),
    ("ペンタクルの8",        "pents08.jpg"),
    ("ペンタクルの9",        "pents09.jpg"),
    ("ペンタクルの10",       "pents10.jpg"),
    ("ペンタクルのペイジ",   "pents11.jpg"),
    ("ペンタクルのナイト",   "pents12.jpg"),
    ("ペンタクルのクイーン", "pents13.jpg"),
    ("ペンタクルのキング",   "pents14.jpg"),
    # ソード (14枚)
    ("ソードのエース",   "swords01.jpg"),
    ("ソードの2",        "swords02.jpg"),
    ("ソードの3",        "swords03.jpg"),
    ("ソードの4",        "swords04.jpg"),
    ("ソードの5",        "swords05.jpg"),
    ("ソードの6",        "swords06.jpg"),
    ("ソードの7",        "swords07.jpg"),
    ("ソードの8",        "swords08.jpg"),
    ("ソードの9",        "swords09.jpg"),
    ("ソードの10",       "swords10.jpg"),
    ("ソードのペイジ",   "swords11.jpg"),
    ("ソードのナイト",   "swords12.jpg"),
    ("ソードのクイーン", "swords13.jpg"),
    ("ソードのキング",   "swords14.jpg"),
    # ワンド (14枚)
    ("ワンドのエース",   "wands01.jpg"),
    ("ワンドの2",        "wands02.jpg"),
    ("ワンドの3",        "wands03.jpg"),
    ("ワンドの4",        "wands04.jpg"),
    ("ワンドの5",        "wands05.jpg"),
    ("ワンドの6",        "wands06.jpg"),
    ("ワンドの7",        "wands07.jpg"),
    ("ワンドの8",        "wands08.jpg"),
    ("ワンドの9",        "wands09.jpg"),
    ("ワンドの10",       "wands10.jpg"),
    ("ワンドのペイジ",   "wands11.jpg"),
    ("ワンドのナイト",   "wands12.jpg"),
    ("ワンドのクイーン", "wands13.jpg"),
    ("ワンドのキング",   "wands14.jpg"),
]


def select_card_for_date(date_str: str) -> tuple[str, str]:
    hash_val = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    index = hash_val % len(TAROT_CARDS)
    return TAROT_CARDS[index]


def get_today_tarot_message(card_name: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": f"""タロットカード「{card_name}」を紹介してください。

条件：
- 以下のフォーマットで、200字前後で書いてください
- フォーマット以外の余分な文章は一切追加しないでください

フォーマット：
🔮 今日のカード：{card_name}
🖼️ 絵柄：[カードに描かれているものを1〜2文で]
✨ 意味：[正位置のキーワードと象徴するものを2〜3文で]
💬 今日のメッセージ：[日常生活へのヒントを1文で]""",
            }
        ],
    )

    return message.content[0].text.strip()


def send_line_message(text: str, image_url: str) -> None:
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url,
            },
            {
                "type": "text",
                "text": text,
            },
        ],
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(
            f"LINE送信エラー: ステータスコード {response.status_code}\n"
            f"詳細: {response.text}"
        )


def main():
    today = datetime.now(JST).strftime("%Y-%m-%d")
    card_name, image_file = select_card_for_date(today)
    image_url = f"{BASE_IMAGE_URL}/{image_file}"
    print(f"[{today}] 今日のカード：{card_name}")

    try:
        message = get_today_tarot_message(card_name)
    except anthropic.APIError as e:
        print(f"Claude APIエラー: {e}", file=sys.stderr)
        sys.exit(1)

    print("生成されたメッセージ:")
    print(message)
    print()

    try:
        send_line_message(message, image_url)
        print("LINEへの送信が完了しました！")
    except RuntimeError as e:
        print(f"LINE送信失敗: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
