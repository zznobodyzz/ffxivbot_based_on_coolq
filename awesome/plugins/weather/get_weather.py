from common import *
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from nonebot.helpers import render_expression

GET_WEATHER_FAILED_REPLY=('获取失败了！','好像没有获取成功...','不好意思呀，没找到数据',
                    '404 error --- data lose','我不想帮你获取了(其实是获取失败了'
                    '刚才在获取天气回来的路上，突然蹿出来两个黑衣人，我吓得拔腿就跑，于是...于是...数据丢了...')

def get_weather_url(location):
    head = 'http://www.weather.com.cn/weather/'
    tail = '.shtml'

    code = ' '
    
    f = open('./awesome/plugins/weather/city_weather.txt', 'r', encoding='UTF-8')
    if f == None:
        return 'error'
    for lines in f.readlines():
        line = lines.split('=')
        if len(line) > 1:
            if location + '\n' == line[1]:
                code = line[0]
                break
            
    if code == ' ':
        return 'error'

    if len(code) < 9:
        return code
    else:
        url = head + code + tail
        return url
        

def get_weather(url,days):
    self_debug("in get weather function")
    weather_dict = {'date':' ','high_temp':' ','low_temp':' ','weather':' '}
    weather_dict_list = []

    resp=urlopen(url)
    soup=BeautifulSoup(resp,'html.parser')
    next_day_flag = False
    tagtoday = soup.find('p',class_="tem")  #第一个包含class="tem"的p标签即为存放今天天气数据的标签

    temperatureLow = tagtoday.i.string  #获取最低温度
    try:
        temperatureHigh = tagtoday.span.string  #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
    except AttributeError as e:
        tagtoday = tagtoday.find_next('p',class_="tem")
        temperatureHigh = tagtoday.span.string #获取第二天的最高温度代替
        next_day_flag = True

    temperatureLow = tagtoday.i.string  #获取最低温度
    weatherToday = soup.find('p',class_="wea") #获取天气
    weather = weatherToday.string
    datetoday = soup.find('h1') #获取日期
    
    weather_dict['high_temp'] = temperatureHigh
    if weather_dict['high_temp'][len(weather_dict['high_temp']) - 1] != '℃':
        weather_dict['high_temp'] = weather_dict['high_temp'] + '℃'
    weather_dict['low_temp'] = temperatureLow
    weather_dict['weather'] = weather
    weather_dict['date'] = '今天'
    weather_dict_list.append(weather_dict.copy())
    if days > 1:
        if days > 7:
            days -= 7
        for day in range(0,days):
            datetoday = datetoday.find_next('h1') #获取日期
            if day == 0:
                weather_dict['date'] = '明天'
            elif day == 1:
                weather_dict['date'] = '后天'
            elif day >= 2:
                weather_dict['date'] = datetoday.string
            weatherToday = weatherToday.find_next('p',class_="wea")
            weather = weatherToday.string
            if next_day_flag == True:
                temperatureLow = tagtoday.i.string                
                next_day_flag = False
            else:
                tagtoday = tagtoday.find_next('p',class_="tem")
                temperatureLow = tagtoday.i.string
                temperatureHigh = tagtoday.span.string
            weather_dict['high_temp'] = temperatureHigh
            if weather_dict['high_temp'][-1] != '℃':
                weather_dict['high_temp'] = weather_dict['high_temp'] + '℃'
            weather_dict['low_temp']  = temperatureLow
            weather_dict['weather']   = weather
            weather_dict_list.append(weather_dict.copy())

    return weather_dict_list


def format_game_time(hour, minite):
    return_list = ['','','','','','']
    now = hour//8*8
    last = now - 8
    if last < 0:
        last = 16
    next1 = now + 8
    if next1 >= 24:
        next1 = next1 - 24
    next2 = now + 16
    if next2 >= 24:
        next2 = next2 - 24
    next3 = now
    

    return_list[0] = str(hour).zfill(2) + ":" + str(minite).zfill(2)
    
    return_list[1] = '过去 ' + str(last).zfill(2) + ":00"
    
    return_list[2] = '现在 ' + str(now).zfill(2) + ":00"
            
    return_list[3] = '将来 ' + str(next1).zfill(2) + ":00"
            
    return_list[4] = '将来 ' + str(next2).zfill(2) + ":00"
            
    return_list[5] = '将来 ' + str(next3).zfill(2) + ":00"
    
    return return_list

    
def get_game_time(time_line):
    index = find_string(time_line, '"hour":')
    return_list = ['','','','','','']
    if index != -1:
        if time_line[index+8].isdigit() == True:
            if time_line[index+9].isdigit() == True:
                hour = int(time_line[index+8:index+10])
            else:
                hour = int(time_line[index+8])
    else:
        return return_list
        
    index = find_string(time_line, '"minute":')
    if index != -1:
        if time_line[index+10].isdigit() == True:
            if time_line[index+11].isdigit() == True:
                minite = int(time_line[index+10:index+12])
            else:
                minite = int(time_line[index+10])
    else:
        return return_list
    return format_game_time(hour, minite)
        
        
def change_weather_code_to_word(c):
    weather_code_dict = ["", "碧空", "晴朗", "阴云", "薄雾", "微风", "强风", "小雨", "暴雨", "打雷", "雷雨", "扬沙", "沙尘暴", "炎热的天气", "热浪", "小雪", "暴雪", "妖雾", "Auroras", "黑暗", "绝命", "阴云", "雷云", "RoughSeas", "暴风雨", "阴沉", "热浪", "妖雾", "强风", "烟雾", "晴朗", "晴朗", "晴朗", "晴朗", "晴朗", "极光","辉核","辉核","辉核","辉核","Shelf Clouds","Shelf Clouds","Shelf Clouds","Shelf Clouds","神意","神意","神意","神意","神意","灵风","灵电","烟武","晴朗","Royal Levin","Hyperelectricity","Royal Levin","神意","Thunder","Thunder","Thunder","CutScene","神秘","Multiplicity","Rain","Fair Skies","Rain","Fair Skies","Dragonstorm","Dragonstorm","Subterrain","平衡","Concordance","Beyond Time","Beyond Time","Beyond Time","Demonic Infinity","鬼气","Demonic Infinity","DimensionalDisruption","DimensionalDisruption","DimensionalDisruption","Revelstorm","Revelstorm","极乐","极乐","Wyrmstorm","豪雨","Quicklevin","打雷","次元","Fair Skies","碧空","白旋风","白旋风","白旋风","","白旋风"];
    if c < 0 or c >= len(weather_code_dict):
        return ""
    return weather_code_dict[c]
        
def get_game_weather(area):
    weather_dict = dict()
    url1 = "https://ff14angler.com/skywatcher/"
    web_data = requests.get(url1)
    result = search_data(web_data.text, "varRID=")
    if result == " ":
        weather_dict['valid'] = False
        return weather_dict
    rid = result.replace(';','')
    url1 = "http://ff14angler.com/skywatcher.php?rid=" + rid + "&name=1"
    web_data = requests.get(url1)
    match = "},"
    src = web_data.text[9:]
    lines = []
    
    #将原始数据切成一行一行的
    while True:
        find_result = find_string(src, match)
        if find_result != -1:
            lines.append(src[0:find_result+2])
            src = src[find_result+2:]
        else:
            time_line = src
            break
    if len(lines) == 0:
        weather_dict['valid'] = False
        return weather_dict
    
    ###############################################
    #先获取当前时间，才能知道-1/0/1/2/3代表什么时间
    ###############################################

    game_time = get_game_time(time_line)
    weather_dict['time'] = game_time[0]
        
    area_line = []
    
    
    #筛检出对应地区的数据
    for line in lines:
        index = find_string(line, '"area":')
        if index != -1:
            if line[index+8:index+8+len(area)] == area:
                area_line.append(line)
                
    weather_dict['weather_data'] = dict()
    #获取天气
    for line in area_line:
        #获取这一行天气
        index = find_string(line, '"weather":')
        if line[index+11].isdigit() == True:
            if line[index+12].isdigit() == True:
                weather_code = int(line[index+11:index+13])
            else:
                weather_code = int(line[index+11])
        else:
            continue
            
        #获取这一行时间
        index = find_string(line, '"time":')
        if index != -1:
            if line[index+7] == '-':
                time_index = 1                
            elif line[index+7] == '0':
                time_index = 2
            elif line[index+7] == '1':
                time_index = 3
            elif line[index+7] == '2':
                time_index = 4
            elif line[index+7] == '3':
                time_index = 5
        
            weather_dict['weather_data'][game_time[time_index]] = change_weather_code_to_word(weather_code)
        else:
            continue
            
    weather_dict['valid'] = True        
    return weather_dict
    
def get_url_dynamic2(url):
    driver=webdriver.Chrome() #调用本地的火狐浏览器，Chrom 甚至 Ie 也可以的
    driver.get(url) #请求页面，会打开一个浏览器窗口
    html_text=driver.page_source
    driver.quit()
    return html_text

def get_game_weather_new(url):
    weather_dict = {}
    weather_dict['weather_data'] = dict()
    weather_dict['valid'] = True
    try:
        soup = BeautifulSoup(get_url_dynamic2('https://nenge.net/skywatcher/'),"html.parser")
        #get time
        data = soup.h1
        l = list(data.children)
        line = l[1].string
        line = line[line.index('日') + 1:]
        hour = int(line.split('时')[0])
        minite = int(line.split('时')[1][:-1])
        game_time = format_game_time(hour, minite)
        weather_dict['time'] = game_time[0]
        
        data = soup.div
        result = data.find(attrs={'data-zoneid': url})
        #get weather data
        for i in range(5):
            sub = result.select('img')[i]
            weather_dict['weather_data'][game_time[i+1]] = sub.attrs['title'].split(' ')[0]
        
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        weather_dict['valid'] = False
    return weather_dict


async def get_weather_of_city(city, url, days = 1):
    self_debug('city is: ' + city)
    location = city
    if url == ' ':
        url = get_weather_url(location)
    if url == 'error':
        return render_expression(GET_WEATHER_FAILED_REPLY)
    if len(url) < 9:
        if url[0] == 0:
            weather_dict = get_game_weather(url)
            data_from = '饥饿的猫'
        else:
            weather_dict = get_game_weather_new(url)
            data_from = 'https://nenge.net/skywatcher/'
        if weather_dict['valid'] == False:
            return render_expression(GET_WEATHER_FAILED_REPLY)
        else:
            send_msg = location + ' 当前时间: ' + weather_dict['time'] + '\n'
            for key in weather_dict['weather_data'].keys():
                send_msg = send_msg + key + ' : ' + weather_dict['weather_data'][key] + '\n'
            return send_msg + "数据来自 " + data_from
    else:
        #8  代表 明天
        #9  代表 后天
        #10 代表 大后天
        #11 代表 大大后天
        #12 代表 大大大后天
        #13 代表 大大大大后天
        weather_dict_list = get_weather(url, days)
        weather_msg = '来咯来咯，新鲜的天气预报 ' + location + ':\n'
        if days > 7 or days == 1:
            weather_msg += weather_dict_list[-1]['date'] + ' 最高温度' + weather_dict_list[-1]['high_temp'] + '，最低温度' + weather_dict_list[-1]['low_temp'] + '，天气是' + weather_dict_list[-1]['weather']
        else:
            for weather_dict in weather_dict_list[1:]:
                weather_msg += weather_dict['date'] + ' 最高温度' + weather_dict['high_temp'] + '，最低温度' + weather_dict['low_temp'] + '，天气是' + weather_dict['weather'] + '\n'
        return weather_msg