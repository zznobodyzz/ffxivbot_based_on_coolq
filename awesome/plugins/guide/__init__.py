from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from common import *
from nonebot.helpers import render_expression
from jieba import posseg
import jieba
import pickle
import os
from nonebot import permission as perm



__plugin_name__ = 'guide(副本攻略查询)'

GUIDE_HELP_REPLY='-guide 副本名(可简写)'
__plugin_usage__ = GUIDE_HELP_REPLY + ' 例: -guide O12S'


guide_database = {}


SEARCH_FAILED_REPLY=('抱歉，这个副本名我读不懂诶','副本名搜索失败，试试更加官方的名字？','输入的副本名是别名吗？可能不支持，换个说法吧')

def plugin_init():
    global guide_database
    print(os.getcwd())
    if os.path.exists('./awesome/plugins/guide/guidedb') == True:
        with open('./awesome/plugins/guide/guidedb', 'rb') as file:
            guide_database = pickle.load(file)
            file.close()
    else:
        file = open("./awesome/plugins/guide/dungeonlist.txt","r")
        for line in file.readlines():
            data_list = line.split('=')
            guide_database[data_list[0]] = [data_list[1] if len(data_list) > 1 else None, data_list[2] if len(data_list) > 2 else None]
        file.close()
        bin_file = open('./awesome/plugins/guide/guidedb', 'wb')
        pickle.dump(guide_database, bin_file)
        bin_file.close()

def search_guide(dungeon):
    global guide_database
    send_msg = ''
    bingo_flag = False
    if dungeon in guide_database.keys():
        bingo_flag = True
    else:
        match_list = []
        for key in guide_database.keys():
            if check_if_match_apart(key, dungeon):
                match_list.append(key)
        if len(match_list) == 1:
            bingo_flag = True
            dungeon = key
        elif len(match_list) > 1:
            send_msg = '找到了多个相似名称的副本:\n'
            for key in match_list:
                send_msg += key + '\n'
            send_msg.rstrip('\n')
            return send_msg
    if bingo_flag == True:
        send_msg += '找到啦，[' + dungeon + ']攻略:\n'
        if guide_database[dungeon][0] != None and guide_database[dungeon][0] != '0':
            send_msg += '文字版:https://www.ffsusu.com/detail/instance/' + guide_database[dungeon][0]
        if guide_database[dungeon][1] != None and guide_database[dungeon][1] != '0':
            send_msg += '视频版:https://www.bilibili.com/video/av' + guide_database[dungeon][1]
    else:
        send_msg += '抱歉，小雷暂未收录该副本的攻略呢'
    return send_msg



@on_command('guide', aliases=('攻略',))
async def guide(session: CommandSession):
    self_debug("in guide command")
    if session.current_arg == '':
        global GUIDE_HELP_REPLY
        await session.send(GUIDE_HELP_REPLY)
        return
    dungeon = session.current_arg

    send_msg = search_guide(dungeon)
       
    self_debug("send by function ------> -guide")
    await session.send(send_msg)
    return


        

        
#副本别名变化太多，问法变化太多，放弃自然语言
'''
@on_natural_language(keywords=('攻略', '怎么打', '要注意的'))
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg_text = session.msg_text.strip()
    words = posseg.lcut(stripped_msg_text)
    dungeon = None
    print(words)
    for word in words:
        if word.flag == 'un':
            dungeon = word.word
            break
    if dungeon is None:
        return NLPResult(0, 'guide', {})
    else:
        return NLPResult(98.0, 'guide', {'dungeon': dungeon})
'''