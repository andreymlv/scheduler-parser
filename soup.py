# coding: utf8
#!/usr/bin/python3
 
from bs4 import BeautifulSoup
import re
from group import Group
import json
#This is a crutch based on the idea of ​​this project alone
def create_table(rows):
    table = []
    for row in rows:
        row_elements = row.find_all('entry')
        markups = get_markup(row_elements)
        vals = []
        for markup in markups:
            val = pair_arr_to_str(markup)
            vals.append(val)
        table.append(vals)
    return table

def get_markup(row_elements):
    markup_arr = []
    for e in row_elements:
        markup_arr.append(e.find_all('para'))
    return markup_arr

def pair_arr_to_str(pair_arr):
    a = ''
    for e in pair_arr:
        if e.text == None:
            continue
        checked_str_arr = (str(e.text).replace('\n', '').replace('\xa0','').split(' '))
        for e in checked_str_arr:
            if not (e == ''):
                a += ' ' + e 
    return a[1:]

def check_config_pattern(row):
    #It's ugly
    if len(row) > 2 and row[0] == row[1] == '' and not(row[2] == '') and re.search('(лаб)',row[2]) == None and re.search('(лек)',row[2]) == None and re.search('(пр)',row[2]) == None:
        return True
    return False

def check_even_and_get_position(row):
    #It's ugly too
    if(len(row) >= 2):
        if check_time(row[0]):
            return 0
        elif check_time(row[1]):
            return 1
    return None

def check_time(e):
    if(not(re.search(r'\d+[.]\d+',e) == None)):
        return True
    return False

def execute(path):
    f = open(path, 'r')
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    f.close()

    rows = soup.find_all("row")
    table = create_table(rows)

    all_groups = []

    day = ''
    time_start = ''
    current_groups = []

    for row in table:
        is_pattern_config = check_config_pattern(row)

        if is_pattern_config:
            l = (list(map(lambda group: group.name, current_groups)))
            l.sort()
            r = row[2:]
            r.sort()
            if not (l == r):
                all_groups += current_groups
                current_groups = []
                for g in row[2:]:
                    current_groups.append(Group(g))
                continue
            else:
                continue


        pos = check_even_and_get_position(row)

        if(pos == None):
            for index in range(len(row)):
                if not(row[index] == ''):
                    current_groups[index].add_subject(row[index] , time_start , False , day)
            continue

        if(pos == 1):
            day = row[0]
            time_start = row[1]
            for index in range(len(row) - 2):
                if not(row[index + 2] == ''):
                    current_groups[index].add_subject(row[index + 2] , time_start , True , day)

        elif(pos == 0):
            time_start = row[0]
            for index in range(len(row) - 1):
                if not(row[index + 1] == ''):
                    current_groups[index].add_subject(row[index + 1] , time_start , True , day)

    all_groups += current_groups
    return all_groups