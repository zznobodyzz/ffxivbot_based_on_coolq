from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from .get_weather import *
from common import *
from jieba import posseg
import jieba
jieba.load_userdict('./awesome/plugins/weather/game_place.txt')

__plugin_name__ = 'weather(天气查询,包括艾欧泽亚地区)'
__plugin_usage__ = '-weather 地区名(不支持国外,支持艾欧泽亚地区) 例: -weather 南京'

# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    self_debug("in weather command")
    # 获取城市的天气预报
    receive_command = session.current_arg
    city = session.get_optional('city')
    url = session.get_optional('url')
    days = session.get_optional('days')
    if days == None:
        if len(receive_command) == 1:
            days = 1
        elif len(receive_command) == 2 and receive_command[1].isdigit() == True:
            days = receive_command[1]
        else:
            days = 1
    if (receive_command == '' and city == None) or (city == 'None' and url == 'None'):
        weather_report = "想知道天气嘛？可是你好像没告诉我地区呀"
    elif url is not None and url == 'unknown' and city is not None:
        weather_report = '#(' + city +') 这个地方我好像不知道诶，抱歉没帮上忙'
    else:
        if city != None and city != 'None':
            receive_command = city
        if url == None:
            url = ' '
        weather_report = await get_weather_of_city(receive_command, url, days)
    # 向用户发送天气预报
    await session.send(weather_report)


@on_natural_language(keywords=('天气','气温','多少度'))
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg_text = session.msg_text.strip()
    NLP_result = 52.0
    if find_string(stripped_msg_text, '?') != -1:
        NLP_result += 1
    elif find_string(stripped_msg_text, '？') != -1:
        NLP_result += 1

    stripped_msg_text = stripped_msg_text.replace('?','')
    stripped_msg_text = stripped_msg_text.replace('？','')
    index1 = find_string(stripped_msg_text, '怎么样')
    index2 = find_string(stripped_msg_text, '如何')
    index3 = find_string(stripped_msg_text, '怎样')
    index4 = find_string(stripped_msg_text, '我想')
    index5 = find_string(stripped_msg_text, '告诉')
    index6 = find_string(stripped_msg_text, '查询')
    index7 = find_string(stripped_msg_text, '查')
    
    if index1 == len(stripped_msg_text) - 3:
        NLP_result += 2
    elif index2 == len(stripped_msg_text) - 2:
        NLP_result += 2
    elif index3 == len(stripped_msg_text) - 2:
        NLP_result += 2
    elif index4 == 0:
        NLP_result += 2
    elif index5 == 0:
        NLP_result += 8
    elif index6 != -1 or index7 != -1:
        NLP_result += 5
    elif find_string(stripped_msg_text, '多少度') != 0:
        NLP_result += 5
    else:
        NLP_result = 0.0
        return NLPResult(NLP_result, 'weather', {})

    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg_text)
    city = None
    for word in words:
        if word.flag == 'ns':
            city = word.word
    if city is None:
        return NLPResult(NLP_result, 'weather', {'city': 'None', 'url': 'None'})
    NLP_result += 5

    url = get_weather_url(city)
    if url != ' ' and url != 'error':
        NLP_result += 5
        days = 1
        if find_string(stripped_msg_text, '明天') != -1:
            if find_string(stripped_msg_text, '后天') != -1:
                days = 3
            else:
                days = 8
        elif find_string(stripped_msg_text, '后天') != -1:
            days = 9
        elif find_string(stripped_msg_text, '明后天') != -1 or find_string(stripped_msg_text, '明后两天') != -1:
            days = 3
        elif find_string(stripped_msg_text, '大后天') != -1:
            days = 10
        elif find_string(stripped_msg_text, '大大后天') != -1:
            days = 11
        elif find_string(stripped_msg_text, '二') != -1:
            if find_string(stripped_msg_text, '第') != -1:
                days = 8
        elif find_string(stripped_msg_text, '两天') != -1:
            days = 2
        elif find_string(stripped_msg_text, '三天') != -1:
            if find_string(stripped_msg_text, '第') != -1:
                days = 9
            else:
                days = 3
        elif find_string(stripped_msg_text, '四天') != -1:
            if find_string(stripped_msg_text, '第') != -1:
                days = 10
            else:
                days = 4
        elif find_string(stripped_msg_text, '五天') != -1:
            if find_string(stripped_msg_text, '第') != -1:
                days = 11
            else:
                days = 5
        elif find_string(stripped_msg_text, '六天') != -1:
            if find_string(stripped_msg_text, '第') != -1:
                days = 12
            else:
                days = 6
        elif find_string(stripped_msg_text, '七天') != -1:
            if find_string(stripped_msg_text, '第') != -1:
                days = 13
            else:
                days = 7

        # 返回处理结果，3 个参数分别为置信度、命令名、命令会话的参数
        return NLPResult(NLP_result, 'weather', {'city': city, 'url': url,'days':days})
    else:   
        return NLPResult(NLP_result, 'weather', {'city': city, 'url': 'unknown'})