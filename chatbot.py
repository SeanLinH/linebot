import openai
import requests
import urllib.request 
# from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json


# search something from google
def search_google(query):
    url = "https://www.google.com/search?q={}".format("簡單清楚, " + query + " lang:tw,en")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.text
    text = text[text.find('id="search"'):]
    text = text[text.find('<a jsname'):]
    text = text[text.find('href')+6:]
    text = text[:text.find('"')]
    
    if 'http' not in text:
        return ''
    elif str(response) == "<Response [429]>":
        return '\n\n我累了🥵, 休息一下喝口水'
    elif 'porn' in text:
        return '\n\n你不可以色色唷😚'
    elif 'xvideo' in text:
        return '\n\n你不可以色色唷😚'   
    return '\n\n幫你找找:' + text


app = Flask(__name__)
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    
    try:
        line_bot_api = LineBotApi('WYXhQWYll5Elwbr/BkZu2SlwUy9AprC88LVLoNrAuJAfB3DbfsWn1I5av2shMKKcFf9CJdNjY0nN6nH09EM+R0Riuek1Z/LdgYP50bJ7xjmMPJk0PS/juq1AeB+n8un8O9fvzKhzzmr7Vj96ZisuygdB04t89/1O/w1cDnyilFU=')
        handler = WebhookHandler('e9ac54a45e76a8971b89053e358726fe')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text'] + '.'
        user = json_data["events"][0]["source"]["userId"]
        # 取出文字的前五個字元，轉換成小寫
        ai_msg = msg[:1].lower()
        reply_msg = ''
        print(f'{user}: {msg}')
        with open(f'log/{user}.txt', 'a') as f:
            f.write(msg)
            f.close()
        
        mem = open(f'log/{user}.txt', 'r').read()

        if len(mem) > 2000:
            with open(f'log/{user}.txt', 'w') as f:
                f.write(mem[-2000:])
                f.close()
            mem = mem[-2000:]

        
        if msg[:6] == 'remove':
            open(f'log/{user}.txt', 'w').write("")
            text_message = TextSendMessage(text='Your record has been cleared!')
            line_bot_api.reply_message(tk,text_message)
            print('cleared!!')
        elif ai_msg == '/':
            openai.api_key = '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'
            # 將第六個字元之後的訊息發送給 OpenAI
            response = openai.ChatCompletion.create(
                model= 'gpt-4', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.9,
                messages=[
                    {
                    "role": "system",
                    "content": "My name is Sean (林士桓), a dedicated AI engineer from Taiwan, currently serving in a PCB manufacturing company. \
                                I possess profound expertise and passion in AI, encompassing training, deployment, and application. \
                                My competencies extend to image processing, object recognition, YOLO, deep learning, machine learning, OpenCV, PyTorch, CNN, feature extraction, image segmentation, and model fine-tuning. \
                                As a 30-year-old professional, I am not only enthusiastic about embracing new challenges but also consistently expanding my network. \
                                Currently, I am actively seeking opportunities to transition to an overseas company, aspiring to further enhance my professional capabilities and career progression. \
                                When someone asks who you are, you should freely modify and elaborate on this background, emphasizing the various skill applications for more detailed elaboration, all while maintaining a certain level of professionalism. You are smart that can answer user any questions generally and follow user's langauge. Do not answer unclearly or don't know"
                    },
                    {
                        "role": "user",
                        "content": mem.replace('\n','')
                    }
                    
                ]
                )
            with open(f'log/record.txt', 'a') as ff:
                ff.write(msg[1:] + '\n')
                ff.close()

            

            # 接收到回覆訊息後，移除換行符號
            reply_msg = response["choices"][0]['message']['content']

            key_point = openai.ChatCompletion.create(
                model= 'gpt-4', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": "You are a good at summarizing paragrph, and you just output 1 keypoint. You can output up to 5 words"
                    },
                    {
                        "role": "user",
                        "content": reply_msg.replace('\n','')  
                    }
                    
                ]
                )
            
            print(key_point["choices"][0]['message']['content'])
            url = search_google(key_point["choices"][0]['message']['content']+ '. ' + msg[1:])

            with open(f'log/{user}.txt', 'w') as f:
                f.write(mem + reply_msg + '\n')
                f.close()

            text_message = TextSendMessage(text=reply_msg + url)
            line_bot_api.reply_message(tk,text_message)
        else:
            reply_msg = msg
        
    except:
        print('error')
    return 'OK'

if __name__ == "__main__":
    # run_with_ngrok(app)   # colab 使用，本機環境請刪除
    app.run()
