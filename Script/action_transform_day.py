# coding=utf-8

import sys

for line in sys.stdin:
    line_arr = line.strip().split(',')
    line_arr[2] = line_arr[2].split(' ')[0]
    print '%s' % (','.join(line_arr))
