import sys
sys.path.append('./awesome/plugins/teach/')
from teach_lib import init_teach


class teach_global:
    def __init__(self):
        self.teach_mode = 0
        self.teach_dict = dict()

    def __str__(self):
        s = ''
        for key in self.teach_dict:
            s += 'key '
            s += key
            s += ' value '
            for value in self.teach_dict[key]['value']:
                s += value + ' '
            s += 'teacher '
            for teacher in self.teach_dict[key]['teacher']:
                s += teacher + ' '
            s += 'image '
            for image in self.teach_dict[key]['image']:
                s += str(image) + ' '
            s += '\n'
        s += 'teach_mode ' + str(self.teach_mode)
        return s

    def teach_init_init(self):
        init_teach(self.teach_dict)