# -*- coding: utf-8 -*-
import time
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
    print len(parts)
    print parts
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
    params = request.args.to_dict()
    result = []

    origin_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['original_text'])
    vernacular_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['vernacular_text'])
    comment_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['comment'])
    comment_map = {}
    for comment in comment_list:
        comment_parts = re.split(re.compile(u':|：'), comment)
        comment_map[comment_parts[0]] = comment_parts[1]

    # for idx, origin in enumerate(origin_list):
    #     result.append({
    #         "original_text": origin,
    #         "vernacular_text": vernacular_list[idx],
    #         "comment":
    #     })



    for (text_type, text) in params:
        result[text_type] = re.split(re.compile(CHAR_SPLIT_REGEX), text)


def get_line_contains_comment(origin_list, key):
    pass


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

def translate(origin_text):
    """
    filter special char in origin text
    :param origin_text:
    :return:
    """
    return u''.join(filter(lambda uc: uc if strB2Q(u' ') != uc else u'', map(lambda uc: strB2Q(uc), origin_text)))
