import re
import requests

from config import pushplus_token


# pushplus推送渠道
def pushplus(msg):
    token = pushplus_token
    if token != '':
        pushplus_url = 'http://www.pushplus.plus/send'
        data = {
            'token': token,
            'title': '图书馆自动预约提醒',
            'content': time.strftime("%m-%d %H:%M:%S", time.localtime(time.time() + 28800)) + '\n' + msg
        }
        r = requests.post(url=pushplus_url, data=data)
        result = json.loads(r.text)
        if result['code'] == 200:
            logger.info('消息推送成功：' + msg)
        else:
            logger.info('消息推送失败：' + msg)


