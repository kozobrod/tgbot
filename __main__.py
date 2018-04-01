import requests
import pandas as pd
import sys


from time import sleep
#tokenfile=open(file='token',mode='r')
#mytoken = tokenfile.read()
#tokenfile.close()
mytoken = sys.argv[1]

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=0, limit=None):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset, 'limit':limit}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return last_update

def get_weather():
    url='https://yandex.ru/pogoda/moscow/details'
    df = pd.read_html(url)
    weather = []
    for i in range(len(df[0]['Unnamed: 0'])):
        weather.append(str(df[0]['Unnamed: 0'][i])+' '+str(df[0]['Влажность'][i])+'    ')
    weather=str(weather).replace('[','').replace(']','').replace("'",'').lower()
    return weather

def main():
    bot = BotHandler(mytoken)
    last_msg_id_known='0'
    while True:
        all_msgs = bot.get_updates()
        last_msg = str(all_msgs[-1]['message']['text']).lower()
        last_msg_id= all_msgs[-1]['message']['message_id']
        last_chat_id = all_msgs[-1]['message']['chat']['id']
        print(last_msg_id,last_msg_id_known,last_msg,last_chat_id)
        if last_msg_id != last_msg_id_known:
            if last_msg =='weather':
                bot.send_message(text="Погода на сегодня : "+str(get_weather()), chat_id=last_chat_id)
            last_msg_id_known=last_msg_id
        sleep(10)

print(__name__)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
print('test commit')
