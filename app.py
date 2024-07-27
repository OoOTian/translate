from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入CORS
import requests
import hashlib
import time

app = Flask(__name__)
CORS(app)  # 在Flask应用中启用CORS

# 百度翻译
def baidu_translate(q, appid, secretKey):
    from_lang = 'auto'
    to_lang = 'zh'
    salt = str(int(time.time()))  # 使用当前时间戳作为salt
    string_to_sign = appid + q + salt + secretKey
    sign = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()
    url = f'http://api.fanyi.baidu.com/api/trans/vip/translate?q={q}&from={from_lang}&to={to_lang}&appid={appid}&salt={salt}&sign={sign}'
    response = requests.get(url)
    return response.json()

# 网易翻译（有道翻译）
def youdao_translate(q, appKey, secretKey):
    from_lang = 'auto'
    to_lang = 'zh-CHS'
    salt = str(int(time.time()))
    curtime = str(int(time.time()))
    string_to_sign = appKey + q + salt + curtime + secretKey
    sign = hashlib.sha256(string_to_sign.encode('utf-8')).hexdigest()
    url = f'https://openapi.youdao.com/api?q={q}&from={from_lang}&to={to_lang}&appKey={appKey}&salt={salt}&sign={sign}&signType=v3&curtime={curtime}'
    response = requests.get(url)
    return response.json()

@app.route('/translate', methods=['GET'])
def translate():
    q = request.args.get('q')
    service = request.args.get('service', 'baidu')  # 默认为百度翻译
    if q:
        q = q.replace('|', '').replace('#', '')

    if service == 'youdao':
        appKey = '73051c9cf2297c32'  # 替换为你的有道翻译appKey
        secretKey = '8HlzlXMy6OeJ3PX50M7EgfAo88mmJEx2'  # 替换为你的有道翻译secretKey
        result = youdao_translate(q, appKey, secretKey)
    else:
        appid = '20240726002108897'  # 替换为你的百度翻译appid
        secretKey = 'dI1J_GBVXJAHkcofMFub'  # 替换为你的百度翻译密钥
        result = baidu_translate(q, appid, secretKey)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
