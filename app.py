from flask import Flask, escape, request, render_template
from decouple import config
from bs4 import BeautifulSoup
import requests
import random
import html

app = Flask(__name__)

api_url = "https://api.telegram.org/bot"
token = config("TELEGRAM_BOT_TOKEN")
google_key = config("GOOGLE_KEY")
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
    keyword = ['로또', '번역', '국내증시']
    req = request.get_json()
    user_id = req['message']['from']['id']
    user_input = req['message']['text'] 

    numbers = list(range(1,46))
    lucky = random.sample(numbers, 6)
    sorted_lucky = sorted(lucky)

    naver_sise_url = "https://finance.naver.com/sise/"
    res = requests.get(naver_sise_url).text
    naver_soup = BeautifulSoup(res, "html.parser")
    kospi = naver_soup.select_one("#KOSPI_now").text
    kospi_change = naver_soup.select_one("#KOSPI_change").text.replace("\n","")
    kosdaq = naver_soup.select_one('#KOSDAQ_now').text
    kosdaq_change = naver_soup.select_one('#KOSDAQ_change').text.replace("\n","")

    if user_input == keyword[0]:
        return_data = f" 로또를 입력하셨습니다. 번호는{sorted_lucky}."
    elif user_input[0:3] == keyword[1]:
        google_api_url = 'https://translation.googleapis.com/language/translate/v2'
        before_text = user_input[3:]
 
        data = {
            'q':before_text,
            'source':'ko',
            'target':'en',
        }
        request_url = f'{google_api_url}?key={google_key}'

        res = requests.post(request_url, data).json()
        print(res)
        after_text = res['data']['translations'][0]['translatedText']
        unescape_text = html.unescape(after_text)
        print(unescape_text)
        return_data = f"{unescape_text}번역완료"
    elif user_input == keyword[2]:
        return_data = f"현재 코스피 : {kospi} \
                        \n 증감률 : {kospi_change}\
                        \n\n 현재 코스닥 : {kosdaq}\
                        \n 증감률 : {kosdaq_change}"

    else:
        return_data = "지금 사용 가능한 명령어는 로또 입니다."

    send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}"
    requests.get(send_url)

    return "ok" , 200


if __name__ == '__main__':
    app.run(debug=True)