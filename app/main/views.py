# -*- coding: utf-8 -*-
import json
import os
import re
import time
from datetime import datetime

from global_vars import CHAR_SPLIT_REGEX
from global_vars import COOKIE_FILENAME_MAP
from . import main
from ..models import TabConfig
import jieba
from flask import render_template, request

def strB2Q(uchar):
    """把字符串半角转全角"""
    inside_code = ord(uchar)
    code = inside_code
    if inside_code < 0x0020 or inside_code > 0x7e:      #不是半角字符就返回原来的字符
        code = inside_code
    elif inside_code == 0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
        code = 0x3000
    else:
        code = inside_code + 0xfee0
    return unichr(code)


path=os.path.dirname(__file__)
jieba.load_userdict(os.path.join(path, 'dict.simplified.txt'))
white_spaces = set([ strB2Q(u' '), strB2Q(u'\r'), strB2Q(u'\n'), strB2Q(u'\t') ])
assist_words = set([ strB2Q(' '), u'\r', u'\n', u'虽', u'昔', u'及', u'与', u'且', u'之', u'为', u'乎', u'也', u'于', u'以', u'乃', u'其', u'则', u'因', u'所', u'焉', u'何', u'者', u'若', u'乎', u'而', u'之', u'能', u'所', u'王'])


seq = 0


@main.route('/config/<path:key>', methods=['GET'])
def get_config():
    timeout = TabConfig.query.filter_by(key='biaodian/execise/time_limit').first().value
    return int(timeout)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@main.route('/test/new/<user>')
def new_test(user):
    global seq
    seq += 1
    return json.dumps(json.loads(u"""{
                "user": "%s",
                "testid": "%s",
                 "number": 1,
                 "question": "观自在菩萨行深般若波罗密多时照见五蕴皆空度一切苦厄"
                }""" % (user, str(int(time.time())) + str(seq))))


@main.route('/upload', methods=['POST'])
def upload():
    file_name = request.files['file'].filename
    origin_content = request.files['file'].stream.read().decode('gbk')
    parts = re.split(re.compile(u'【原典】|【白话语译】|【注释】|【校勘】'), origin_content)
    if len(parts) < 4 or len(parts) > 5:
        return json.dumps({'success': 'false', 'message': u'未找到合适的分隔符：【原典】，【白话语译】，【注释】'})

    title = u''.join(translate(parts[0]))
    origin = devide(translate(parts[1]))
    vernacular = devide(translate(parts[2]))
    comment =  u''.join([strB2Q(uc) for uc in parts[3]  if strB2Q(uc) not in [ strB2Q(u' '), strB2Q(u'\t') ]])
    collation = ''

    if len(parts) == 5:
        collation = translate(parts[4])

    # may do
    cookie_key = str(datetime.now().microsecond)
    COOKIE_FILENAME_MAP[cookie_key] = file_name

    return json.dumps({'success': 'true',
                       'parts': {'title': title, 'origin': origin, 'vernacular': vernacular, 'comment': comment,
                                 'collation': collation},
                       'cookie_key': cookie_key
                       })


@main.route('/convert', methods=['POST'])
def convert():
    params = request.json
    result = []

    origin_list = re.split(re.compile( u'[\r\n]+' ), params['original_text'])
    vernacular_list = re.split(re.compile(u'[\r\n]+'), params['vernacular_text'])
        
    comment_list = re.split(re.compile(u'[\r\n]+'), params['comment'])
    comment_map = {}
    for comment in comment_list:

        if len(comment) == 0:
            continue
        comment_parts = re.split(re.compile(u'：'), comment)
        if len(comment_parts) != 2:
            continue
        comment_map[comment_parts[0].strip()] = u'【%s】：%s' % ( comment_parts[0].strip(),  comment_parts[1] )

    cookie_key = str(request.cookies["cookie_key"])
    if cookie_key in COOKIE_FILENAME_MAP:
        # todo
        #print COOKIE_FILENAME_MAP[cookie_key]
        pass

    for idx, origin in enumerate(origin_list):
        if idx >= len( vernacular_list ):
            break
        result.append({
            "original_text": origin,
            "vernacular_text": vernacular_list[idx],
            "comment": get_line_contains_comment(origin, comment_map)
        })

    return json.dumps({"success": "true", "formatData": result})


def get_line_contains_comment(origin, comment_map):
    res = {} 
    for key in comment_map:
        if key in origin:
            res[key] = comment_map[key]

    for key in res:
        del comment_map[key]
    rel = u'' 
    for key in res:
        rel += res[key] + strB2Q( u' ' ) 
    return u'\r\n'.join( res.values())


def translate(origin_text):
    """
    filter special char in origin text
    :param origin_text:
    :return:
    """
    return [strB2Q(uc) for uc in origin_text  if strB2Q(uc) not in white_spaces ]

def devide( paragraph ):
    rel = []
    max_len = len( paragraph )
    curr_idx = 0
    while curr_idx < len( paragraph ):
        idx = find_next_split_point( paragraph, curr_idx )
        rel.append(  u''.join( paragraph[curr_idx:idx + 1]) + u'\r\n\r\n')
        curr_idx = idx + 1
    return u''.join(rel)
        

def find_next_split_point( paragraph, begin_idx ):
    idx = begin_idx
    while idx < len( paragraph ):
        if CHAR_SPLIT_REGEX.match(paragraph[idx]):
            
            if idx + 1 < len( paragraph ) and paragraph[idx+1] in [ u'’', u'”' ]:
                idx += 1
            return idx
        idx += 1

    return idx
            
def saveToExcel(filename, table):
    
    pass
