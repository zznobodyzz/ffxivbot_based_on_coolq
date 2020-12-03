from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot.helpers import render_expression
from common import *
import random
import time

__plugin_name__ = 'tq2a(transform question to answer疑问句转换肯定句)'
__plugin_usage__ = '-qa 开启功能 再次输入以关闭功能(重要！嫌烦就关闭，任何人都有权限)'

FUNCTION_SWITCH = False

call_up_times = 0
last_call_time = 0

TQ2A_REPLY=['是的','对的','是这样的','没错','嗯对','嗯嗯','yes','我不知道','不懂']

def is_question_and_need_transform(content):
    '''
    if find_string(content, '奥雷') != -1 or \
        find_string(content, '亚莉') != -1 or \
        find_string(content, '亚丽') != -1 or \
        find_string(content, '奥莉') != -1 or \
        find_string(content, '莉奥') != -1:
        return False
    '''
    if len(content) > 2 and (content[-1] == '?' or \
        content[-1] == '？') and \
        (content[-2] == '吗' or content[-2] == '嘛') and content[-3] != '干':
        return True
    if len(content) > 1 and (content[-1] == '吗' or content[-1] == '嘛') and content[-2] != '干':
        return True
    return False


def change_question_to_answer(content):
    content = content.split(',')[-1]
    if find_string(content, '那么') == 0:
        content = content[2:]
    if find_string(content, '那') == 0:
        content = content[1:]
    elif find_string(content, '所以') == 0:
        content = content[2:]
    elif find_string(content, '于是') == 0:
        content = content[2:]
    elif find_string(content, '然后') == 0:
        content = content[2:]
    content = content.replace('我','嶤')
    content = content.replace('你','我')
    content = content.replace('嶤','你')
    msg = content.replace('吗','').replace('嘛','').replace('?','').replace('？','')
    if find_string(content, '有') != -1:
        msg = render_expression(['有','有的','没有',msg,msg,msg])
    elif find_string(content, '会') != -1:
        msg = render_expression(['会','会的','不会',msg,msg,msg])
    elif find_string(content, '是') != -1:
        msg = render_expression(['是','是的','不是',msg,msg,msg])
    else:
        msg = render_expression([content,msg,msg,msg])
    return msg

@on_command('qa')
async def tq2a_switch(session: CommandSession):
    global FUNCTION_SWITCH
    if FUNCTION_SWITCH == True:
        FUNCTION_SWITCH = False
        msg = '疑问句回答功能已关闭'
    else:
        FUNCTION_SWITCH = True
        msg = '疑问句回答功能已开启'
    await session.send(msg)



@on_command('tq2a')
async def tq2a(session: CommandSession):
    msg = session.get_optional('msg')
    if msg == None or FUNCTION_SWITCH == False:
        return

    global call_up_times
    global last_call_time
    current_time = time.time()
    if (find_string(msg, '奥雷') != -1 or \
        find_string(msg, '亚莉') != -1 or \
        find_string(msg, '亚丽') != -1 or \
        find_string(msg, '奥莉') != -1 or \
        find_string(msg, '莉奥') != -1) and \
        current_time - last_call_time < 60:
        call_up_times += 1
    if call_up_times > 3:
        send_msg = SYSTEM_ERROR_REPLY
    else:
        index1 = find_string(msg,'吗')
        index2 = find_string(msg,'嘛')
        if index1 != -1 and msg[index1-1] == '好' or msg[index1-1] == '对':
            send_msg = msg[index-1] + '的'
        elif index2 != -1 and msg[index2-1] == '好' or msg[index2-1] == '对':
            send_msg = msg[index-1] + '的'
        else:
            send_msg = change_question_to_answer(msg)
    self_debug("send by function ------> response for change question to answer")
    self_debug("call up times = %d" %(call_up_times))
    last_call_time = time.time()
    await session.send(send_msg)

@on_natural_language(keywords=('吗','嘛'))
async def _(session: NLPSession):
    stripped_msg_text = session.msg_text.strip()
    if is_question_and_need_transform(stripped_msg_text):
        return NLPResult(60.0, 'tq2a', {'msg': stripped_msg_text})
        