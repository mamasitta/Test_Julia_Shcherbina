import csv


def to_list(param):
    s = param.strip("][")
    s1 = s.strip('""')
    formatted = s1.split(', ')
    give_back = []
    for i in range(len(formatted)):
        item = formatted[i].strip("''")
        give_back.insert(i, item)
    return give_back

