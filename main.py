from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)
import os

app = Flask(__name__)

# チャネルシークレットを設定
YOUR_CHANNEL_SECRET = "XXX"
# チャネルアクセストークンを設定
YOUR_CHANNEL_ACCESS_TOKEN = "XXX"

# LINEbotAPI について定義
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# https://example.herokuapp.com/callback にアクセスされたら以下の関数を実行する
@app.route("/callback", methods=['POST'])
def callback():
    # アクセス時に送られてきたデータ「X-Line-Signature」を、変数sigunatureに代入する
    signature = request.headers['X-Line-Signature']

    # アクセス時に送られてきたデータの主な部分を、変数bodyに代入する
    body = request.get_data(as_text=True)

    # エラーが起きることを覚悟にとりあえずプログラムを実行してみる！
    try:
        # 問題なければハンドラーに定義されている関数を呼び出す
        handler.handle(body, signature)
    # もし「InvalidSigunatureError」というエラーが発生したら、以下のプログラムを実行する！
    except InvalidSignatureError:
        # リクエストを送った側に400番(悪いリクエストですよー！)と言う
        abort(400)

    # すべて順調にいけば、リクエストを送った側に「OK」と言う
    return "OK"

# ハンドラーに定義されている関数
# ここにメッセージの内容による処理を書いていこう
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # プロフィールを取得
    profile = line_bot_api.get_profile(event.source.user_id)
    # テキストメッセージが送られてきたなら
    if event.type == "message":
        # 返す言葉
        response_message = ""

        if (event.message.text == "おはようございます"):
            response_message = "おはようー！"
        elif (event.message.text == "こんにちは"):
            response_message = "こんにちはー！"
        elif (event.message.text == "こんばんは"):
            response_message = "こんばんはー！"
        elif (event.message.text == "好きな食べものはなんですか？"):
            response_message = "寿司！"
        elif (event.message.text == "確認"):
            response_message = "普通のやつ: {}\nよく使われるやつ: {}".format(profile.user_id, profile.user_id[:5])
        else:
            response_message = "何その言葉？"

        # 返信文を送信
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=response_message)
            ]
        )

# ポート番号をHerokuの実行設定から取得
port = os.getenv("PORT")
app.run(host="0.0.0.0", port=port)