from Src.utils import config_util

print(config_util.get(section='Path',key='Action03'))

file_p = '/Users/Data/JData_Action_201602.csv'

with open(file_p,'r') as m_f:
    line = m_f.readline()
    line = m_f.readline()

    while line:
            # process your line
            print line
            # process end
            line = m_f.readline()
            row = line.split(',')