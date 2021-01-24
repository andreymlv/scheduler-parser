# coding: utf8
#!/usr/bin/python3
 
import pandas as pd
import group as g

def execute(path: str):
    dfs = pd.read_html(path)
    groups = []
    for data in dfs:
        
        days = data[0]
        start_times = data[1]

        for column_index in range(2,data.shape[1]):

            column = data[column_index]
            group_name = column[0]
            group = update_group(group_name, groups)

            for row_index in range(3, len(column)):
                sbj_name = column[row_index]
                if pd.isnull(sbj_name) or pd.isnull(days[row_index]):#NaN check
                    continue
                sbj = group.add_subject(sbj_name, start_times[row_index], False, days[row_index])
                if start_times[row_index] == start_times[row_index - 1]:
                    sbj.is_even = True
    return groups

def update_group(group_name: str, dataframe: list):
    for group in dataframe:
        if group.name == group_name:
            return group
    a = g.Group(group_name)
    dataframe.append(a)
    return a