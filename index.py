import json
import logging
import re
import time
import requests


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger()


# 获取网页中的lt，execution以及cookies(JSESSIONID)
def get_lt_execution(session):
    cas_url = 'http://cas.lib.ctgu.edu.cn/cas/login?service=http://zwyy.lib.ctgu.edu.cn/cas/index.php?callback=http://zwyy.lib.ctgu.edu.cn/home/web/seat/area/1'
    r = session.get(url=cas_url)
    lt = re.findall(r'<input type="hidden" name="lt" value="(.*?)" />', r.text)
    execution = re.findall(r'<input type="hidden" name="execution" value="(.*?)" />', r.text)
    cookie = dict(r.cookies)
    return lt[0], execution[0], cookie


# 登录
def login(session, username, password):
    lt, execution, cookie = get_lt_execution(session)
    way = '&' + time.strftime("%Y%m%d%H%M", time.localtime())
    cas_url = 'http://cas.lib.ctgu.edu.cn/cas/login;jsessionid=' + cookie[
        'JSESSIONID'] + '?service=http%3A%2F%2Fzwyy.lib.ctgu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Fzwyy.lib.ctgu.edu.cn%2Fhome%2Fweb%2Fseat%2Farea%2F1'
    data = {
        'param1': 'http://zwyy.lib.ctgu.edu.cn/cas/index.php?callback=http://zwyy.lib.ctgu.edu.cn/home/web/seat/area/1',
        'param2': '',
        'username': username,
        'password': password,
        'way': way,
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit'
    }
    # 这里会重定向
    r = session.post(url=cas_url, data=data, allow_redirects=False)
    if r.status_code == 200:
        logger.info('账号或密码错误，登录失败')
        pushplus('账号或密码错误，登录失败')
        exit(1)
    # 这里完善cookies，以获取access_token
    session.get(url=r.url)
    name = get_name(session)
    return dict(session.cookies)['access_token'], name


# 获取用户名字
def get_name(session):
    seat_url = 'http://zwyy.lib.ctgu.edu.cn/home/web/seat/area/1'
    r = session.get(url=seat_url)
    result = re.findall(r'target="_blank" >我的中心</a>\s*欢迎(.*?)\s*<a class="logout-btn"', r.text)
    if len(result) == 0:
        logger.info('名字获取失败')
        name = ''
    else:
        logger.info(result[0] + '登录成功')
        name = result[0]
    return name


# 整合的一个函数
def get_access_token(username, password):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    }
    access_token, name = login(session, username, password)
    # logger.info(access_token)
    return access_token, name


# 获取各个具体区域的座位剩余信息
def get_area_info(session, day):
    area_info_url = 'http://zwyy.lib.ctgu.edu.cn/api.php/v3areas/1/date/' + day
    if day == time.strftime("%Y-%m-%d", time.localtime()):
        area_info_url = 'http://zwyy.lib.ctgu.edu.cn/api.php/v3areas/1'
    r = session.get(url=area_info_url)
    result = json.loads(r.text)
    seat_info_list = result['data']['list']['seatinfo']
    area_parent_dict = {}
    area_info = []
    for i in range(len(seat_info_list)):
        if seat_info_list[i]['parentId'] == 1:
            area_parent_dict[seat_info_list[i]['id']] = seat_info_list[i]['name']
        elif seat_info_list[i]['parentId'] > 1:
            # [18,一楼A区,256]
            temp_list = [seat_info_list[i]['id'],
                         area_parent_dict[seat_info_list[i]['parentId']] + seat_info_list[i]['name'],
                         str(int(seat_info_list[i]['TotalCount']) - int(seat_info_list[i]['UnavailableSpace']))]
            area_info.append(temp_list)
    # 打印每层每区域座位剩余信息
    # for item in area_info:
    #     logger.info(item[0] + item[1] + ' 剩余 ' + str(item[2]))


# 获取区域编号对应的名字
def get_area_name(session, area_id):
    area_info_url = 'http://zwyy.lib.ctgu.edu.cn/api.php/v3areas/1'
    r = session.get(url=area_info_url)
    result = json.loads(r.text)
    seat_info_list = result['data']['list']['seatinfo']
    area_parent_dict = {}
    area_info = []
    for i in range(len(seat_info_list)):
        if seat_info_list[i]['parentId'] == 1:
            area_parent_dict[seat_info_list[i]['id']] = seat_info_list[i]['name']
        elif seat_info_list[i]['parentId'] > 1:
            # [18,一楼A区,256]
            temp_list = [str(seat_info_list[i]['id']),
                         area_parent_dict[seat_info_list[i]['parentId']] + seat_info_list[i]['name']]
            area_info.append(temp_list)
    for i in range(len(area_info)):
        if area_info[i][0] == area_id:
            return area_info[i][1]


# 通过area_id获取当前的segment
def get_segment(session, area_id, day):
    segment_url = 'http://zwyy.lib.ctgu.edu.cn/api.php/areadays/' + str(area_id)
    r = session.get(url=segment_url)
    segment = json.loads(r.text)['data']['list'][0]['id']
    if day == 'tomorrow':
        segment = json.loads(r.text)['data']['list'][1]['id']
    # logger.info(segment)
    return segment


# 通过seat_num和segment以及area_id获取对应的seat_id
def get_seat_id(session, area_id, segment, seat_num):
    nowday = time.strftime("%Y-%m-%d", time.localtime())
    nowtime = time.strftime("%H:%M", time.localtime())
    seat_info_url = 'http://zwyy.lib.ctgu.edu.cn/api.php/spaces_old?area=' + str(area_id) + '&segment=' + str(
        segment) + '&day=' + nowday + '&startTime=' + nowtime + '&endTime=22:00'
    r = session.get(url=seat_info_url)
    seat_list = json.loads(r.text)['data']['list']
    for i in range(len(seat_list)):
        if seat_list[i]['name'] == seat_num:
            # logger.info(str(seat_list[i]['id']), seat_list[i]['name'])
            return str(seat_list[i]['id'])


def get_book_data(username, area_id, seat_num, day):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Referer': 'http://zwyy.lib.ctgu.edu.cn/home/web/seat/area/1'
    }
    area_name = get_area_name(session, area_id)
    segment = get_segment(session, area_id, day)
    seat_id = get_seat_id(session, area_id, segment, seat_num)
    book_data = {
        'seat_id': seat_id,
        'seat_num': seat_num,
        'user_id': username,
        'segment': segment,
        'area_name': area_name
    }
    # logger.info('您预约的位置为：【' + area_name + seat_num + '】')
    return book_data


# 通过book_data和access_token来直接预约
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
    # logger.info(result)
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
        logger.info(name + user['username'] + '【' + day + book_data['area_name'] + book_data['seat_num'] + '】' + result['msg'])
        if result['status'] == 1:
            break
        elif result['status'] == 0 and user['seats'].index(seat) == len(user['seats']) - 1:
            pushplus(name + user['username'] + '全部座位预约失败，请及时自行预约')


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
            logger.info('消息推送成功：' + msg)
        else:
            logger.info('消息推送失败：' + msg)


def main():
    for user in users:
        # 云函数不支持多线程线程
        book_seat_user(user)


def main_handler(event, content):
    logger.info('-'*30+'日志开始'+'-'*30)
    main()
    logger.info('-'*30+'日志结束'+'-'*30)


# 用户配置，可以配置多个人的，配置多人的可以用来抢多个邻近的位置(采用多线程实现)
# 项目采用区域编号，座位号，以及日期来唯一定位到座位，即通过配置seats和day来确定位置
# seats为列表，第一位数为区域编号，见下面对应表，第二位为座位号，可以有多个座位号，抢不到就往后顺延
# 例如[['13', '016'], ['15', '020']]代表首选三楼c区016座位，其次选四楼b区020座位
# day为字符串，只能填today或tomorrow，意思是抢当天的还是第二天的位置
users = [
    {
        'username': '2019123456',
        'password': '123456',
        'seats': [['13', '018']],
        'day':'today'
    },
    {
        'username': '2020123456',
        'password': '255555',
        'seats': [['13', '009'], ['13', '021']],
        'day':'tomorrow'
    }
]
# 登录\预约失败会推送消息，采取pushplus推送渠道，请自行注册获取token，如不想受到推送请留空
pushplus_token = 'f1d396a853bb4821931cbc6200812345'


main()
# 图书馆各个区域对应的区域编号
# 7 一楼C区
# 8 二楼A区
# 9 二楼B区
# 10 二楼C区
# 11 三楼A区
# 12 三楼B区
# 13 三楼C区
# 14 四楼A区
# 15 四楼B区
# 16 四楼C区
# 17 四楼A电子阅览室K
# 18 四楼自主学习空间
# 19 五楼A区
# 20 五楼B区
# 21 五楼C区