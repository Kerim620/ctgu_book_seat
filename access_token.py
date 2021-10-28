import re
import time
import requests


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
        print('账号或密码错误，登录失败')
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
        print('名字获取失败')
        name = ''
    else:
        print(result[0] + '登录成功')
        name = result[0]
    return name


# 整合的一个函数
def get_access_token(username, password):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    }
    access_token, name = login(session, username, password)
    # print(access_token)
    return access_token, name
