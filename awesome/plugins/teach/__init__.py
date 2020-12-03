from nonebot import on_command, CommandSession
from nonebot import permission as perm
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot.helpers import context_id, render_expression
from common import *
from .teach_lib import *
from .teach_global import teach_global

__plugin_name__ = 'teach(教机器人说话)'

TEACH_HELP_REPLY='--teach 需要作出应答的语句|应答语句--image(image为可选项,允许作为联想词)'
TEACH_MODE_HELP_REPLY='--teach-mode 0|1(1表示说出教学人,0表示不说)'
__plugin_usage__ = TEACH_HELP_REPLY + ' 例: --teach 猴|说道猴，我就想到...--image'

t_global = teach_global()
t_global.teach_init_init()



def plugin_init():
    global t_global
    init_teach(t_global.teach_dict)


@on_command('-teach-save', aliases=('保存教学',))
async def teach_save(session: CommandSession):
    if len(t_global.teach_dict.keys()) == 0:
        return_msg = "你还啥都没教我呢！"
    else:
        save_teach(t_global.teach_dict)
        return_msg = "好的，我把今天教的全部记小本本了"
    self_debug("send by function ------> --teach-save")
    await session.send(return_msg)


@on_command('-teach', aliases=('教学',))
async def teach(session: CommandSession):
    global t_global
    print(session.ctx['sender'])
    if 'card' in session.ctx['sender'].keys():
        member_name = session.ctx['sender']['card']
        member_name = member_name.split('-')[0]
    else:
        member_name = session.ctx['sender']['nickname']
    if session.current_arg == '':
        global TEACH_HELP_REPLY
        await session.send(TEACH_HELP_REPLY)
        return
    await session.send(append_teach(session.current_arg, t_global.teach_dict, member_name))

@on_command('-teach-delete', aliases=('删除教学',))
async def teach_delete(session: CommandSession):
    global t_global
    await session.send(delete_teach(session.current_arg, t_global.teach_dict))

@on_command('-teach-mode', aliases=('教学者',))
async def teach_mode(session: CommandSession):
    global t_global
    if session.current_arg == '':
        global TEACH_HELP_REPLY
        await session.send(TEACH_MODE_HELP_REPLY)
        return
    await session.send(teach_mode_config(t_global, session.current_arg, session))


#内部命令，自然语言进入匹配
@on_command('teach-search')
async def teach_search(session: CommandSession):
    global t_global
    message = session.get_optional('message')
    image = session.get_optional('image')
    send_msg = search_teach(message, t_global.teach_dict, t_global.teach_mode, image)
    if send_msg != '':
        await session.send(send_msg)






@on_command('-teach-debug', permission=perm.SUPERUSER)
async def teach_debug(session: CommandSession):
    global t_global
    self_debug("teach-debug start:")
    print(t_global)
    self_debug("teach-debug end")


@on_natural_language
async def _(session: NLPSession):
    global t_global
    stripped_msg_text = session.msg_text.strip()
    if stripped_msg_text in t_global.teach_dict.keys():
        # 以置信度 100.0 返回 teach-search 命令
        return NLPResult(100.0, 'teach-search', {'message': stripped_msg_text, 'image': 0}) #image 0 表示完全匹配
    else:
        #开始联想
        for key in t_global.teach_dict.keys():
            #判断image列表中是否全部禁止联想
            flag = True
            for image in t_global.teach_dict[key]['image']:
                if image != 0:
                    flag = False
                    break
            #是，则跳过这个key
            if flag == True:
                continue
            for char in stripped_msg_text:
                if char in key:
                    confident = check_image_match(stripped_msg_text, char, key)
                    if confident != 0:
                        #联想成功,计算置信度
                        return NLPResult(confident + 80, 'teach-search', {'message': key, 'image': 1}) #image变量表示是通过联想得到的key
        #失败
        return NLPResult(0.0, 'teach-search', {'message': session.msg_text})