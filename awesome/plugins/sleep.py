from nonebot import on_command, CommandSession
from common import *
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot.helpers import context_id, render_expression

__plugin_name__ = 'sleep(休眠)'
__plugin_usage__ = '-sleep 让机器人去睡觉 -wakeup 唤醒机器人'

sleep_flag = False

SLEEP_REPLY=('呼呼呼','zZZ','嗯，说来我有些困了，睡觉！','好的，我去睡了','麻烦关下灯谢谢，我要睡觉了','我还不想睡呀','我还精神着呐')

WAKEUP_REPLY=('已经早上了吗','我醒了，嘿嘿','我好像还没睡醒','是谁！唤醒了我','早呀','呼呼呼（不管继续睡','我被床封印了。。。')

@on_command('sleep', aliases=('睡觉',))
async def sleep(session: CommandSession):
    global sleep_flag
    sleep_flag = True
    await session.send(render_expression(SLEEP_REPLY))

@on_command('wakeup', aliases=('唤醒',))
async def wakeup(session: CommandSession):
    global sleep_flag
    sleep_flag = False
    await session.send(render_expression(WAKEUP_REPLY))


@on_command('sleep-ensurance')
async def sleep(session: CommandSession):
    self_debug("in sleep ensurance function, skip message")
    return


@on_natural_language
async def _(session: NLPSession):
    global sleep_flag
    if sleep_flag == True:
        #如果进入睡眠，100%进入睡眠模块而不是进入其他模块
        return NLPResult(100.0, 'sleep-ensurance', {'message': session.msg_text})
    else:
        return NLPResult(0.0, 'sleep-ensurance', {'message': session.msg_text})