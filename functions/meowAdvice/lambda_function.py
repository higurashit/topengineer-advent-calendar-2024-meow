import json
import urllib.request
import os
_env = os.environ

def lambda_handler(event, context):
    # 猫の名前を取得
    name = get_name(event)

    # 猫画像取得
    imeowge = get_imeowge()

    # アドバイス取得
    admeowce = get_admeowce()
    admeowce_jp = get_admeowce_jp(admeowce)
    admeowce_jp = translate_meow(admeowce_jp)

    # メッセージ
    meowssage = f'{name}「{admeowce_jp} ({admeowce}) 」'

    # LINEに送信
    post_admeowce_to_line(imeowge, meowssage)

def get_name(event):
    default_cat_name = 'Cat'
    return event.key('name', default_cat_name)

def get_imeowge():
    _url = 'https://api.thecatapi.com/v1/images/search'
    imeowge = send_request(_url)
    # print(f'imeowge => {imeowge}')
    return imeowge[0]['url']

def get_admeowce():
    _url = 'https://api.adviceslip.com/advice'
    admeowce = send_request(_url)
    # print(f'admeowce => {admeowce}')
    return admeowce['slip']['advice']

def get_admeowce_jp(admeowce):
    _url = 'https://api-free.deepl.com/v2/translate'
    _data = urllib.parse.urlencode({
        'auth_key': _env["DEEPL_AUTH_KEY"]
        ,"text": admeowce
        ,"target_lang": "JA"
    }).encode('utf-8')
    _header = {
        "Content-type": "application/x-www-form-urlencoded; utf-8"
    }

    admeowce_jp = send_request(_url, _data, _header)
    # print(f'admeowce_jp => {admeowce_jp}')
    return admeowce_jp['translations'][0]['text']

def translate_meow(text):
    _url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    _prompt = "語尾を猫語「～にゃん」に変換して。"
    meow = send_request(
        f'{_url}?key={_env["GEMINI_API_KEY"]}'
        , _data=json.dumps({
                "contents": [{
                    "parts": [{
                        "text": f'{_prompt}\n- {text}'
                    }]
                }]
            }).encode()
        , _header={"Content-Type": "application/json"}
    )
    # print(meow)
    ret = meow["candidates"][0]["content"]["parts"][0]["text"]
    return ret.rstrip("\n")

def post_admeowce_to_line(imeowge, meowssage):
    _url = 'https://api.line.me/v2/bot/message/push'
    _data = json.dumps({
        "to": _env["LINE_USER_ID"]
        ,"messages": [
            # imeowge
            {
                "type": "image"
                , "originalContentUrl": imeowge
                , "previewImageUrl": imeowge
            }
            # meowssage
            ,{
                "type": "text"
                ,"text": meowssage
            }
        ]
    }).encode()
    _header = {
      "Content-type": "application/json; charset=UTF-8",
      "Authorization": "Bearer " + _env["LINE_ACCESS_TOKEN"]
    }
    send_request(_url, _data, _header)

def send_request(_url, _data=None, _header={}):
    # print(f'send_request: {_url}, {_data}, {_header}')
    _req = urllib.request.Request(_url, _data, _header)
    try:
        with urllib.request.urlopen(_req) as _res:
            _body = json.loads(_res.read().decode())
            return _body

        raise Exception('No Meow!!')
    except urllib.error.HTTPError as _err:
        print("HTTPError: " + str(_err.code))
        print(_err)
    except urllib.error.URLError as _err:
        print("HTTPError: " + _err.reason)
        print(_err)
    except Exception as e:
        raise e
