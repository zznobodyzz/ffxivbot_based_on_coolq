from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from .calc_lib import *

__plugin_name__ = 'calc(配方计算)'
example = ' 例: -calc 450hq t 头手胸'
HELP_REPLY = '-calc 450hq 职业(职能) (职业2 职业3...) (除)(头|手|身|腰|腿|脚|耳|腕|项|戒|主手|骑士剑|骑士盾)(为空默认全套)\n(查武器不用指定职业)(戒指为一对!)'
__plugin_usage__ = HELP_REPLY + example


@on_command('calc', aliases=('配方计算', '生产计算'))
async def calc(session: CommandSession):
    global __plugin_usage__
    global HELP_REPLY
    receive_command = session.current_arg
    if receive_command == '':
        await session.send(__plugin_usage__)
        return
    element = receive_command.split(' ')
    if len(element) < 2:
        await session.send(__plugin_usage__)
        return
        
    if element[0] == '450hq' or element[0] == '450' or element[0] == '450HQ':
        element.pop(0)
        send_data = calc_450hq(element, HELP_REPLY)
    else:
        send_data = '抱歉，[%s]是未支持的配方呢' % element[0]
    await session.send(send_data)
    
    
@on_command('calc_450_help', aliases=())
async def calc_450_help(session: CommandSession):
    await session.send("是要查450HQ的材料吗？小雷可以帮你计算哦\n" + example)

 
@on_natural_language(keywords=('450hq','450HQ'))
async def _(session: NLPSession):
    NLP_result = 50
    if '什么' in session.msg_text:
        NLP_result += 5
    if '材料' in session.msg_text:
        NLP_result += 8
    if '要什么材料' in session.msg_text or '要哪些材料' in session.msg_text:
        NLP_result += 20
    return NLPResult(NLP_result, 'calc_450_help', {})