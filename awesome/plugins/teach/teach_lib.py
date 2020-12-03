from common import *
import sys
from nonebot.helpers import context_id, render_expression

def init_teach(teach_dict):
    try:
        f = open("./awesome/plugins/teach/teach_record.txt", "r")
    except FileNotFoundError:
        return
    else:
        for lines in f.readlines():
            column = lines.split(" ")
            if column[0] == '\n':
                continue
            if column[1] not in teach_dict.keys():
                value = []
                teacher = []
                image = []
                for i in range(column.index('value') + 1, column.index('teacher')):
                    value.append(column[i])
                for i in range(column.index('teacher') + 1, column.index('image')):
                    teacher.append(column[i])
                for i in range(column.index('image') + 1, column.index('\n')):
                    image.append(int(column[i]))
                teach_dict[column[1]] = {'value':value,'teacher':teacher,'image':image}
        f.close()
        self_debug("initialize teach dictionary success!!")

def save_teach(teach_dict):
    try:
        f = open("./awesome/plugins/teach/teach_record.txt", "w")
    except FileNotFoundError:
        return
    else:
        for key in teach_dict.keys():
            write_buf = "key " + key + " value "
            for value in teach_dict[key]['value']:
                write_buf = write_buf + value + ' '
            write_buf = write_buf + "teacher "
            for teacher in teach_dict[key]['teacher']:
                write_buf = write_buf + teacher + ' '
            write_buf = write_buf + "image "
            for image in teach_dict[key]['image']:
                write_buf = write_buf + str(image) + ' '
            write_buf = write_buf + '\n'
            f.write(write_buf)
        f.close()
        self_debug("save teach dictionary success!!")

def teach_mode_config(teach_dict, value, session):
    self_debug("send by function ------> --teach-mode")
    member_id = session.ctx['user_id']
    if member_id not in session.bot.config.SUPERUSERS:
        return "你不是我的主人，你不能设置！"
    if value == '1':
        teach_dict.teach_mode = 1
        return "设置成功"
    elif value == '0':
        teach_dict.teach_mode = 0
        return "设置成功"
    else:
        return "这是啥，模式只能为0或1"


def append_teach(content, teach_dict, member_name):
    teach_and_result = content.split('|')
    if len(teach_and_result) < 2:
        return "格式不对，请用|分隔，中间不要加空格"
    else:
        key_word = teach_and_result[0]
        value_start_index = len(teach_and_result[0]) + 1
        if content[len(content)-7:] == '--image':
            value_end_index = len(content)-7
        else:
            value_end_index = len(content)
        result_word = content[value_start_index : value_end_index]
        teacher = member_name
        #添    
        if key_word in teach_dict.keys():
            if result_word in teach_dict[key_word]['value']:
                self_debug("send by function ------> --teach")
                return "已经教过我这句啦"
            teach_dict[key_word]['value'].append(result_word)
            teach_dict[key_word]['teacher'].append(teacher)
            if content[len(content)-7:] == '--image':
                teach_dict[key_word]['image'].append(1)
            else:
                teach_dict[key_word]['image'].append(0)
            self_debug("send by function ------> --teach")
            return "我又学会了！"
        #学
        else:
            teach_sub_dict = {'value':[],'teacher':[],'image':[]}
            teach_sub_dict['value'].append(result_word)
            teach_sub_dict['teacher'].append(teacher)
            if content[len(content)-7:] == '--image':
                teach_sub_dict['image'].append(1)
            else:
                teach_sub_dict['image'].append(0)
            teach_dict[key_word] = teach_sub_dict                            
            self_debug("send by function ------> --teach")
            return "我学会了！"

def delete_teach(content, teach_dict):
    teach_and_result = content.split('|')
    key = teach_and_result[0]
    value = ''
    if len(teach_and_result) > 1:
        value = content[len(teach_and_result[0]) + 1:]
    if key in teach_dict.keys():
        if len(teach_dict[key]['value']) == 1 or value == '--all':
            del teach_dict[key]
            self_debug("send by function ------> --teach-delete")
            return "好的，我已经把这句话忘了"
        elif value != '' and value in len(teach_dict[key]['value']):
            index = teach_dict[key]['value'].index(value)
            teach_dict[key]['value'].remove(value)
            teach_dict[key]['teacher'].pop(index)
            teach_dict[key]['image'].pop(index)
            self_debug("send by function ------> --teach-delete")
            return "好的，我已经把这句话忘了"
        else:
            self_debug("send by function ------> --teach-delete")
            return "有人教过我这句吗？(挠头"
    else:
        self_debug("send by function ------> --teach-delete")
        return "有人教过我这句吗？(挠头"



def search_teach(key, teach_dict, teach_mode, image):
    self_debug("in function search_teach")
    if image == 0:
        send_value = render_expression(teach_dict[key]['value'])
    else:
        send_value_list = []
        for value in teach_dict[key]['value']:
            if teach_dict[key]['image'][teach_dict[key]['value'].index(value)] == image:
                send_value_list.append(value)
        if send_value_list == []:
            return ''
        send_value = render_expression(send_value_list)
    if teach_mode == 1:
        index = teach_dict[key]['value'].index(send_value)
        teacher = teach_dict[key]['teacher'][index]
        send_value = send_value + " (这句是" + teacher + "大佬教我的(小声嘀咕)"
    self_debug("send by function ------> search teach success")    
    return send_value



def check_image_match(content, char, key):
    if len(key) == 1:
        return 10
    confident = 1
    while len(content) > content.index(char) + confident and len(key) > key.index(char) + confident:
        if content[content.index(char)+confident] == key[key.index(char)+confident]:
            confident += 1
            continue
        else:
            break
    #confident 表示命中字数

    if confident == len(key):
        return 10
    if confident < 3:
        return 0
    elif confident > 10:
        return 10
    else:
        return confident
