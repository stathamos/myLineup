import requests
import time
import pandas as pd
import Database


def converttuple(tup):
    """Convert tuple into list"""
    s = ''.join(tup)
    return s


def sql_column_to_list(ty):
    """Convert SQL column into list"""
    li = Database.c.execute('select tbl_name from sqlite_master where type = "table" and name like "' + ty +
                            '%"').fetchall()
    j = 0
    for i in li:
        li[j] = converttuple(i[0])
        j += 1
    return li


def listtostring(s):
    """Convert list into string"""
    s.sort()
    str1 = ""
    for ele in s:
        str1 += ele + ', '
    return str1[:-2]


def sql_query_to_list(query):
    """Convert SQL Query into list"""
    Database.conn.row_factory = Database.sqlite3.Row
    list_of_tuple = Database.c.execute(query).fetchall()
    li = []
    for i in list_of_tuple:
        li.append(i[0])
    return li


def count_element_list(li):
    """Count element in list"""
    li2 = []
    for i in li:
        if li.count(i) > 1:
            li2.append(str(li.count(i)) + ' - ' + i)
        else:
            li2.append(i)
    res = []
    for j in li2:
        if j not in res:
            res.append(j)
            res.sort()
    return res


def combinliste(seq, k):
    """Find possible combination in list"""
    p = []
    i, imax = 0, 2 ** len(seq) - 1
    while i <= imax:
        s = []
        j, jmax = 0, len(seq) - 1
        while j <= jmax:
            if (i >> j) & 1 == 1:
                s.append(seq[j])
            j += 1
        if len(s) == k:
            p.append(s)
        i += 1
    return p


def get_distinct_list(li):
    """Get distinct element from list"""
    for j in range(0, len(li)):
        li[j].sort()
    li_f = list()
    for sublist in li:
        if sublist not in li_f:
            li_f.append(sublist)
    li_f.sort()
    for j in range(0, len(li_f)):
        li_f[j].sort()
    return li_f


def weighted_average(df, data_col, weight_col, by_col):
    """Compute the weighted average of a column"""
    df['_data_times_weight'] = df[data_col] * df[weight_col]
    df['_weight_where_notnull'] = df[weight_col] * pd.notnull(df[data_col])
    g = df.groupby(by_col)
    result = g['_data_times_weight'].sum() / g['_weight_where_notnull'].sum()
    del df['_data_times_weight'], df['_weight_where_notnull']
    return result.to_frame(name=data_col)
