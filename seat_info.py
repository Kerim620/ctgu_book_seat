import time
import json
import requests


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
    #     print(item[0] + item[1] + ' 剩余 ' + str(item[2]))


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
    # print(segment)
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
            # print(str(seat_list[i]['id']), seat_list[i]['name'])
            return str(seat_list[i]['id'])


def get_book_data(username, area_id, seat_num, day):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
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
    # print('您预约的位置为：【' + area_name + seat_num + '】')
    return book_data
