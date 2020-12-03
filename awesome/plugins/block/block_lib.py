    
from common import *

def init_block(block_list):
    try:  
        f = open("./awesome/plugins/block/block_record.txt", "r")
    except FileNotFoundError:
        return
    else:
        for lines in f.readlines():
            lines = lines.replace('\n','')
            if lines not in block_list:
                block_list.append(lines)
        f.close()
        self_debug("initialize block list success!!")

def save_block(block_list):
    try:  
        f = open("./awesome/plugins/block/block_record.txt", "w")
    except FileNotFoundError:
        return
    else:
        for member in block_list:
            f.write(member + '\n')
        f.close()
        self_debug("save block list success!!")
        