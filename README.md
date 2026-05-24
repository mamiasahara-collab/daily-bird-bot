# 毎日の鳥 LINE Bot 🐦

毎朝7時（日本時間）に、世界の珍しい鳥の情報をLINEに自動送信するBotです。

---

## 送信メッセージのイメージ

```
🐦 今日の鳥：ケツァール
📍 生息地：中米（グアテマラなど）
✨ 特徴：世界一美しいとも言われる鳥。尾羽が最大1mになる。古代マヤ文明では神聖な存在とされていた。
```

---

## セットアップ手順

### 1. このリポジトリをGitHubに作成する

1. [GitHub](https://github.com) にログイン
2. 右上の「＋」→「New repository」をクリック
3. リポジトリ名を入力（例：`daily-bird-bot`）して作成
4. このフォルダの中身をそのままアップロード（またはgit pushする）

---

### 2. LINE Messaging APIの準備

1. [LINE Developers](https://developers.line.biz/) にアクセスしてログイン
2. 「プロバイダー」→「新規プロバイダー作成」
3. 「チャネル作成」→「Messaging API」を選択
4. チャネル作成後、「Messaging API設定」タブを開く
5. 「チャネルアクセストークン（長期）」の「発行」ボタンをクリックしてコピー（`LINE_CHANNEL_ACCESS_TOKEN`）
6. 自分のLINEアカウントのユーザーIDを確認する（下記参照）

**ユーザーIDの確認方法：**
- 「チャネル基本設定」→「あなたのユーザーID」に表示されています（`LINE_USER_ID`）

---

### 3. GitHub Secretsに環境変数を登録する

GitHubのリポジトリページで：

1. 上部の「Settings」タブをクリック
2. 左メニュー「Secrets and variables」→「Actions」を開く
3. 「New repository secret」ボタンで以下の3つを登録する

| Name | 値 |
|------|-----|
| `ANTHROPIC_API_KEY` | Anthropicのダッシュボードで取得したAPIキー |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Developersで発行したトークン |
| `LINE_USER_ID` | 自分のLINEユーザーID |

---

### 4. 動作確認（手動送信テスト）

1. GitHubのリポジトリページで「Actions」タブを開く
2. 左側の「毎日の鳥 LINE Bot」をクリック
3. 右側の「Run workflow」→「Run workflow」ボタンをクリック
4. 数秒後、LINEにメッセージが届けばOK！

---

## 自動実行のスケジュール

毎朝 **7:00（日本時間）** に自動で送信されます。  
GitHub Actionsの仕様上、数分の誤差が生じることがあります。

---

## エラーが起きたときの確認方法

1. GitHubの「Actions」タブを開く
2. 赤い「✗」がついている実行をクリック
3. 「send-bird」のステップを開くとエラーの詳細が表示されます

よくある原因：
- Secretsの登録ミス（スペルや余分なスペースに注意）
- LINE Messaging APIのチャネルが「停止中」になっている
- Anthropic APIの残高不足
