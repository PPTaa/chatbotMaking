import requests
from decouple import config
tokten = config("TELEGRAM_BOT_TOKEN")
# 챗봇 사용자의 정보를 알아올때 사용하는 메서드 getMe
url = f"https://api.telegram.org/bot{tokten}/getUpdates"

# str형식을 dictionary 형식으로 형 변환
res = requests.get(url).json()
user_input = input("보낼 매세지를 입력")
user_id = res["result"][-1]["message"]["from"]["id"]
send_url = f"https://api.telegram.org/bot{tokten}/sendMessage?text={user_input}&chat_id={user_id}"
requests.get(send_url)


