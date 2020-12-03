from .calc_450hq_db import calc_unique_meterial
import copy
from common import *

job_dict = {'占星':'治疗','诗人':'远敏','黑魔':'法系','暗骑':'坦克','黑骑':'坦克','龙骑':'龙骑','机工':'远敏', \
            '武僧':'武士武僧','忍者':'忍者','骑士':'坦克','学者':'治疗','召唤':'法系','战士':'坦克','白魔':'治疗', \
            '赤魔':'法系','武士':'武士武僧', '舞娘':'远敏' ,'枪刃':'坦克',\
            '暗黑骑士':'坦克','龙骑士':'龙骑','机工师':'远敏','白魔法师':'治疗','吟游诗人':'远敏',\
            '黑魔法师':'法系','召唤师':'法系','赤魔法师':'法系','占星术士':'治疗','绝枪战士':'坦克','舞者':'远敏'}
            
weapon_dict = {'占星':'天球仪','诗人':'弓','黑魔':'魔杖','暗骑':'大剑','黑骑':'大剑','龙骑':'龙骑枪','机工':'机工枪', \
            '武僧':'拳套','忍者':'匕首','骑士':'骑士剑盾','学者':'学者书','召唤':'召唤书','战士':'斧','白魔':'法杖', \
            '赤魔':'刺剑','武士':'武士刀', '舞娘':'月轮' ,'枪刃':'枪刃',\
            '暗黑骑士':'大剑','龙骑士':'龙骑枪','机工师':'机工枪','白魔法师':'法杖','吟游诗人':'弓',\
            '黑魔法师':'魔杖','召唤师':'召唤书','赤魔法师':'刺剑','占星术士':'天球仪','绝枪战士':'枪刃','舞者':'月轮'}

def calc_450hq(element, HELP_REPLY):
    character = []
    job = []
    clothing_list = []
    tank_character_list = ('t','T','坦','坦克')
    healer_character_list = ('n','N','奶','奶妈','治疗')
    dps_character_list = ('远敏','法系','武士武僧','忍者','龙骑')
    clothing = {'头':1,'手':1,'身':1,'腰':1,'腿':1,'脚':1,'耳':1,'腕':1,'项':1,'戒':1}
    weapon = {'骑士剑':0,'骑士盾':0,'斧':0,'枪刃':0,'大剑':0, \
                '拳套':0,'武士刀':0,'匕首':0,'龙骑枪':0, \
                '魔杖':0,'刺剑':0,'召唤书':0, \
                '机工枪':0,'弓':0,'月轮':0, \
                '法杖':0,'学者书':0,'天球仪':0}
    
    #get job type
    reverse = 0
    for i in range(len(element)):
        if element[i] in tank_character_list:
            character.append('坦克')
            clothing_list.append(copy.deepcopy(clothing))
        elif element[i] in healer_character_list:
            character.append('治疗')
            clothing_list.append(copy.deepcopy(clothing))
        elif element[i] in weapon.keys():
            for k,v in weapon_dict.items():
                if v == element[i]:
                    job.append(k)
                    break
        else:
            success = False
            for c in dps_character_list:
                if element[i] in c:
                    character.append(c)
                    success = True
                    if element[i] == '武士' or element[i] == '武僧' or element[i] == '忍者' or element[i] == '龙骑':
                        job.append(element[i])
                    break
            if success == False:
                global job_dict
                if element[i] in job_dict.keys():
                    character.append(job_dict[element[i]])
                    job.append(element[i])
                else:
                    for j in job_dict.keys():
                        if j in element[i]:
                            character.append(job_dict[j])
                            clothing_list.append(copy.deepcopy(clothing))
                            job.append(j)
                            success = True
                            break
                    if success == False:
                        break
        if len(character) == 7:
            break
    #去重
    character = list(set(character))
        
    if len(character) == 0:
        return "命令解析失败了\n" + HELP_REPLY
    if len(character) > 1:
        for j in job:
            weapon[weapon_dict[j]] = 1
        return calc_unique_meterial(character, clothing_list, weapon)

    #if len(character) == 1
    if len(element) == 1:
        weapon[weapon_dict[job[0]]] = 1
        return calc_unique_meterial(character, [clothing], weapon)
    elif len(element) == 2:
        if element[1][0] == '除':
            element[1] = element[1][1:]
            for wea in weapon.keys():
                weapon[wea] = 1
        else:
            for cloth in clothing.keys():
                clothing[cloth] = 0
        weapon_flag = False
        index = find_string(element[1], '主手')
        if index != -1:
            weapon_flag = True
            element[1] = element[1][0:index] + element[1][index+2:]
        index = find_string(element[1], '武器')
        if index != -1:
            weapon_flag = True
            element[1] = element[1][0:index] + element[1][index+2:]
        if weapon_flag == True:
            if element[0] in weapon_dict.keys():
                weapon[weapon_dict[element[0]]] = 1
            else:
                return '没有指定特定职业的武器呢'
        #clothing
        for c in element[1]:
            if c in clothing.keys():
                clothing[c] ^= 1
                index = element[1].index(c)
                element[1] = element[1][0:index] + element[1][index+1:]
        #weapon
        for w in weapon.keys():
            index = find_string(element[1], w)
            if index != -1:
                weapon[w] ^= 1
                element[1] = element[1][0:index] + element[1][index+len(w):]
        return calc_unique_meterial(character, [clothing], weapon)
        