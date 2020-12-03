from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from .equipment_5_05 import *

__plugin_name__ = 'equip(配装)'
example = ' 例: -equip 5.05 战士'
HELP_REPLY = '-equip 版本 职业 '
__plugin_usage__ = HELP_REPLY + example


version = ('5.05')
job_alias_dict = {'占星':'Astrologian','诗人':'Bard','黑魔':'BlackMage','暗骑':'DarkKnight','黑骑':'DarkKnight','龙骑':'Dragoon','机工':'Machinist', \
            '武僧':'Monk','忍者':'Ninja','骑士':'Paladin','学者':'Scholar','召唤':'Summoner','战士':'Warrior','白魔':'WhiteMage', \
            '赤魔':'RedMage','武士':'Samurai','舞娘':'Dancer','枪刃':'Gunbreaker'}
job_fullname_dict = {'暗黑骑士':'DarkKnight','龙骑士':'Dragoon','机工师':'Machinist','白魔法师':'WhiteMage','吟游诗人':'Bard', \
            '黑魔法师':'BlackMage','召唤师':'Summoner','赤魔法师':'RedMage','占星术士':'Astrologian','绝枪战士':'Gunbreaker','舞者':'Dancer'}





def equip_advise(version, job):
    if version == '5.05':
        return equip_advise_5_05(job)
    #TODO
    
def equip_advise_url(version):
    if version == '5.05':
        return equip_advise_url_5_05()
    
    
@on_command('equip', aliases=('配装'))
async def equip(session: CommandSession):
    global __plugin_usage__
    global HELP_REPLY
    receive_command = session.current_arg
    if receive_command == '':
        await session.send(__plugin_usage__)
        return
    element = receive_command.split(' ')
    if len(element) < 2:
        if len(element) == 0:
            await session.send(__plugin_usage__)
            return
        else:
            if element[0] in version:
                await session.send(equip_advise_url(element[0]))
            else:
                await session.send("抱歉，[%s] 该版本的配装当前不支持哦" %(element[0]))
            return
        
    if element[0] not in version:
        await session.send("抱歉，[%s] 该版本的配装当前不支持哦" %(element[0]))
        return
    if element[1] in job_alias_dict.keys():
        job = job_alias_dict[element[1]]
    elif element[1] in job_fullname_dict.keys():
        job = job_fullname_dict[element[1]]
    elif element[1] in job_alias_dict.values():
        job = element[1]
    else:
        await session.send("抱歉，[%s] 是未识别的职业呢" %(element[0]))
        return
    send_data = equip_advise(element[0], job)
    await session.send(send_data)
    
    
@on_command('equip_help', aliases=())
async def equip_help(session: CommandSession):
    await session.send("想获取配装方面的建议吗？小雷可以帮你哦\n" + example)

 
@on_natural_language(keywords=('配装'))
async def _(session: NLPSession):
    NLP_result = 50
    if '怎么配装' in session.msg_text:
        return NLPResult(70, 'equip_help', {})
    else:
        return NLPResult(0, 'equip_help', {})