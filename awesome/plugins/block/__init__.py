from nonebot import on_command, CommandSession
from common import *
from .block_global import block_global
from .block_lib import *
from nonebot import on_natural_language, NLPSession, NLPResult


b_global = block_global()
b_global.block_init_init()

__plugin_name__ = 'block(屏蔽)'
__plugin_usage__ = '-block 设置机器人无视你的发言, 再次输入以解除效果'


@on_command('block', aliases=('屏蔽'))
async def block_set(session: CommandSession):
    global b_global
    member_id = str(session.ctx['user_id'])
    if member_id in session.bot.config.SUPERUSERS:
        if session.current_arg != '':
            b_global.block_list.append(session.current_arg)
            session.bot.config.BLACKLIST.append(session.current_arg)
            await session.send('#' + session.current_arg + ' 设置成功！')
    elif member_id not in b_global.block_list:
        b_global.block_list.append(member_id)
        session.bot.config.BLACKLIST.append(member_id)
        self_debug("send by function ------> -block")
        if session.ctx['sender'].has_key('card'):
            name = session.ctx['sender']['card']
        else:
            name = session.ctx['sender']['nickname']
        await session.send('#' + name + ' 设置成功！如有打扰十分抱歉')

@on_command('block-save', aliases=('屏蔽'))
async def block_set(session: CommandSession):
    global b_global
    member_id = str(session.ctx['user_id'])
    if member_id in session.bot.config.SUPERUSERS:
        save_block(b_global.block_list)
        await session.send('保存成功！')
    else:
        await session.send('你没有权限')

#内部命令，被屏蔽的语句进入这里，不做处理
@on_command('block-ensurance')
async def block(session: CommandSession):
    self_debug("in block ensurance function, skip message")
    return


@on_command('unblock', aliases=('解除屏蔽'))
async def block_unset(session: CommandSession):
    global b_global
    member_id = str(session.ctx['user_id'])
    if member_id in session.bot.config.SUPERUSERS:
        if session.current_arg != '' and session.current_arg in b_global.block_list:
            b_global.block_list.remove(session.current_arg)
            session.bot.config.BLACKLIST.remove(session.current_arg)
            await session.send('#' + session.current_arg + ' 设置成功！')
    if member_id in b_global.block_list:
        b_global.block_list.remove(member_id)
        session.bot.config.BLACKLIST.remove(member_id)
        if session.ctx['sender'].has_key('card'):
            name = session.ctx['sender']['card']
        else:
            name = session.ctx['sender']['nickname']
        await session.send('#' + name + ' 设置成功！嗨呀又见面啦')

@on_command('block-debug', aliases=())
async def block_debug(session: CommandSession):
    global b_global
    member_id = str(session.ctx['user_id'])
    if member_id in session.bot.config.SUPERUSERS:
        data = ''
        for id in b_global.block_list:
            data += id + '\n'
        await session.send(data)
    else:
        await session.send('你没有权限')

@on_natural_language
async def _(session: NLPSession):
    global b_global
    member_id = str(session.ctx['user_id'])
    if member_id in b_global.block_list:
        #如果被屏蔽，100%进入屏蔽模块而不是进入其他模块
        return NLPResult(100.0, 'block-ensurance', {'message': session.msg_text})
    else:
        return NLPResult(0.0, 'block-ensurance', {'message': session.msg_text})