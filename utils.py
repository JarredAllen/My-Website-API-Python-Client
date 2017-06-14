################################################################################
#
# Some utilities for the main module, stored as functions here
#
################################################################################

from functools import reduce

__all__ = ['table']


def safe_len(foo):
    try:
        return len(foo)
    except TypeError:
        return 0


def center_pad(string, length):
    if len(string)>length:
        string = string[:max(0, length-3)]+'...'
    if len(string)<length:
        dif=length-len(string)
        pad=''.join(' ' for i in range(dif//2))
        string=pad+string+pad
        if dif & 1:
            string += ' '
    return string


def left_pad(string, length):
    if len(string)>length:
        string = string[:max(0, length-3)]+'...'
    if len(string)<length:
        pad = ''.join(' ' for i in range(length-len(string)))
        string = string+pad
    return string


def table(logs):
    print('-', len(logs), 'rows')
    data = [['Timestamp', 'IP Address', 'User ID', 'User Agent',
            'Calculation', 'Result']]
    for key in logs:
        data.append(logs[key])
    lens = [[safe_len(data[y][x]) for x in range(len(data[y]))]
            for y in range(len(data))]
    lens = [min(reduce(max, [lens[a][i] for a in range(len(lens))], 0), 42)+3
            for i in range(len(lens[0]))]
    out = '|'
    # print(lens)
    for a in range(len(data)):
        if a == 0:
            out += '-'.join('' for i in range(sum(lens)+6)) + '|\n|'
        for b in range(len(data[a])):
            if a == 0:
                out += center_pad(str(data[a][b]), lens[b]) + '|'
            else:
                out += left_pad(' '+str(data[a][b]), lens[b]) + '|'
        out += '\n|'
        if a == 0:
            out += '-'.join('' for i in range(sum(lens)+6))+'|\n|'
    return out + '-'.join('' for i in range(sum(lens)+6))+'|'

