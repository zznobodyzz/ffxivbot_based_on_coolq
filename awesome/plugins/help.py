from nonebot import on_command, CommandSession
from common import *
from nonebot import on_natural_language, NLPSession, NLPResult, plugin

__plugin_name__ = 'help(帮助,使用说明)'


@on_command('help', aliases=('帮助','cmd'))
async def help(session: CommandSession):
    loaded_plugins = plugin.get_loaded_plugins()
    functions = dict()
    for p in loaded_plugins:
        name = getattr(p, 'name', None)
        usage = getattr(p, 'usage', None)
        if name != None and usage != None:
            functions[name] = usage
    send_msg = ''
    for func_name in functions.keys():
        send_msg += func_name + '\n描述:' + functions[func_name] + '\n\n'
    await session.send(send_msg)