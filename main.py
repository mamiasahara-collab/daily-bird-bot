import os
import sys
from datetime import datetime, timezone, timedelta

import anthropic
import requests

JST = timezone(timedelta(hours=9))


def get_today_bird_message(date_str: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": f"""今日は {date_str} です。この日付をヒントに、世界の鳥をひとつ選んで紹介してください。

条件：
- 毎日違う鳥が出るよう、日付に合わせて選んでください（例：月・日の数字から連想するなど）
- スズメ・カラス・ハトなど身近な鳥は避けて、世界の珍しい・美しい・面白い鳥を選んでください
- 以下のフォーマットで、200字前後で書いてください
- フォーマット以外の余分な文章は一切追加しないでください

フォーマット：
🐦 今日の鳥：[鳥の名前]
📍 生息地：[主な生息地]
✨ 特徴：[興味深い特徴を2〜3文で]""",
            }
        ],
    )

    return message.content[0].text.strip()


def send_line_message(text: str) -> None:
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": text}],
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(
            f"LINE送信エラー: ステータスコード {response.status_code}\n"
            f"詳細: {response.text}"
        )


def main():
    today = datetime.now(JST).strftime("%Y-%m-%d")
    print(f"[{today}] 今日の鳥メッセージを生成中...")

    try:
        message = get_today_bird_message(today)
    except anthropic.APIError as e:
        print(f"Claude APIエラー: {e}", file=sys.stderr)
        sys.exit(1)

    print("生成されたメッセージ:")
    print(message)
    print()

    try:
        send_line_message(message)
        print("LINEへの送信が完了しました！")
    except RuntimeError as e:
        print(f"LINE送信失敗: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
