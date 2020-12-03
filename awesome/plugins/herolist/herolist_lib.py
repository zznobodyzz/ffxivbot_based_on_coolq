from common import *
import requests
import json


RAID_DICT_ALIASES=['启动','天动','律动','德尔塔','西格玛']
SERVER_DICT_ALIASES=['拉诺','紫水','幻影','神意','静语','萌芽']


RAID_DICT3={'亚历山大零式机神城启动之章':{'url_index':'','version':2},'亚历山大零式机神城律动之章':{'url_index':'0712','version':2}, \
            '亚历山大零式机神城天动之章':{'url_index':'0220','version':3}}
#TODO
#'欧米茄时空狭缝阿尔法幻境':
RAID_DICT4={'欧米茄零式时空狭缝德尔塔幻境':{'url_index':'20171213','version':4,'ashx':'171213'},'欧米茄零式时空狭缝西格玛幻境':{'url_index':'20180525','version':4,'ashx':'171213'}, \
            '欧米茄零式时空狭缝阿尔法幻境':{'url_index':'20180525','version':5,'ashx':'190128'}}


SERVER_DICT3={'拉诺西亚':{'group_id':[3,3],'area_id':[1,1]},'紫水栈桥':{'group_id':[4,4],'area_id':[1,1]},'幻影群岛':{'group_id':[5,5],'area_id':[1,1]}, \
                '摩杜纳':{'group_id':[6,6],'area_id':[1,1]},'神意之地':{'group_id':[24,24],'area_id':[1,1]},'静语庄园':{'group_id':[23,23],'area_id':[1,1]}, \
                '萌芽池':{'group_id':[1,25],'area_id':[2,1]}}
SERVER_DICT4={'拉诺西亚':3,'紫水栈桥':4,'幻影群岛':5,'摩杜纳':6,'神意之地':23,'静语庄园':24,'萌芽池':25,'延夏':26,'红玉海':27,'潮风亭':61,'神拳痕':62,'白银乡':63,'白金幻象':64}





def get_herolist_raid_name(msg):
    for raid in RAID_DICT3.keys():
        if find_string(msg, raid) != -1:
            return raid
    for raid in RAID_DICT4.keys():
        if find_string(msg, raid) != -1:
            return raid
    for raid in RAID_DICT_ALIASES:
        if find_string(msg, raid) != -1:
            return raid
    return 'None'

def get_herolist_server_name(msg):
    for server in SERVER_DICT4.keys():
        if find_string(msg, server) != -1:
            return server
    for server in SERVER_DICT_ALIASES:
        if find_string(msg, server) != -1:
            return server
    return 'None'




def get_herolist_url(raid_name):
    return_dict = {'url':'None', 'raid_name':'', 'raid_version':0}
    for raid in RAID_DICT4.keys():
        if check_if_match_apart(raid, raid_name) == True:
            return_dict['url'] = 'http://act.ff.sdo.com/' + RAID_DICT4[raid]['url_index'] + 'HeroList/Server/HeroList' + RAID_DICT4[raid]['ashx'] + '.ashx'
            return_dict['raid_version'] = RAID_DICT4[raid]['version']
            return_dict['raid_name'] = raid
            return return_dict
    for raid in RAID_DICT3.keys():
         if check_if_match_apart(raid, raid_name) == True:
            return_dict['url'] = 'http://act.ff.sdo.com/HeroList/Server/HreoList' + RAID_DICT3[raid]['url_index'] +'.ashx'
            return_dict['raid_version'] = RAID_DICT3[raid]['version']
            return_dict['raid_name'] = raid
            return return_dict
    return return_dict


def get_herolist_data(data_list, raid_version):
    ret =  {'data':{ "method":"queryhreodata", \
                    "name":'', \
                    "areaId":'', \
                    'groupId':''}, \
            'errno':0, \
            'server_name':'None'}
    name = data_list[0]
    if len(name) > 6:
       ret['errno'] = 1
       return ret
    server = data_list[1]
    area_id = 0
    group_id = 0

    if raid_version == 2 or raid_version == 3:
        for servers in SERVER_DICT3.keys():
            if check_if_match_apart(servers, server) == True:
                group_id = SERVER_DICT3[servers]['group_id'][raid_version-2]
                area_id = SERVER_DICT3[servers]['area_id'][raid_version-2]
                ret['server_name'] = servers
                break
    elif raid_version == 4:
        for servers in SERVER_DICT4.keys():
            if check_if_match_apart(servers, server) == True:
                group_id = SERVER_DICT4[servers]
                area_id = 1
                ret['server_name'] = servers
                break
    elif raid_version == 5:
        ret['data']['stage'] = '1'
        for servers in SERVER_DICT4.keys():
            if check_if_match_apart(servers, server) == True:
                group_id = SERVER_DICT4[servers]
                area_id = 1
                ret['server_name'] = servers
                break
    ret['data']['name'] = name
    ret['data']['areaId'] = str(area_id)
    ret['data']['groupId'] = str(group_id)
    return ret
    


def get_herolist(url, data, server_name, raid_name, raid_version):
    r = requests.post(url=url,data=data)
    res = json.loads(r.text)
    msg = ''
    msg += '冒险者 ' + data['name'] + '\n'
    msg += '服务器 ' + server_name + '\n'
    date = []
    for i in range(1,5):
        level = "Level{}".format(i)
        if res['Attach'][level] != None and len(res['Attach'][level]) == 8:
            date.append(res['Attach'][level])
        else:
            date.append('None')
    if raid_version < 4:
        raid_name = raid_name[-4:]
    else:
        raid_name = raid_name[-5:]
    for i in range(0,4):
        msg += raid_name + str(i+1) + '层: '
        if date[i] == 'None':
            msg += '无记录'
        else:
            msg += "{}年{}月{}日".format(date[i][:4],date[i][4:6],date[i][6:8])
        msg += '\n'
    return msg.strip()
    

