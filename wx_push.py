import re
import requests

from config import pushplus_token


# pushplus推送渠道
def pushplus(msg):
    token = pushplus_token
    if token != '':
        pushplus_url = 'http://pushplus.hxtrip.com/send'
        data = {
            'token': token,
            'title': '图书馆自动预约提醒',
            'content': msg,
            'template': 'html'
        }
        r = requests.post(url=pushplus_url, data=data)
        result = re.findall(r'<code>([0-9]{3})</code>', r.text)
        if result[0] == '200':
            print('消息推送成功：' + msg)
        else:
            print('消息推送失败：' + msg)


