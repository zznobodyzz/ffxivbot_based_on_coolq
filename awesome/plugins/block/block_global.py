import sys
sys.path.append('./awesome/plugins/block')
from block_lib import init_block

class block_global:
    def __init__(self):
        self.block_list = []

    def __str__(self):
        s = ''
        for element in self.block_list:
            s += element
        return s

    def block_init_init(self):
        init_block(self.block_list)