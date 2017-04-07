# coding=utf-8
from __future__ import print_function

"""Generate sku data(per day) from action data"""

from Src.utils import config_util
import copy

sku_data_path = '../../Res/sku_action.txt'
sku_data_file = open(sku_data_path, 'a')


def __get_date(line):
    return line.split(',')[2].split(' ')[0]


def __get_sku(line):
    return line.split(',')[-1]


def __get_type(line):
    return line.split(',')[-3]


def __get_skuid(line):
    return line.split(',')[1]


def __get_userid(line):
    return line.split(',')[0]


def process_group(group):
    """Process each group, line within one group share the same day

    Args:
        group(list): List of line(striped)

    Returns:
        None

    """
    sku_list = [{
        'count': 0,
        'user': set()
    }] * 6

    sku_dict = {}
    # {'sku_id' : sku_list, 'sku_id' : sku_list}
    for line in group:
        sku_id = __get_sku(line)
        click_type = int(__get_type(line))
        user_id = __get_userid(line)
        if sku_id not in sku_dict:
            sku_dict[sku_id] = copy.deepcopy(sku_list)

        sku_dict[sku_id][click_type - 1]['count'] += 1
        sku_dict[sku_id][click_type - 1]['user'].add(user_id)

    for sku_id, sku_list in sku_dict.iteritems():
        line = [sku_id, __get_date(group[0])]
        for m_type in sku_list:
            line.append(m_type['count'])
            line.append(len(m_type['user']))

        write_line = ','.join([str(item) for item in line])
        print(write_line, file=sku_data_file)


def extract_sku_from(action_path):
    with open(action_path) as m_f:
        m_f.readline()
        line = m_f.readline()
        group = []
        pre_date = __get_date(line)
        group.append(line.strip())
        line = m_f.readline()
        while line:
            cur_date = __get_date(line)
            if cur_date == pre_date:
                # same group
                group.append(line.strip())
            else:
                # new group begin
                process_group(group)
                group = []
            pre_date = cur_date
            line = m_f.readline()
        process_group(group)


def main():
    action_path_keys = ['Action02',
                        'Action03',
                        'Action03_extra',
                        'Action04']
    action_paths = [config_util.get('Path', item) for item in action_path_keys]
    for path in action_paths:
        extract_sku_from(path)


if __name__ == '__main__':
    main()

'''
from Src.utils import config_util

file_p = config_util.get(section='Path', key='Action02')

with open(file_p,'r') as m_f:
    line = m_f.readline()
    line = m_f.readline()

    i = 0

    while line:
            # process your line
            row1 = line.replace("\n","")
            row = row1.split(',')
            print row[6]

            line = m_f.readline()
            i = i + 1
            if( i == 10 ):
                break
            # process end
'''