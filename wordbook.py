#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy
import ydcv
import sys
sys.path.append('./mdictlib')
from mdict_query import IndexBuilder
builder = IndexBuilder('./Collins.mdx')

def has_explains(result):
    return ('basic' in result) and ('explains' in result['basic'])

def get_explian_from_result(result):
    if not has_explains(result):
        return ''
    return ';'.join(result['basic']['explains'])

def translate_from_yd(word):
    result = ydcv.lookup_word_inner(word)
    return result

def if_in_collins(word):
    return len(builder.mdx_lookup(word)) > 0

df1 = pd.read_csv('./2018.12.20-wordbook-neat.txt',names=['worlds'])
df1 = df1.sort_values(by = 'worlds')
df1['yd_explain'] = df1['worlds'].apply(lambda x :translate_from_yd(x))
df1['expalins'] = df1['yd_explain'].apply(get_explian_from_result)
origin_word = df1['expalins'].str.extractall(r'[（\(]([a-z]+)的.*[）\)]').unstack()
df2 = df1.copy()
if len(origin_word) > 0:
    df2.loc[list(origin_word[0].index)] = origin_word[0]
df2 = df2.reindex(columns=['worlds','expalins'])
df2 = df2.drop_duplicates('worlds')
df_not_in_collins = df2[df2['worlds'].apply(lambda x: if_in_collins(x))]

df1.to_json('./words_queried_by_youdao.json')
df_not_in_collins.to_csv('./df_not_in_collins.csv')

df_not_in_collins['worlds'].to_csv('./neat_word_list.csv')