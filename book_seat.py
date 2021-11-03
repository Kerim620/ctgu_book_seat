import json
import threading
import time
import requests

from access_token import get_access_token
from config import users
from seat_info import get_book_data


# 通过book_data和access_token来直接预约
from wx_push import pushplus


def book_seat(book_data, access_token):
    url = 'http://zwyy.lib.ctgu.edu.cn/api.php/spaces/' + book_data['seat_id'] + '/book'
    data = {
        'access_token': access_token,
        'userid': book_data['user_id'],
        'segment': book_data['segment'],
        'type': '1',
        'operateChannel': '2',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Referer': 'http://zwyy.lib.ctgu.edu.cn/web/seat3'
    }
    r = requests.post(url=url, data=data, headers=headers)
    result = json.loads(r.text)
    # print(result)
    return result


# 只有config的user，调用book_seat()一步步预约
def book_seat_user(user):
    access_token, name = get_access_token(user['username'], user['password'])
    for seat in user['seats']:
        book_data = get_book_data(user['username'], seat[0], seat[1], user['day'])
        day = time.strftime("%m-%d", time.localtime())
        if user['day'] == 'tomorrow':
            day = time.strftime("%m-%d", time.localtime(time.time() + 86400))
        result = book_seat(book_data, access_token)
        print(name + user['username'] + '【' + day + book_data['area_name'] + book_data['seat_num'] + '】' + result['msg'])
        if result['status'] == 1:
            break
        elif result['status'] == 0 and user['seats'].index(seat) == len(user['seats'])-1:
            pushplus(name + day + '全部座位预约失败，请及时自行预约')


def main():
    for user in users:
        # 每个用户分配一条线程
        t = threading.Thread(target=book_seat_user, name=user['username'], args=(user,))
        t.start()


if __name__ == '__main__':
    main()
