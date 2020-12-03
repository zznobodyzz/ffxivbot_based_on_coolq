import time
from nonebot.helpers import render_expression

SYSTEM_ERROR_REPLY= '#######################\n' \
                    '     system warning\n' \
                    '#######################\n' \
                    '      核心温度过高'


def self_debug(sentence):
    current_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    print("%s [SELF-DEBUG] %s" %(current_time, sentence))


def search_next_line(src_data, comp_data):
    comp_data_tmp = comp_data.replace(' ','').replace('\t','')
    lines = src_data.split('\n')
    flag = 0
    for line in lines:
        line_tmp = line.replace(' ','').replace('\t','')
        if len(line_tmp) >= len(comp_data_tmp):
            if line_tmp[0:len(comp_data_tmp)] == comp_data_tmp:
                return lines[lines.index(line) + 1]
    return " "
                
def search_data(src_data, comp_data):
    lines = src_data.split('\n')
    for line in lines:
        line = line.replace(' ','')
        line = line.replace('\t','')
        if len(line) > len(comp_data):
            if line[0:len(comp_data)] == comp_data:
                return line[len(comp_data):]
    return " "

def check_string_contain_word_num(content, word):
    count = 0
    for char in content:
        if char == word[0]:
            count = count + 1
    return count
    

def find_string(where, find):
    if len(where) < len(find):
        return -1
            
    for index in range(0,len(where)):
        find_index = 0
        where_index = 0
        while where[index + where_index] == find[find_index]:
            where_index = where_index + 1
            find_index = find_index + 1
            if find_index == len(find):
                return index
            if index + where_index == len(where):
                return -1
    return -1


def return_random_with_additional_element(main_reply, additional_reply):
    for reply in additional_reply:
        main_reply.append(reply)
    msg = render_expression(main_reply)
    for reply in additional_reply:
        main_reply.remove(reply)
    return msg

def check_if_match_apart(src_data, comp_data):
    if len(src_data) >= len(comp_data):
        for i in range(0,len(src_data)-len(comp_data)+1):
            if src_data[i:i + len(comp_data)] == comp_data:
                return True
    return False