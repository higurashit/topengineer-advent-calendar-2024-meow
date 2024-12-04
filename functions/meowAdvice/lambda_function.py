import json
import urllib.request
import os
_env = os.environ

def lambda_handler(event, context):
    # 猫画像取得
    imeowge = getImeowge()

    # 誕生日メッセージ取得
    admeowce = getAdmeowce()
    admeowce_jp = getAdmewceJp(admeowce)
    admeowce_jp = translate_meow(admeowce_jp)

    # LINEに送信
    happyMeowthdayToLine(imeowge, f'{admeowce}\n{admeowce_jp}')

def getImeowge():
    _url = 'https://api.thecatapi.com/v1/images/search'
    imeowge = sendRequest(_url)
    # print(f'imeowge => {imeowge}')
    return imeowge[0]['url']

def getAdmeowce():
    _url = 'https://api.adviceslip.com/advice'
    admeowce = sendRequest(_url)
    # print(f'admeowce => {admeowce}')
    return admeowce['slip']['advice']

def getAdmewceJp(admeowce):
    _url = 'https://api-free.deepl.com/v2/translate'
    _data = urllib.parse.urlencode({
        'auth_key': _env["DEEPL_AUTH_KEY"]
        ,"text": admeowce
        ,"target_lang": "JA"
    }).encode('utf-8')
    _header = {
        "Content-type": "application/x-www-form-urlencoded; utf-8"
    }

    admeowce_jp = sendRequest(_url, _data, _header)
    # print(f'admeowce_jp => {admeowce_jp}')
    return admeowce_jp['translations'][0]['text']

def translate_meow(text):
    _url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    _prompt = "語尾を猫語「～にゃん」に変換して。"
    meow = sendRequest(
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

def happyMeowthdayToLine(imeowge, meowssage):
    _msg = f'Happy Meowthday!!\n{meowssage}'
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
                ,"text": _msg
            }
        ]
    }).encode()
    _header = {
      "Content-type": "application/json; charset=UTF-8",
      "Authorization": "Bearer " + _env["LINE_ACCESS_TOKEN"]
    }
    # print(f'_url, _data, _header => {_url}, {_data}, {_header}')
    sendRequest(_url, _data, _header)

def sendRequest(_url, _data=None, _header={}):

    # print(f'sendRequest: {_url}, {_data}, {_header}')
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