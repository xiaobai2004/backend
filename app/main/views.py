# -*- coding: utf-8 -*-
import time
import os
from flask import render_template, session, request, redirect, url_for, current_app
from .. import db
from ..models import User, TabConfig
from ..email import send_email
from . import main
from .forms import NameForm
import json
import re
import chardet
from global_vars import CHAR_FILTER_MAP
from global_vars import CHAR_SPLIT_REGEX
import jieba

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
def get_config(key):
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
    origin_content = request.files['file'].stream.read().decode('gbk')
    parts = re.split(re.compile(u'【原典】|【白话语译】|【注释】|【校勘】'), origin_content)
    if len(parts) < 4 or len(parts) > 5:
        return json.dumps({'success': 'false', 'message': u'未找到合适的分隔符：【原典】，【白话语译】，【注释】'})

    title = translate(parts[0])
    origin = translate(parts[1])
    vernacular = translate(parts[2])
    comment = translate(parts[3])
    collation = ''

    if len(parts) == 5:
        collation = translate(parts[4])

    return json.dumps({'success': 'true', 'parts': {
        'title': title,
        'origin': origin,
        'vernacular': vernacular,
        'comment': comment,
        'collation': collation
    }})


@main.route('/convert', methods=['POST'])
def convert():
    params = request.json
    result = []

    origin_set = [ w for w in set(jieba.cut(params['original_text'])) ]
    vernacular_set = [ w for w in set(jieba.cut(params['vernacular_text'])) ]

    origin_set = origin_set.intersection( vernacular_set )
    origin_set = None
    vernacular_set = None

    origin_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['original_text'])
    vernacular_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['vernacular_text'])
    idx_in_baihua=0
    for wenyanwen in origin_list:
        if idx_in_baihua >= len( vernacular_list ):
            break
        begin = idx_in_baihua
        words = [ w for w in jieba.cut( wenyanwen ) if w in origin_set ]
        while len( words ) != 0:
            for word in words:
                if word in vernacular_list[idx_in_baihua]:
                    del words[0]
                else:
                    idx_in_baihua += 1
        merged_baihua = u''.join( vernacular_list[begin:idx_in_baihua + 1 ] )
        vernacular_list[begin] = merged_baihua
        del vernacular_list[begin+1:idx_in_baihua+1]
                
        
    comment_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['comment'])
    comment_map = {}
    for comment in comment_list:

        if len(comment) == 0:
            continue
        comment_parts = re.split(re.compile(u'：'), comment)
        if len(comment_parts) != 2:
            continue
        comment_map[comment_parts[0].strip()] = comment_parts[1].strip()


    for idx, origin in enumerate(origin_list):
        result.append({
            "original_text": origin,
            "vernacular_text": vernacular_list[idx],
            "comment": get_line_contains_comment(origin, comment_map)
        })

    return json.dumps({"success": "true", "formatData": result})


def get_line_contains_comment(origin, comment_map):
    res = {}
    for (key, value) in comment_map.items():
        if key in origin and key not in res:
            res[key] = key + ":" + value

    for (key, value) in res.items():
        del comment_map[key]
    return res



def translate(origin_text):
    """
    filter special char in origin text
    :param origin_text:
    :return:
    """
    rel = [strB2Q(uc) for uc in origin_text  if strB2Q(uc) not in white_spaces ]

    
    return u''.join(rel)
