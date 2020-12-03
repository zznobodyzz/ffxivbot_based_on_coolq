from common import *
import requests
import urllib.parse as cparse
from bs4 import BeautifulSoup
SERVER_LIST=('拉诺西亚','紫水栈桥','幻影群岛','摩杜纳','神意之地','静语庄园','萌芽池','延夏','红玉海','潮风亭','神拳痕','白银乡','白金幻象')
SERVER_LIST_JP=('Aegis','Atomos','Carbuncle','Garuda','Gungnir','Ramuh','Tonberry','Typhon','Unicorn','Alexander','Bahamut','Durandal','Fenrir', \
                'Ifrit','Ridill','Tiamat','Ultima','Valefor','Yojimbo','Zeromus','AnimaAsura','Belias','Chocobo','Hades','Ixion','Mandragora', \
                'Masamune','Pandaemonium','Shinryu','Titan')
SERVER_LIST_NA=('Adamantoise','Balmung','Cactuar','Cocurl','Facric','Gilgamesh','Goblin','Jenova','Mateus','Midgardsormr','Sargatanas','Siren', \
                'Zalera','Behemoth','Brynhildr','Diabolos','Excalibur','Exodus','Famfrit','Hyperion','Lamia','Leviathan','Malboro','Ultros')
SERVER_LIST_EU=('Cerberus','Lich','Louisoix','Moogle','Odin','Omega','Phoenix','Ragnarok','Shiva','Zodiark')
job_dict = {'占星':'Astrologian','诗人':'Bard','黑魔':'BlackMage','暗骑':'DarkKnight','黑骑':'DarkKnight','龙骑':'Dragoon','机工':'Machinist', \
            '武僧':'Monk','忍者':'Ninja','骑士':'Paladin','学者':'Scholar','召唤':'Summoner','战士':'Warrior','白魔':'WhiteMage', \
            '赤魔':'RedMage','武士':'Samurai', '舞娘':'Dancer' ,'枪刃':'Gunbreaker',\
            '暗黑骑士':'DarkKnight','龙骑士':'Dragoon','机工师':'Machinist','白魔法师':'WhiteMage','吟游诗人':'Bard',\
            '黑魔法师':'BlackMage','召唤师':'Summoner','赤魔法师':'RedMage','占星术士':'Astrologian','绝枪战士':'Gunbreaker','舞者':'Dancer'}

zone_dict = {'阿尔法':'25','西格玛':'21','伊甸':'29','4.0极神':'15','5.0极神':'28'}

'''4.0 bosses'''
domain_sigma_boss_dict = {'魔列车':'51','恶魔查达努克':'52','守护者':'53','凯夫卡':'55','凯夫卡-门神':'54','凯夫卡-本体':'55', \
                            'o5s':'51','o6s':'52','o7s':'53','o8s':'55','O5S':'51','O6S':'52','O7S':'53','O8S':'55'}
domain_alpha_boss_dict = {'卡奥斯':'60','尘世幻龙':'61','欧米茄':'62','双生欧米茄':'63','至尊欧米茄':'64','终极欧米茄':'64','门神':'63','本体':'64', \
                            'o9s':'60','o10s':'61','o11s':'62','o12s':'64','O9S':'60','O10S':'61','O11S':'62','O12S':'64'}
domain_trail_boss_dict4 = {'极豪神':'1036','极美神':'1037','极神龙':'1038','极白虎':'1039','极月读':'1040','极朱雀':'1041','豪神':'1036', \
                            '美神':'1037','神龙':'1038','白虎':'1039','月读':'1040','朱雀':'1041'}
'''5.0 bossess'''
domain_edengate_boss_dict = {'至尊伊甸':'65','虚无行者':'66','利维亚桑':'67','泰坦':'68'}
domain_trail_boss_dict5 = {'极妖精王':'1045','极妖精':'1045','极妖灵王':'1045','妖灵王':'1045','缇妲妮娅':'1045','极完美神':'1046','极肥宅':'1046','无瑕灵君':'1046'}

job_list = list(job_dict.keys())
boss_list = list(domain_sigma_boss_dict.keys()) + list(domain_alpha_boss_dict.keys()) + \
            list(domain_edengate_boss_dict.keys()) + \
            list(domain_trail_boss_dict4.keys()) + list(domain_trail_boss_dict5.keys())


def calc_dps_percent(logs_dps, dps_dict):
    index = 7
    dps_value_list = list(dps_dict.values())
    dps_key_list = list(dps_dict.keys())
    for dps in dps_value_list:
        dpsn = int(dps.rstrip('\n'))
        if logs_dps > dpsn:
            index = dps_value_list.index(dps)
            break
        elif logs_dps == dpsn:
            return int(dps_key_list[dps_value_list.index(dps)])
    if index == 0:
        return 100.0
    elif index == 7:
        return 10.0
    else:
        return (logs_dps - int(dps_value_list[index])) / (int(dps_value_list[index - 1]) - int(dps_value_list[index])) * (int(dps_key_list[index - 1]) - int(dps_key_list[index])) + int(dps_key_list[index])
    

async def get_logs(url: str) -> str:
    web_data = requests.get(url)
    data={}
    #data['100'] = search_data(web_data.text, '<td class="main-table-number primary">') + "\n"
    data['99'] = search_data(web_data.text, 'series99.data.push').replace('(','').replace(')','').split('.')[0] + "\n"
    data['95'] = search_data(web_data.text, 'series95.data.push').replace('(','').replace(')','').split('.')[0] + "\n"
    data['75'] = search_data(web_data.text, 'series75.data.push').replace('(','').replace(')','').split('.')[0] + "\n"
    data['50'] = search_data(web_data.text, 'series50.data.push').replace('(','').replace(')','').split('.')[0] + "\n"
    data['25'] = search_data(web_data.text, 'series25.data.push').replace('(','').replace(')','').split('.')[0] + "\n"
    data['10'] = search_data(web_data.text, 'series10.data.push').replace('(','').replace(')','').split('.')[0]
    return data

def get_logs_url(element):
    global job_dict
    global domain_sigma_boss_dict
    global domain_alpha_boss_dict
    global domain_edengate_boss_dict
    global domain_trail_boss_dict4
    global domain_trail_boss_dict5
    analy={'boss':'','job':'','error':0,'url':'','logs_dps':0}
    if element[0] in domain_alpha_boss_dict.keys():
        boss_id = domain_alpha_boss_dict[element[0]]
        zone = "25"
    elif element[0] in domain_sigma_boss_dict.keys():
        boss_id = domain_sigma_boss_dict[element[0]]
        zone = "21"
    elif element[0] in domain_edengate_boss_dict.keys():
        boss_id = domain_edengate_boss_dict[element[0]]
        zone = "29"
    elif element[0] in domain_trail_boss_dict4.keys():
        boss_id = domain_trail_boss_dict4[element[0]]
        zone = "15"
    elif element[0] in domain_trail_boss_dict5.keys():
        boss_id = domain_trail_boss_dict5[element[0]]
        zone = "28"
    else:
        analy['error'] = 1
        analy['error_msg'] = '不支持的副本'
        return analy
        
    if element[1] in job_dict.keys():
        job_id = job_dict[element[1]]
    else:
        analy['error'] = 1
        analy['error_msg'] = '职业名未识别'
        return analy

    analy['boss'] = element[0]
    analy['job'] = element[1]
    if element[-1].isdigit() == True:
        analy['logs_dps'] = int(element[-1])
    if '国服' in element:
        analy['url'] = "https://cn.fflogs.com/zone/statistics/table/" + zone + "/dps/" + boss_id + "/100/8/5/100/1/14/1/Global/" + job_id + "/All/0/normalized/single/0/-1/?keystone=15&dpstype=rdps"
    else:
        analy['url'] = "https://www.fflogs.com/zone/statistics/table/" + zone + "/dps/" + boss_id + "/100/8/3/100/1/14/0/Global/" + job_id + "/All/0/normalized/single/0/-1/?keystone=15&dpstype=rdps"
    return analy
    
def get_server_official_name(server_alias, server_list):
    for server in server_list:
        if find_string(server, server_alias) != -1:
            return server
    return None

def get_player_hompage_url(element):
    global SERVER_LIST
    server_name = get_server_official_name(element[1], SERVER_LIST)
    if server_name is not None:
        return 'https://www.fflogs.com/character/cn/' + cparse.quote(server_name) + '/' + cparse.quote(element[0]), '5', server_name
    global SERVER_LIST_JP
    server_name = get_server_official_name(element[1], SERVER_LIST_JP)
    if server_name is not None:
        return 'https://www.fflogs.com/character/jp/' + server_name.lower() + '/' + cparse.quote(element[0].lower().replace('+',' ')), '3', server_name
    global SERVER_LIST_NA
    server_name = get_server_official_name(element[1], SERVER_LIST_NA)
    if server_name is not None:
        return 'https://www.fflogs.com/character/na/' + server_name.lower() + '/' + cparse.quote(element[0].lower().replace('+',' ')), '3', server_name
    global SERVER_LIST_EU
    server_name = get_server_official_name(element[1], SERVER_LIST_EU)
    if server_name is not None:
        return 'https://www.fflogs.com/character/eu/' + server_name.lower() + '/' + cparse.quote(element[0].lower().replace('+',' ')), '3', server_name
    return None, None, None
    
    
def get_log_details_url(element):
    analy = {}
    analy['error'] = 0
    zone = ''
    if len(element) == 3:
        if element[2] in job_dict.keys():
            job_id = job_dict[element[2]]
        else:
            analy['error'] = 1
            analy['error_msg'] = '职业名未识别'
            return analy
        if len(element) == 4:
            global zone_dict
            if element[3] in zone_dict.keys():
                zone = zone_dict[element[3]]
            else:
                analy['error'] = 1
                analy['error_msg'] = '不支持的副本'
                return analy
    else:
        job_id = 'Any'
        
    url, country, server_official_name = get_player_hompage_url(element)
    if url == None:
        analy['error'] = 1
        analy['error_msg'] = '服务器名未识别'
        return analy
    try:
        web_data = requests.get(url)
    except Exception as e:
        analy['error'] = 1
        analy['error_msg'] = '与fflogs网站通信错误'
        return analy
    character_id = search_data(web_data.text, 'varcharacterID=').rstrip(';')
    if character_id == ' ':
        analy['error'] = 1
        analy['error_msg'] = '未找到该玩家'
        return analy
    else:
        analy['url'] = []
        if zone == '':
            analy['url'].append('https://www.fflogs.com/character/rankings-detailed/' + character_id + '/dps/28/0/100/8/' + country + '/' + job_id + '/rankings/0/0?dpstype=rdps')
            analy['url'].append('https://www.fflogs.com/character/rankings-detailed/' + character_id + '/dps/29/0/101/8/' + country + '/' + job_id + '/rankings/0/0?dpstype=rdps')
        else:
            analy['url'].append('https://www.fflogs.com/character/rankings-detailed/' + character_id + '/dps/' + zone + '/0/100/8/' + country + '/' + job_id + '/rankings/0/0?dpstype=rdps')
        analy['server_official_name'] = server_official_name
    return analy

async def get_log_details(url: list) -> dict:
    data = {}
    for u in url:
        head={'Accept':'text/html, */*; q=0.01', \
                'Accept-Encoding':'gzip, deflate, br', \
                'Accept-Language':'zh-CN,zh;q=0.9', \
                'Connection':'keep-alive', \
                'Host':'www.fflogs.com', \
                'Referer':'https://www.fflogs.com/character/id/11966651?zone=28&mode=detailed', \
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', \
                'X-Requested-With':'XMLHttpRequest'}
        try:
            web_data = requests.get(u,headers=head)
        except Exception as e:
            return None
        lines = web_data.text.split('\n')
        find_data = 0
        boss = ''
        for line in lines:
            if line == '':
                continue
            if find_data == 0:
                index1 = find_string(line, 'class="Boss">')
                index2 = find_string(line, '</a>')
                if index1 != -1 and index2 != -1:
                    boss = line[index1 + len('class="Boss">'):index2]
                    data[boss] = {}
                    find_data = 1
            elif find_data == 1:
                if line[-3:].isdigit() == True:
                    data[boss]['blogs'] = line[-3:]
                    find_data = 2
                elif line[-2:].isdigit() == True:
                    data[boss]['blogs'] = line[-2:]
                    find_data = 2
                elif line[-1:].isdigit() == True:
                    data[boss]['blogs'] = line[-1:]
                    find_data = 2
                else:
                    find_data = 0
                    data.pop(boss)
            elif find_data == 2:
                global job_dict
                for cjob,ejob in job_dict.items():
                    if ejob in line:
                        data[boss]['job'] = cjob
                        find_data = 3
                        break
                if find_data != 3:
                    data[boss]['job'] = 'Unknown'
                    find_data = 3
            elif find_data == 3:
                if '>' in line and line.index('>') < len(line) - 1:
                    data[boss]['dps'] = line[line.index('>') + 1:]
                else:
                    data[boss]['dps'] = '0'
                find_data = 4
            elif find_data == 4:
                find_data = 5
            elif find_data == 5:
                if '>' in line and line.index('>') < len(line) - 1:
                    data[boss]['kills'] = line[line.index('>') + 1:]
                else:
                    data[boss]['kills'] = '0'
                find_data = 6
            elif find_data == 6:
                if '>' in line and line.index('>') < len(line) - 1:
                    data[boss]['fkill'] = line[line.index('>') + 1:]
                else:
                    data[boss]['fkill'] = '0:0'
                find_data = 7
            elif find_data == 7:
                if '>' in line and line.index('>') < len(line) - 1:
                    data[boss]['mlogs'] = line[line.index('>') + 1:]
                else:
                    data[boss]['mlogs'] = '0'
                find_data = 8
            elif find_data == 8:
                if '>' in line and line.index('>') < len(line) - 1:
                    data[boss]['point'] = line[line.index('>') + 1:]
                else:
                    data[boss]['point'] = '0'
                find_data = 0
    return data

def check_type(input):
    for i in input:
        if u'\u4e00' <= i <= u'\u9fff':
            return True
    return False

def get_log_details_search_player(player):
    if check_type(player) == True:
        url = 'https://www.fflogs.com/search/?term=' + cparse.quote(player)
    else:
        url = 'https://www.fflogs.com/search/?term=' + player
    try:
        web_data = requests.get(url)
    except Exception as e:
        print(e)
        return '与服务器通信错误', 0, None
    soup = BeautifulSoup(web_data.text,'html.parser')
    result = soup.find_all('div', attrs={'class':'search-item'})
    if result == None or len(result) == 0:
        return '未找到该玩家', 0, None
    else:
        data = ''
        for res in result:
            child = list(res.children)
            data += child[0].string + ' : ' + child[1].string + '\n'
        data = data[:-1]
        return data, len(result), child[1].string.split(' ')[-1]
    
    
    
    
    
    
    
    
    