from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from common import *
from nonebot.helpers import render_expression

__plugin_name__ = 'graceful_reply(自然语言解析回复)'
__plugin_usage__ = '-ra 开启功能,再次输入以关闭功能'

FUNCTION_SWITCH = False

CALL_ME_REPLY=('在的亲，找我有什么事呢亲？','哎嘿',
                '干嘛？谁喊我呀','啥事？','小雷在此！','怎么了？','啥事呀(挠头',
                '嗯？','嗯嗯','想和我聊天请at我哦~','哦豁','嘿嘿（傻笑','哈哈哈哈',
                '不要以为我傻，我聪明着呢')
CALL_MY_MASTER=('你们在讨论我主人呀？','什么什么','突然感兴趣','快向我主人夸我~',
                    '奥雷？他咋啦？','emmmm(飘过','hhhhhh')
BLESSING=('小雷祝','小雷希望','祝','祝愿','小雷祝愿')
BLESSING_REPLY=('欢欢喜喜迎新年，开开心心过大年，平平安安吉祥年，快快乐乐喜庆年，团团圆圆团圆年，顺顺利利顺心年，舒舒服服舒心年，祝你长长久久岁岁年年！', \
                '欢乐新春，欣喜还在追忆，新年祝福已塞满邮箱;辛劳一岁，征尘尚未洗尽，年终奖金已撑满荷包！祝新的一年：好梦圆圆，好事连连！', \
                '吉祥钟声是我的问候，天籁歌声是我的祝福，纯洁雪花是我的贺卡，醇香美酒是我的飞吻，醉人春风是我的拥抱，甜蜜快乐是我的礼物，无限幸福是我的红包！统统都送给你，祝你春节快乐！', \
                '猪年到，鸿运照，烦恼的事儿往边靠，祝君出门遇贵人，在家听喜报！年年有此时，岁岁有今朝！', \
                '天增岁月人增寿，春满乾坤福满门。三羊开泰送吉祥，五福临门财源茂。恭祝新春快乐，平安幸福，合家欢乐！', \
                '猪年踏着金蹄过，期盼猪年不蹉跎。心中虽有千千结，勉励话语对谁说。新春虬枝梅花落，初夏清新喜事多。金秋结满吉祥果，暖冬飘来猪年雪。祝猪年快乐！', \
                '走过的是狗年，驱走的是霉运;到来的是猪年，期待的是美好;流逝的是光阴，换回的是记忆;送去的是祝福，留下的是：猪年家和万事兴！', \
                '金猪到，财神到，提“钱”贺新春，祝买卖赚钱，打牌赢钱，出门捡钱，办事省钱，兜里有钱，家里堆钱，银行存钱，院里晾钱，炕上藏钱，枕下压钱，勇往直前。祝您春节快乐，阖家幸福！', \
                '春节到，祝福问候一起到。用真心织一条快乐，用关心磨一袋幸福，用细心送一份健康，用精心剪一段平安，用放心投一颗梦想。心意到，愿你新年佳节快快乐乐，幸福一辈子。春节快乐！', \
                '新春佳节到，向您问声好，祝您猪年，身体倍健康，心情特别好；好运天天交，口味顿顿妙。最后祝您及您的家人：猪年好运挡不住，猪年财源滚滚来！新春快乐，万事如意！', \
                '新年好，好运到，祝福问候满天飘，愿您福气多多，快乐连连，万事圆圆，微笑甜甜，一帆风顺，二龙腾飞，三阳开泰，四季平安，五福临门，六六大顺，七星高照，八方来财，九九同心，十全十美！春节愉快！', \
                '点起温馨火炉，照亮光明前途；举起甜美红酒，喝下平安幸福；唱出美好祝福，踏出健康舞步；迈着轻盈脚步，送出猪年祝福；祝你家庭和睦，猪年一展鸿图！春节快乐！', \
                '新年的喜庆如月光，照亮千万家；快乐的味道如糖果，甜蜜你心间；思念的温馨似棉被，温暖你身心；问候的传递载祝福，送到你眼前。祝你新春快乐，幸福安康！', \
                '喜迎新春吉祥年，祝福深深情无限；大吉大利拜大年，恭喜发财好运来；家庭美满事业兴，笑容满面体健安；百事可乐心舒畅，万事顺利梦想圆。祝朋友春节快乐！猪年吉祥！', \
                '祝福只多不少，喜气正在燃烧；字句渗透欢笑，包含标点符号；锁定问候目标，让你喜上眉梢；搂着开心舞蹈，撑着快乐跳高；新春祝福送到，愿你猪年乐逍遥！', \
                '猪年好，猪年妙，猪年的歌声满天飘；猪年烂，猪年暖，猪年的幸福享不完；猪年旺，猪年香，猪年的祝福分外长。愿你猪年心飞扬，万事皆顺畅！', \
                '新年来，好运来。快乐天天有，万事随心愿。事业再丰收，生活更美满。红颜相伴爱无边，家庭和睦人团圆。兜里钞票比星星还多，脸上笑容比阳光更加灿烂。祝猪年快乐！', \
                '新年快到了，祝福老套了，没啥爆料了，只好趁早了，愿你吃好了，愿你睡好了，如有雷同了，纯属巧合了，如有先到了，一定是抄我的了。新年快乐！', \
                '新年到，鸿运照，烦恼的事儿往边靠，爱情滋润没烦恼，钞票一个劲儿往家跑；出门遇贵人，在家听喜报，年年有此时，岁岁有今朝，祝您一年更比一年好！祝您猪年大吉大利！', \
                '世人都晓春节好，一年到头相聚闹；最是童年忘不掉，新衣新裤新鞋帽；亲朋好友拜年早，红包礼品不会少；祝福送到就是好，幸福安康新年好！新年快乐！')
BLESSING_LENGTH=len(BLESSING_REPLY)
BLESSING_INDEX=0
PRAISE_ME_REPLY=['过奖了过奖了','讨厌，你这么夸我我也不会高兴的','必须的','不好意思，膨胀了','那必须的','嘿嘿','不愧是我','哦豁']
PRAISE_MASTER_REPLY=['别夸了，他会膨胀的','毕竟是我主人','我替我主人说一句过奖了']
LAUGH_REPLY=['','','','','','','哦嚯嚯嚯嚯','笑声是会传染的，哈哈哈哈哈','笑（','嘿嘿嘿']



LAST_CONTENT=''
FUDU_CONTENT=''
LAST_CONTENT_USER_ID=0



@on_command('ra')
async def graceful_reply_switch(session: CommandSession):
    global FUNCTION_SWITCH
    if FUNCTION_SWITCH == True:
        FUNCTION_SWITCH = False
        msg = '自然语言解析回复功能已关闭'
    else:
        FUNCTION_SWITCH = True
        msg = '自然语言解析回复功能已开启'
    await session.send(msg)

#提及我自己
@on_command('graceful_reply_call_me')
async def graceful_reply_call_me(session: CommandSession):
    msg = session.get_optional('message')
    command = session.get_optional('command')
    if msg is None or command is None or command != 'call_me':
        return
    if find_string(msg, '你好') != -1 or \
        find_string(msg, '嗨') != -1 or \
        find_string(msg, 'hello') != -1 or \
        find_string(msg, 'hi') != -1 or \
        find_string(msg, '晚上好') != -1 or \
        find_string(msg, '见面') != -1 or \
        find_string(msg, '早安') != -1:
        #greetings
        await session.send("你好呀")
    elif find_string(msg, '再见') != -1 or \
        find_string(msg, '拜拜') != -1 or \
        find_string(msg, '晚安') != -1 or \
        find_string(msg, '好梦') != -1 or \
        find_string(msg, '撒有啦啦') != -1 or \
        find_string(msg, '回见') != -1:
        await session.send("拜拜")
    elif len(msg) == 2:
        if session.ctx['user_id'] in session.bot.config.SUPERUSERS:
            await session.send("至高无上的主人，您叫我？")
        else:
            await session.send("请问您是？")
    else:
        await session.send(render_expression(CALL_ME_REPLY))


#提及主人
@on_command('graceful_reply_call_master')
async def graceful_reply_call_master(session: CommandSession):
    msg = session.get_optional('message')
    command = session.get_optional('command')
    if msg is None or command is None or command != 'call_master':
        return
    await session.send(render_expression(CALL_MY_MASTER))


#祝福
@on_command('graceful_blessing')
async def graceful_blessing(session: CommandSession):
    global BLESSING
    global BLESSING_REPLY
    global BLESSING_LENGTH
    global BLESSING_INDEX
    from random import randint
    msg = session.get_optional('message')
    command = session.get_optional('command')
    if msg is None or command is None or command != 'blessing':
        return
    sender_name = session.ctx['sender']['card'].split('-')[0]
    await session.send(render_expression(BLESSING)+sender_name+'大佬'+'新年快乐！猪年大吉！心想事成！万事如意！！')
    if randint(1,3) > 1:
        if BLESSING_INDEX == BLESSING_LENGTH:
            BLESSING_INDEX = 0
        await session.send(BLESSING_REPLY[BLESSING_INDEX])
        BLESSING_INDEX += 1


#夸奖
@on_command('graceful_praise_reply')
async def graceful_reply(session: CommandSession):
    msg = session.get_optional('message')
    command = session.get_optional('command')
    if msg is None or command is None or command != 'praise':
        return
    sender_name = session.ctx['sender']['card'].split('-')[0]
    to_personal_reply = sender_name + '大佬过奖了'

    #praise to master
    if find_string(msg,'奥雷') != -1 or find_string(msg,'黯') != -1:
        reply_msg = return_random_with_additional_element(PRAISE_MASTER_REPLY,(to_personal_reply, (msg)))
    #praise to me
    elif find_string(msg, '小雷') != -1 or find_string(msg, '雷导') != -1:
        reply_msg = return_random_with_additional_element(PRAISE_ME_REPLY,(to_personal_reply, (msg)))
    #send reply
    else:
        reply_msg = msg
    await session.send(reply_msg)



@on_command('graceful_laugh_reply')
async def graceful_laugh_reply(session: CommandSession):
    numbers = session.get_optional('numbers')
    msg = numbers * render_expression(('哈','嘿','ha','嘻','嘎'))
    send_msg = return_random_with_additional_element(LAUGH_REPLY, (msg,))
    if send_msg != '':
        await session.send(send_msg)



@on_command('graceful_fudu_reply')
async def graceful_fudu_reply(session: CommandSession):
    msg = session.get_optional('message')
    global FUDU_CONTENT
    FUDU_CONTENT = msg
    await session.send(msg)




#### Natural language processor ####


@on_natural_language(keywords=('小雷','雷导'))
async def _(session: NLPSession):
    stripped_msg_text = session.msg_text.strip()
    return NLPResult(75.0 if FUNCTION_SWITCH else 0, 'graceful_reply_call_me', {'message': stripped_msg_text,'command':'call_me'})



@on_natural_language(keywords=('奥雷','黯'))
async def _(session: NLPSession):
    stripped_msg_text = session.msg_text.strip()
    return NLPResult(75.0 if FUNCTION_SWITCH else 0, 'graceful_reply_call_master', {'message': stripped_msg_text,'command':'call_master'})



@on_natural_language(keywords=('新年快乐','春节快乐','新年好','过年好','过年快乐'))
async def _(session: NLPSession):
    stripped_msg_text = session.msg_text.strip()
    return NLPResult(99.0 if FUNCTION_SWITCH else 0, 'graceful_blessing', {'message': stripped_msg_text,'command':'blessing'})



@on_natural_language(keywords=('不愧是','萨斯噶','不愧','tql','牛逼'))
async def _(session: NLPSession):
    global LAST_CONTENT
    LAST_CONTENT = session.msg_text
    stripped_msg_text = session.msg_text.strip()
    return NLPResult(95.0 if FUNCTION_SWITCH and session.msg_text != FUDU_CONTENT else 0, 'graceful_praise_reply', {'message': stripped_msg_text,'command':'praise'})


@on_natural_language(keywords=('哈',))
async def _(session: NLPSession):
    stripped_msg_text = session.msg_text.strip()
    numbers = check_string_contain_word_num(stripped_msg_text, '哈')
    if numbers > 2 and FUNCTION_SWITCH:
        return NLPResult(80.0, 'graceful_laugh_reply', {'message': stripped_msg_text,'numbers':numbers})
    else:
        return NLPResult(0.0, 'graceful_laugh_reply', {'message': stripped_msg_text,'numbers':numbers})


@on_natural_language()
async def _(session: NLPSession):
    global LAST_CONTENT
    global LAST_CONTENT_USER_ID
    global FUDU_CONTENT
    if session.msg_text != LAST_CONTENT or LAST_CONTENT_USER_ID == session.ctx['user_id'] or session.msg_text == FUDU_CONTENT:
        confident = 0.0
        LAST_CONTENT = session.msg_text
    else:
        confident = 96.0
    LAST_CONTENT_USER_ID = session.ctx['user_id']
    return NLPResult(confident, 'graceful_fudu_reply', {'message': session.msg_text})
                
    








###########################################################

                    #大型‘系统调用’命令簇
                                                        
###########################################################
'''
def decode_lit_command(command_list):

def decode_recovery_command(command_list):

def decode_transfer_command(command_list):

def decode_generate_command(command_list):

def decode_enhance_command(command_list):

def decode_deep_freeze_command(command_list):

def decode_release_command(command_list):

def decode_inspect_command(command_list):


def decode_command(command_list):
    if command_list[0] == 'lit':
        decode_lit_command(command_list.pop(0))
    elif command_list[0] == 'recovery':
        decode_recovery_command(command_list.pop(0))
    elif command_list[0] == 'transfer':
        decode_transfer_command(command_list.pop(0))
    elif command_list[0] == 'generate':
        decode_generate_command(command_list.pop(0))
    elif command_list[0] == 'enhance':
        decode_enhance_command(command_list.pop(0))
    elif command_list[0] == 'deep' and command_list[1] == 'freeze':
        decode_deep_freeze_command(command_list[2:]])
    elif command_list[0] == 'release':
        decode_release_command(command_list.pop(0))
    elif command_list[0] == 'inspect':
        decode_inspect_command(command_list.pop(0))







@on_command('system_call')
async def system_call(session: CommandSession):
    error = session.get_optional('error')
    if error == True:
        await session.send('[ERROR-0001]Command Error: Subcommand Missing')
        return
    subcommand = session.get_optional('subcommand')
    sub = subcommand.split(' ')
    if len(sub) < 2:
        await session.send('[ERROR-0002]Command Error: Subcommand Missing')
        return
    else:
        decode_command(sub)




@on_natural_language(keywords=('system call',))
async def _(session: NLPSession):
    stripped_msg_text = session.msg_text.strip()
    index = find_string(stripped_msg_text,'call')
    index += 5
    #check if system call ending with none words
    if index < len(stripped_msg_text)-1:
        #get sub order, give it to handle process
        system_call = stripped_msg_text[index:].replace(',',' ').strip(' ')
        return NLPResult(98.0, 'system_call', {'subcommand': system_call, 'error': False})
    else:
        return NLPResult(98.0, 'system_call', {'error': True})
'''