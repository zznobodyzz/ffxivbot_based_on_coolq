from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from jieba import posseg
from .get_logs import *
from common import *
from nonebot.helpers import render_expression

__plugin_name__ = 'logs(logs查询)'

LOGS_HELP_REPLY='-logs 副本名 职业名 国服(可选) dps数值(可选)'
LOG_DETAILS_HELP_REPLY='-log-details 角色名(如有空格以"+"号代替) 服务器名(可选) 职业(可选)'
__plugin_usage__ = LOGS_HELP_REPLY + ' 例: -logs O12S 黑魔 国服 8000'


LEAK_OF_BOSS_REPLY=('哪个boss呀？','啥boss？','好像没输入boss名称','我没理解你想查哪个boss','来来来，告诉我boss名称，我帮你查logs')
LEAK_OF_JOB_REPLY=('哪个职业呀？','啥职业？','好像没输入职业名哟','你想查哪个职业的logs呢','来来来，告诉我职业，我帮你查logs')
SEARCH_ERROR_REPLY=('好像没查到，请向奥雷反映问题','emmmm，数据可能被吞了','没查到诶...','查找失败了')

LEAK_OF_CHARACTER_REPLY=('没能正确获取角色名呢')
LEAK_OF_SERVER_REPLY=('没能正确获取服务器名呢')

@on_command('logs', aliases=('日志', '记录', '查日志'))
async def logs(session: CommandSession):
    receive_command = session.get_optional('nlp_result')
    if receive_command is None:
        receive_command = session.current_arg
    global LOGS_HELP_REPLY
    if receive_command == '':
        await session.send(LOGS_HELP_REPLY)
        return
    element = receive_command.split(' ')
    if len(element) != 2:
        await session.send(LOGS_HELP_REPLY)
        return
    #boss is None
    if element[0] == 'None':
        send_data = render_expression(LEAK_OF_BOSS_REPLY)
    elif element[1] == 'None':
        send_data = render_expression(LEAK_OF_JOB_REPLY)
    else:
        analy = get_logs_url(element)
        self_debug("send by function ------> -logs")
        if analy['error'] == 0:
            data = await get_logs(analy['url'])
            send_data = "boss: " + analy['boss'] + " job: " + analy['job'] + "\n（两周数据）"
            if '国服' in receive_command:
                send_data += ' 国服'
            send_data += ":\n"
            for key in data.keys():
                send_data = send_data + key + "%: " + data[key]
            if analy['logs_dps'] != 0:
                send_data += '\n' + str(analy['logs_dps']) + ' 大概在 '
                dps_percent = calc_dps_percent(analy['logs_dps'], data)
                send_data += '{:.2f}'.format(dps_percent) + '% 左右哦~'
                if dps_percent > 80:
                    send_data += '\n你好厉害啊，这个水平已经是绝对的大佬了!'
                elif dps_percent < 25:
                    send_data += '\n小雷觉得你的上升空间很大嘛，别灰心，多练习，继续加油吧~'
            #send_data = send_data + "100%的就别看了吧，怕伤你自尊"
        else:
            send_data = render_expression(SEARCH_ERROR_REPLY) + '\n错误原因：' + analy['error_msg']
    await session.send(send_data)


@on_command('log-details', aliases=(''))
async def log_details(session: CommandSession):
    receive_command = session.get_optional('nlp_result')
    if receive_command is None:
        receive_command = session.current_arg
    if receive_command == '':
        global LOG_DETAILS_HELP_REPLY
        await session.send(LOG_DETAILS_HELP_REPLY)
        return
    element = receive_command.split(' ')
    if element[0] == 'None':
        send_data = render_expression(LEAK_OF_CHARACTER_REPLY)
    elif len(element) == 1:
        send_data, player_num, server_name = get_log_details_search_player(element[0])
        if player_num == 0:
            await session.send(send_data)
            return
        elif player_num > 1:
            send_data = '查询到多个重名角色:\n' + send_data
            send_data += '\n请指定服务器名查询'
            await session.send(send_data)
            return
        else:
            element.append(server_name)
    if element[1] == 'None':
        await session.send(render_expression(LEAK_OF_SERVER_REPLY))
        return
    analy = get_log_details_url(element)
    self_debug("send by function ------> -log-details get log-details")
    if analy['error'] == 0:
        data = await get_log_details(analy['url'])
        if data is None:
            send_data = '与fflogs网站通信错误'
        else:
            send_data = element[0] + ' - ' + analy['server_official_name'] + '\n'
            if len(data.keys()) == 0:
                send_data += '小雷偷偷去看了眼，发现这个人什么记录都没有！'
            else:
                for boss in data.keys():
                    send_data += 'boss:' + boss + '\n' + \
                                    '    ' + '职业: [' + data[boss]['job'] + ']\n' + \
                                    '    ' + '最优秀logs: [' + data[boss]['blogs'] + ']\n' + \
                                    '    ' + '最优秀rdps: [' + data[boss]['dps'] + ']\n' + \
                                    '    ' + '击杀并上传次数: [' + data[boss]['kills'] + ']\n' + \
                                    '    ' + '最快用时: [' + data[boss]['fkill'] + ']\n' + \
                                    '    ' + '平均logs: [' + data[boss]['mlogs'] + ']\n' + \
                                    '    ' + '得分: [' + data[boss]['point'] + ']\n'
                send_data.rstrip('\n')
    else:
        send_data = render_expression(SEARCH_ERROR_REPLY) + '\n错误原因：' + analy['error_msg']
    await session.send(send_data)


@on_natural_language(keywords=('logs','打多高','打多少'))
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg_text = session.msg_text.strip()
    NLP_result = 64.0
    if find_string(stripped_msg_text, '?') != -1:
        NLP_result += 10
    elif find_string(stripped_msg_text, '？') != -1:
        NLP_result += 10

    stripped_msg_text = stripped_msg_text.replace('?','')
    stripped_msg_text = stripped_msg_text.replace('？','')

    if find_string(stripped_msg_text, 'logs') != -1:
        NLP_result += 5

    index1 = find_string(stripped_msg_text, '有谁知道')
    index2 = find_string(stripped_msg_text, '我想')
    index3 = find_string(stripped_msg_text, '告诉')
    index4 = find_string(stripped_msg_text, '查询')
    index5 = find_string(stripped_msg_text, '查')
    if index1 == 0:
        NLP_result += 8
    elif index2 == 0:
        NLP_result += 8
    elif index3 == 0:
        NLP_result += 8
    elif index4 != -1 or index5 != -1:
        NLP_result += 5

    job = 'None'
    boss = 'None'

    global job_list
    global boss_list

    job_exist_flag = False
    for jobs in job_list:
        if find_string(stripped_msg_text, jobs) != -1:
            NLP_result += 5
            job = jobs
            job_exist_flag = True
            break
    if job_exist_flag == False:
        NLP_result -= 10

    boss_exist_flag = False 
    for bosses in boss_list:
        if find_string(stripped_msg_text, bosses) != -1:
            NLP_result += 5
            boss = bosses
            boss_exist_flag = True
            break
    if boss_exist_flag == False:
        NLP_result -= 30

    stripped_msg_text += '!'
    dps_count = 0
    dps_index = 0
    logs_dps = ''
    for char in stripped_msg_text:
        if char.isdigit() == True:
            dps_count += 1
        elif dps_count < 4:
            dps_count = 0
        else:
            dps_index = stripped_msg_text.index(char) - dps_count
            logs_dps = stripped_msg_text[dps_index:dps_index+dps_count]
            break
    
    if find_string(stripped_msg_text, '国服') != -1:
        return NLPResult(NLP_result, 'logs', {'nlp_result':boss+' '+job+' '+'国服 ' + logs_dps})
    else:
        return NLPResult(NLP_result, 'logs', {'nlp_result':boss+' '+job+' ' + logs_dps})
