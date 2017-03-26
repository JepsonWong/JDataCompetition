# coding=utf-8
from __future__ import print_function
from Src.utils import redis_util
import copy
import extract_single

COLUMN = {
    0: "user",
    1: "sku",
    2: "time",
    3: "model",
    4: "type",
    5: "cate",
    6: "brand"
}

REDIS_COLUMN = {
    0: "userid",
    1: "skuid",
    2: "time",
    3: "modelid",
    4: "type",
    5: "cate",
    6: "brand"
}

TYPE = {
    1: "skim",
    2: "add_cart",
    3: "del_cart",
    4: "order",
    5: "attention",
    6: "click"
}


def extract_pair_from_redis(attr_index, pair_index, file_path):
    """Extract pair basic profile from redis.

    Args:
        attr_index(list): list of int, e.g. [3,4].
        pair_index(list): List of int, e.g. [1,2].
        file_path(str): Path to save the profile file.

    Returns:
        None
    """
    file_obj = open(file_path, 'a')

    m_dict = {
        'count': 0
    }
    for attr_i in attr_index:
        m_dict[COLUMN[attr_i]] = set()

    redis_cli_pair = redis_util.get_pair_db()
    match_pattern = '*:' + REDIS_COLUMN[pair_index[0]] + '_' + REDIS_COLUMN[pair_index[1]] + ':*'
    for record_key in redis_cli_pair.scan_iter(match=match_pattern):
        # Each record represents one line in result file
        value = [copy.deepcopy(m_dict),
                 copy.deepcopy(m_dict),
                 copy.deepcopy(m_dict),
                 copy.deepcopy(m_dict),
                 copy.deepcopy(m_dict),
                 copy.deepcopy(m_dict)]

        res_dict = {}

        len_record = redis_cli_pair.llen(record_key)

        for i in xrange(len_record):
            line = redis_cli_pair.lindex(record_key, i).strip()
            keys = []
            for key_i in pair_index:
                keys.append(extract_single.call_tbl[key_i](line))

            click_type = int(extract_single.get_type(line))

            attr_values = []

            for attr_i in attr_index:
                attr_values.append(extract_single.call_tbl[COLUMN[attr_i]](line))

            joint_key = "#".join(keys)
            if joint_key not in res_dict:
                res_dict[joint_key] = copy.deepcopy(value)

            res_dict[joint_key][click_type - 1]['count'] += 1

            for j in attr_index:
                res_dict[joint_key][click_type - 1][COLUMN[j]].add(attr_values[j])

        for m_joint_key, value in res_dict.iteritems():
            line = m_joint_key.split('#') + [record_key.split(':')[0]]
            for m_type in value:
                line.append(m_type['count'])
                for i in attr_index:
                    line.append(len(m_type[COLUMN[i]]))

            write_line = ','.join([str(item) for item in line])
            print(write_line, file=file_obj)
    if file_obj:
        file_obj.close()


def main():
    pass


if __name__ == '__main__':
    main()
