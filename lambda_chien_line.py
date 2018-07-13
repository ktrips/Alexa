import requests

import urllib.request
import json

# Chien Json
CHIEN_URL = 'https://rti-giken.jp/fhc/api/train_tetsudo/delay.json'

# Get Chien JSON
def get_chien(keyword):
    req = urllib.request.Request(CHIEN_URL)
    with urllib.request.urlopen(req) as res:
    #res  = urllib2.urlopen(CHIEN_URL)
        datas= json.loads(res.read())
        results = ""
        for data in datas:
            chien_train = data["name"] + "(" + data["company"] + ") "
            if chien_train.find(keyword) > -1:
                results += chien_train
                    
    return results
    
def lambda_handler(event, context):
    if event['request']['type'] == "IntentRequest":
        intent = event['request']['intent']
        slot = intent['slots']['MessageType']['value']

        url = "https://notify-api.line.me/api/notify"

        # LINE Token
        token = "c3EkzehGnZvpEgAtw1iTMjsU4NZVi7echeVgvtWXamQ"
        headers = {"Authorization" : "Bearer "+ token}
        
        chien_result = get_chien(slot)
        if chien_result:
            message = chien_result + "は遅延しています！"
        else:
            message = slot + "は遅延していません！"
            
        payload = {"message" :  message}
        r = requests.post(url ,headers = headers ,params=payload)

        talk_message = str(message) + "ラインにも通知しました！"
        # リマインドメッセージがある場合はラインに通知してアプリを終える
        endSession = True
    else:
        keyword = "東日本"
        chien_test = get_chien(keyword)
        talk_message = "とりあえず、"
        talk_message+= chien_test+"は遅延中！" if chien_test else keyword + "は遅延してません！"
        talk_message+= "小田急線の遅れ？地下鉄の遅延は？などと聞いてみてください！"
        # リマインドメッセージがない場合は何をリマインドするか確認する
        endSession = False

    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': talk_message
            },
            "shouldEndSession": endSession
        }
    }
    return response

