meterial = {0:('铜矿','普通'),1:('金矿','普通'),2:('硬金沙','普通'),3:('硫磺','普通'),4:('粗硝石','普通'),5:('黄明矾','普通'),6:('暗银沙','普通'),7:('地下天然水','普通'),8:('落叶松原木','普通'),9:('矮人棉','普通'),10:('凝灰岩','普通'), \
            11:('重钨矿','限时'),12:('彩虹晶','限时'),13:('泡茧','限时'),14:('檀香木原木','限时'),15:('黑玛瑙原石','限时'),16:('三重石原石','限时'), \
            17:('野蛮盗龙的粗皮','Fate币'),18:('吸血大口花的卷须','Fate币'),19:('缠尾蛟的粗皮','Fate币'), \
            20:('甜香荠','普通'),21:('光芒大丁草','普通'),22:('青柠罗勒草','普通'),23:('邪衣薰衣草','普通'),24:('虎百合','普通'), \
            25:('工芸館特製研磨剤','点数'),26:('工芸館特製綿布','点数'),27:('カリコテリウムの粗皮','点数'),28:('工芸館特製錬金薬','点数'),29:('工芸館特製アルメン','点数'),30:('工芸館特製樹脂','点数'),31:('工芸館特製ワニス','点数'), \
            32:('一水灵砂','灵砂'),33:('险山灵砂','灵砂'),34:('古树灵砂','灵砂'), \
            35:('石金块','半成品'),36:('深金块','半成品'),37:('黑玛瑙','半成品'),38:('矮人棉布','半成品'),39:('缠尾蛟革','半成品'),40:('三重石','半成品'),41:('暗银附魔墨水','半成品'),42:('野蛮盗龙革','半成品'),43:('红色火药','半成品'),44:('凝灰岩砥石','半成品'), \
            45:('g2幻水刚力','幻水'),46:('g2幻水耐力','幻水'),47:('g2幻水意力','幻水'),48:('g2幻水巧力','幻水'),49:('g2幻水智力','幻水') \
}

def combine_result(unique_meterial):
    data = '无半成品所需材料:\n\t'
    global meterial
    for id in (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19):
        if unique_meterial[id] != 0:
            data += meterial[id][0] + ':' + str(unique_meterial[id]) + ' (' + meterial[id][1] + ')\n\t'
    data = data[:-1]
    data += '半成品准备好后所需材料:\n\t'
    for id in (11,12,13,14,35,36,37,38,39,40,41,42,43,44):
        if unique_meterial[id] != 0:
            data += meterial[id][0] + ':' + str(unique_meterial[id]) + ' (' + meterial[id][1] + ')\n\t'
    data = data[:-1]
    data += '点数材料:\n\t'
    point = 0
    for id in (25,26,27,28,29,30,31):
        if unique_meterial[id] != 0:
            data += meterial[id][0] + ':' + str(unique_meterial[id]) + '\n\t'
            point += unique_meterial[id] * 20
    data += '(总计[%d]神典石点数)\n' %(point)
    data += '其他材料:\n\t'
    for id in (20,21,22,23,24,32,33,34):
        if unique_meterial[id] != 0:
            data += meterial[id][0] + ':' + str(unique_meterial[id]) + '\n\t'
    data = data[:-1]
    data += 'g2幻水:\n\t'
    for id in (45,46,47,48,49):
        if unique_meterial[id] != 0:
            data += meterial[id][0] + ':' + str(unique_meterial[id]) + '\n\t'
    data = data[:-2]
    return data

def calc_unique_meterial_param1(unique_param1, ch, cl):
    unique_param1[ch] = (int(((cl['头']+cl['身']+cl['手']+cl['腿']+cl['脚']+cl['戒'])*2+cl['腰']+cl['耳']+cl['项']+cl['腕'])/3)+1)*2  
    
def calc_unique_meterial(character, clothing, weapon):
    unique_meterial = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0, \
        19:0,20:0,21:0,22:0,23:0,24:0,25:0,26:0,27:0,28:0,29:0,30:0,31:0,32:0,33:0,34:0,35:0, \
        36:0,37:0,38:0,39:0,40:0,41:0,42:0,43:0,44:0,45:0,46:0,47:0,48:0,49:0}
    unique_param1 = {'坦克':0,'治疗':0,'武士武僧':0,'忍者':0,'龙骑':0,'法系':0,'远敏':0}
    unique_param2 = {'坦克':0,'治疗':0,'武士武僧':0,'忍者':0,'龙骑':0,'法系':0,'远敏':0}
    job_param = {'坦克':{'头':0,'手':0,'身':0,'腰':0,'腿':0,'脚':0,'耳':0,'腕':0,'项':0,'戒':0}, \
                '治疗':{'头':0,'手':0,'身':0,'腰':0,'腿':0,'脚':0,'耳':0,'腕':0,'项':0,'戒':0}, \
                '武士武僧':{'头':0,'手':0,'身':0,'腰':0,'腿':0,'脚':0,'耳':0,'腕':0,'项':0,'戒':0}, \
                '忍者':{'头':0,'手':0,'身':0,'腰':0,'腿':0,'脚':0,'耳':0,'腕':0,'项':0,'戒':0}, \
                '龙骑':{'头':0,'手':0,'身':0,'腰':0,'腿':0,'脚':0,'耳':0,'腕':0,'项':0,'戒':0}, \
                '法系':{'头':0,'手':0,'身':0,'腰':0,'腿':0,'脚':0,'耳':0,'腕':0,'项':0,'戒':0}, \
                '远敏':{'头':0,'手':0,'身':0,'腰':0,'腿':0,'脚':0,'耳':0,'腕':0,'项':0,'戒':0}}
    data = '指定的装备为:\n'
    for ch,cl in zip(character, clothing):
        calc_unique_meterial_param1(unique_param1, ch, cl)
        if '坦克' == ch:
            unique_param2['坦克'] = (weapon['骑士剑'] + weapon['骑士盾'] + weapon['斧'] + weapon['枪刃'] + weapon['大剑']) * 2
            job_param['坦克'] = cl
        if '治疗' == ch:
            unique_param2['治疗'] = (weapon['法杖'] + weapon['学者书'] + weapon['天球仪']) * 2
            job_param['治疗'] = cl
        if '武士武僧' == ch:
            unique_param2['武士武僧'] = (weapon['拳套'] + weapon['武士刀']) * 2
            job_param['武士武僧'] = cl
        if '龙骑' == ch:
            unique_param2['龙骑'] = weapon['龙骑枪'] * 2
            job_param['龙骑'] = cl
        if '忍者' == ch:
            unique_param2['忍者'] = weapon['匕首'] * 2
            job_param['忍者'] = cl
        if '远敏' == ch:
            unique_param2['远敏'] = (weapon['机工枪'] + weapon['弓'] + weapon['月轮']) * 2
            job_param['远敏'] = cl
        if '法系' == ch:
            unique_param2['法系'] = (weapon['魔杖'] + weapon['刺剑'] + weapon['召唤书']) * 2
            job_param['法系'] = cl
        data += '[%s]-[' %(ch)
        for c,v in cl.items():
            if v != 0:
                data += c + '.'
        data.rstrip('.')
        data += ']\n'
    data += '指定的武器为: ['
    for w,v in weapon.items():
        if v != 0:
            data += w + '.'
    data.rstrip('.')
    data += ']\n'
    #get grass number
    unique_meterial[20] = (unique_param1['武士武僧'] + unique_param2['武士武僧'] + unique_param1['龙骑'] + unique_param2['龙骑']) / 2
    unique_meterial[21] = (unique_param1['忍者'] + unique_param2['忍者'] + unique_param1['远敏'] + unique_param2['远敏']) / 2
    unique_meterial[22] = (unique_param1['坦克'] + unique_param2['坦克']) / 2
    unique_meterial[23] = (unique_param1['法系'] + unique_param2['法系']) / 2
    unique_meterial[24] = (unique_param1['治疗'] + unique_param2['治疗']) / 2
    #get water number
    unique_meterial[45] = unique_meterial[20] * 3
    unique_meterial[46] = unique_meterial[22] * 3
    unique_meterial[47] = unique_meterial[24] * 3
    unique_meterial[48] = unique_meterial[21] * 3
    unique_meterial[49] = unique_meterial[23] * 3
    #get sand number
    unique_meterial[32] = unique_meterial[21] * 3
    unique_meterial[33] = (unique_param1['武士武僧'] + unique_param2['武士武僧'] + \
                            unique_param1['龙骑'] + unique_param2['龙骑'] + \
                            unique_param1['坦克'] + unique_param2['坦克']) / 2 * 3
    unique_meterial[34] = (unique_param1['法系'] + unique_param2['法系'] + \
                        unique_param1['治疗'] + unique_param2['治疗']) / 2 * 3
    #get base number
    unique_meterial[36] = job_param['坦克']['头'] + job_param['坦克']['身'] + job_param['坦克']['腰'] + \
                        job_param['武士武僧']['腰'] + \
                        job_param['忍者']['腰'] + job_param['忍者']['脚'] + \
                        job_param['龙骑']['头'] + job_param['龙骑']['腰'] + \
                        job_param['治疗']['腰'] + \
                        job_param['法系']['腰'] + \
                        job_param['远敏']['手'] + job_param['远敏']['腰'] + job_param['远敏']['脚']
    unique_meterial[35] = job_param['治疗']['脚'] + \
                        job_param['法系']['身'] + job_param['法系']['脚'] + \
                        job_param['远敏']['身'] + \
                        job_param['忍者']['身'] + \
                        weapon['斧'] + weapon['枪刃'] + weapon['骑士剑'] + weapon['骑士盾'] + weapon['大剑'] + weapon['法杖'] + weapon['天球仪'] + weapon['拳套'] + weapon['匕首'] + weapon['龙骑枪'] + weapon['刺剑'] + weapon['弓']
    unique_meterial[0] = unique_meterial[36]
    unique_meterial[1] = unique_meterial[35]
    unique_meterial[2] = (unique_meterial[35] + unique_meterial[36]) * 4
    unique_meterial[3] = weapon['机工枪'] * 3
    unique_meterial[4] = weapon['机工枪'] * 3
    unique_meterial[19] = (job_param['治疗']['身'] + job_param['治疗']['腿']) * 4
    unique_meterial[39] = unique_meterial[19] / 4
    unique_meterial[17] = job_param['法系']['腿'] * 4
    unique_meterial[42] = unique_meterial[17] / 4
    unique_meterial[5] = unique_meterial[39] + unique_meterial[42]
    unique_meterial[6] = (weapon['学者书'] + weapon['召唤书']) * 3
    unique_meterial[7] = weapon['学者书'] + weapon['召唤书']
    unique_meterial[8] = weapon['机工枪']
    unique_meterial[38] = job_param['坦克']['手'] + \
                        job_param['武士武僧']['头'] + job_param['武士武僧']['身'] + job_param['武士武僧']['手'] + job_param['武士武僧']['腿'] +  + job_param['武士武僧']['脚'] + \
                        job_param['忍者']['头'] + job_param['忍者']['手'] + job_param['忍者']['腿'] + \
                        job_param['龙骑']['身'] + job_param['龙骑']['手'] + \
                        job_param['治疗']['头'] + \
                        job_param['法系']['头'] + job_param['法系']['手'] + \
                        job_param['远敏']['头'] + job_param['远敏']['腿']
    unique_meterial[9] = unique_meterial[38] * 12
    for job in job_param.keys():
        unique_meterial[37] += (job_param[job]['耳'] + job_param[job]['项'] + job_param[job]['腕'] + job_param[job]['戒'])
    unique_meterial[37] *= 2
    unique_meterial[37] += job_param['坦克']['头'] + \
                        weapon['斧'] + weapon['骑士剑'] + weapon['大剑'] + weapon['法杖'] + weapon['天球仪'] + weapon['拳套'] + weapon['匕首'] + weapon['龙骑枪'] + weapon['魔杖'] + weapon['刺剑'] + weapon['弓']
    unique_meterial[40] = job_param['治疗']['手']
    unique_meterial[44] = unique_meterial[37] + unique_meterial[40] + weapon['武士刀'] + weapon['月轮']
    unique_meterial[10] = (weapon['武士刀'] + weapon['月轮'] + unique_meterial[44]) * 3
    unique_meterial[25] = weapon['骑士剑'] * 2 + weapon['拳套'] * 2 + weapon['斧'] * 3 + weapon['龙骑枪'] * 2 + weapon['弓'] + weapon['匕首'] * 2 + weapon['大剑'] * 3 + weapon['机工枪'] * 2 + weapon['魔杖'] + \
                        weapon['学者书'] + weapon['天球仪'] * 2 + weapon['武士刀'] * 3 + weapon['刺剑'] + weapon['枪刃'] * 3 + weapon['月轮'] * 3 + weapon['骑士盾'] * 2 + \
                        job_param['坦克']['头']+ job_param['坦克']['身'] * 2 + job_param['坦克']['手'] * 2 + job_param['坦克']['腰'] + job_param['坦克']['腿'] + job_param['坦克']['脚'] *2 + \
                        job_param['武士武僧']['手'] + job_param['武士武僧']['腰'] + \
                        job_param['忍者']['手'] + job_param['忍者']['腰'] + \
                        job_param['龙骑']['头'] * 2 + job_param['龙骑']['身'] * 3 + job_param['龙骑']['手'] * 2 + job_param['龙骑']['腰'] + job_param['龙骑']['脚'] * 2 + \
                        job_param['治疗']['腰'] + \
                        job_param['法系']['手'] + job_param['法系']['腰'] + \
                        job_param['远敏']['腰']
    unique_meterial[25] *= 2
    unique_meterial[11] = unique_meterial[25] * 2
    unique_meterial[30] = weapon['拳套'] * 2 + weapon['斧'] + weapon['匕首'] * 2 + weapon['大剑'] + weapon['机工枪'] * 2 + weapon['法杖'] * 2 + weapon['魔杖'] + \
                        weapon['天球仪'] * 2 + weapon['武士刀'] + weapon['刺剑'] * 3 + weapon['枪刃'] + weapon['月轮'] + \
                        job_param['坦克']['头'] * 2 + job_param['坦克']['身'] + job_param['坦克']['手'] + job_param['坦克']['腰'] + job_param['坦克']['耳'] + job_param['坦克']['项'] + job_param['坦克']['腕'] + job_param['坦克']['戒'] * 2 + \
                        job_param['龙骑']['身'] + job_param['龙骑']['手'] + job_param['龙骑']['腰'] + job_param['龙骑']['耳'] + job_param['龙骑']['项'] + job_param['龙骑']['腕'] + job_param['龙骑']['戒'] * 2 + \
                        job_param['武士武僧']['头'] * 2 + job_param['武士武僧']['腰'] + job_param['武士武僧']['耳'] + job_param['武士武僧']['项'] + job_param['武士武僧']['项'] + job_param['武士武僧']['戒'] * 2 + \
                        job_param['远敏']['头'] + job_param['远敏']['身'] + job_param['远敏']['手'] + job_param['远敏']['腰'] + job_param['远敏']['耳'] + job_param['远敏']['项'] + job_param['远敏']['腕'] + job_param['远敏']['戒'] * 2 + \
                        job_param['忍者']['身'] + job_param['忍者']['腰'] + job_param['忍者']['耳'] + job_param['忍者']['项'] + job_param['忍者']['腕'] + job_param['忍者']['戒'] * 2 + \
                        job_param['法系']['耳'] + job_param['法系']['项'] + job_param['法系']['腕'] + job_param['法系']['戒'] * 2 + \
                        job_param['治疗']['耳'] + job_param['治疗']['项'] + job_param['治疗']['腕'] + job_param['治疗']['戒'] * 2
    unique_meterial[30] *= 2
    unique_meterial[12] = unique_meterial[30] * 2
    unique_meterial[26] = job_param['坦克']['身']+ job_param['坦克']['腿'] * 2 + job_param['坦克']['脚'] + \
                        job_param['龙骑']['腿'] * 2 + job_param['龙骑']['脚'] + \
                        job_param['武士武僧']['身'] * 2 + job_param['武士武僧']['腿'] * 2 + \
                        job_param['远敏']['头'] * 2 + job_param['远敏']['身'] * 2 + job_param['远敏']['手'] * 2 +  job_param['远敏']['腿'] * 2 + \
                        job_param['忍者']['头'] * 2 + job_param['忍者']['身'] * 2 + job_param['忍者']['腿'] * 2 + \
                        job_param['治疗']['头'] * 2 + job_param['治疗']['身'] * 3 + job_param['治疗']['手'] * 2 + job_param['治疗']['腿'] * 2 + \
                        job_param['法系']['头'] * 2 + job_param['法系']['身'] * 2 + job_param['法系']['腿'] * 2
    unique_meterial[26] *= 2
    unique_meterial[13] = unique_meterial[26] * 2
    unique_meterial[31] = weapon['龙骑枪'] * 2 + weapon['弓'] * 3 + weapon['法杖'] * 2 + weapon['魔杖'] * 2 + weapon['召唤书'] * 2 + weapon['学者书'] + \
                        job_param['武士武僧']['脚'] + job_param['远敏']['脚'] + job_param['忍者']['脚'] + job_param['治疗']['脚'] + job_param['法系']['脚']
    unique_meterial[31] *= 2
    unique_meterial[14] = unique_meterial[31] * 2
    unique_meterial[15] = unique_meterial[37] * 3
    unique_meterial[16] = unique_meterial[40] * 3
    unique_meterial[18] = weapon['召唤书'] + weapon['学者书']
    unique_meterial[27] = weapon['召唤书'] * 2 + weapon['学者书'] * 2 + \
                        job_param['坦克']['腿'] * 2 + \
                        job_param['龙骑']['头'] + job_param['龙骑']['腿'] * 2 + \
                        job_param['武士武僧']['头'] + job_param['武士武僧']['身'] * 2 + job_param['武士武僧']['手'] * 2 + job_param['武士武僧']['腿'] * 2 + job_param['武士武僧']['脚'] * 2 + \
                        job_param['远敏']['身'] + job_param['远敏']['腿'] * 2 + job_param['远敏']['脚'] * 2 + \
                        job_param['忍者']['头'] + job_param['忍者']['身'] + job_param['忍者']['手'] * 2 + job_param['忍者']['腿'] * 2 + job_param['忍者']['脚'] * 2 + \
                        job_param['治疗']['头'] + job_param['治疗']['身'] + job_param['治疗']['腿'] * 2 + job_param['治疗']['脚'] * 2 + \
                        job_param['法系']['头'] + job_param['法系']['身'] + job_param['法系']['手'] * 2 + job_param['法系']['腿'] * 2 + job_param['法系']['脚']
    unique_meterial[27] *= 4
    for k in unique_param1.keys():
        unique_meterial[28] += unique_param1[k]
    for k in unique_param2.keys():
        unique_meterial[28] += unique_param2[k]
    unique_meterial[29] = unique_meterial[27] / 2
    unique_meterial[41] = unique_meterial[6] / 3
    unique_meterial[43] = weapon['机工枪']
    
    for meterial in unique_meterial.keys():
        unique_meterial[meterial] = int(unique_meterial[meterial])
    
    data += combine_result(unique_meterial)
    return data