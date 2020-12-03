from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from .herolist_lib import *
from common import *
from nonebot.helpers import render_expression

__plugin_name__ = 'herolist(英雄榜查询)'

HEROLIST_HELP_REPLY='-herolist 副本名 角色名 服务器名'
__plugin_usage__ = HEROLIST_HELP_REPLY + ' 例: -herolist 阿尔法 小明 幻影'

#命令格式:-herolist 西格玛 黯丨 幻影群岛
@on_command('herolist', aliases=('armory', '英雄榜'))
async def herolist(session: CommandSession):
    receive_command = session.get_optional('nlp_result')
    if receive_command is None:
        receive_command = session.current_arg

    if receive_command == '':
        global HEROLIST_HELP_REPLY
        await session.send(HEROLIST_HELP_REPLY)
        return

    command_list = receive_command.split(' ')

    if len(command_list) < 3:
        send_msg = '缺少关键信息呢，需要的信息有:raid名、角色名、服务器名'
    else:
        if command_list[0] == 'None':
            send_msg = '抱歉呀，没有定位到有效的副本名称呢'
        else:
            return_dict = get_herolist_url(command_list[0])
            if return_dict['url'] == 'None':
                send_msg = '抱歉呀，该副本英雄榜暂不支持查询呢'
            else:
                if command_list[2] == 'None':
                    send_msg = '抱歉呀，没有定位到有效的服务器名称呢'
                else:
                    ret = get_herolist_data(command_list[1:], return_dict['raid_version'])
                    if ret['errno'] == 1:
                        send_msg = '角色名好像超过6个字了呢'
                    elif ret['errno'] == 2:
                        send_msg = '好像没有这个服务器吧？'
                    else:
                        send_msg = get_herolist(return_dict['url'], ret['data'], ret['server_name'], return_dict['raid_name'], return_dict['raid_version'])


    await session.send(send_msg)



@on_natural_language(keywords=('英雄榜',))
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg_text = session.msg_text.strip().replace('英雄榜','')
    NLP_result = 64.0
    if find_string(stripped_msg_text, '?') != -1:
        NLP_result += 1
    elif find_string(stripped_msg_text, '？') != -1:
        NLP_result += 1

    stripped_msg_text = stripped_msg_text.replace('?','')
    stripped_msg_text = stripped_msg_text.replace('？','')

    index1 = find_string(stripped_msg_text, '查询')
    index2 = find_string(stripped_msg_text, '查')
    if index1 != -1 or index2 != -1:
        NLP_result += 12
    
    stripped_msg_text = stripped_msg_text.replace('查询','')
    stripped_msg_text = stripped_msg_text.replace('查','')
    
    raid = get_herolist_raid_name(stripped_msg_text)
    if raid == 'None':
        NLP_result -= 10
    else:
        stripped_msg_text = stripped_msg_text.replace(raid,'')
    server = get_herolist_server_name(stripped_msg_text)
    if server == 'None':
        NLP_result -= 10
    else:
        stripped_msg_text = stripped_msg_text.replace(server,'')

    name = ''
    if ',' in stripped_msg_text:
        msg_list = stripped_msg_text.split(',')
    elif '，' in stripped_msg_text:
        msg_list = stripped_msg_text.split('，')
    else:
        msg_list = stripped_msg_text
    for msg in msg_list:
        name_index = find_string(msg, 'id')
        if name_index != -1:
            name_index += 2
            if name_index < len(msg) - 1:
                name = msg[name_index:]
                if name[0] == '是' or name[0] == '为' or name[0] == '叫':
                    name = name[1:]
                    if name[-1] == '的':
                        name = name[:-1]
    if name == '':
        name = session.ctx['sender']['card'].split('-')[0]
    name = name.replace(' ','')
    print(raid+' '+name+' '+server)
    return NLPResult(NLP_result, 'herolist', {'nlp_result':raid+' '+name+' '+server})

    
    

    