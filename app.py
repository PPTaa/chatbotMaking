from flask import Flask, escape, request, render_template
from decouple import config
import requests
app = Flask(__name__)

api_url = "https://api.telegram.org/bot"
token = config("TELEGRAM_BOT_TOKEN")
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route("/write")
def write():
    return render_template("write.html")

@app.route("/send")
def send():
    user_input = request.args.get("user_input")
    get_user_api = f"{api_url}{token}/getUpdates"

    res = requests.get(get_user_api).json()
    
    user_id = res["result"][0]["message"]["from"]["id"]

    send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={user_id}"
    requests.get(send_url)
    return render_template("send.html")

#telegram에서 보낸 메세지를 flask와 연결하는 작업
#번외 local 서버를 외부에서 접속 하는 방법중 ngrok을 사용해 서버를 받을 수 있다. 서버 설정은 ./ngrok http 5000 = flask에 설정되어 있는 5000이라는 포트 번호 -> 개발자 모드 최대 사용 시간 7시간
@app.route(f"/telegram" , methods = ["POST"])
def telegram():
    req = request.get_json()
    user_id = req['message']['from']['id']
    user_input = req['message']['text']

    if user_input == "로또":
        return_data = " 로또를 입력하셨습니다."
    else:
        return_data = "지금 사용 가능한 명령어는 로또 입니다."

    send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}"
    requests.get(send_url)

    return "ok" , 200

if __name__ == '__main__':
    app.run(debug=True)