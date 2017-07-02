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
    params = request.json
    result = []

    vernacular_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['vernacular_text'])
    comment_list = re.split(re.compile(CHAR_SPLIT_REGEX), params['comment'])
    comment_map = {}
    # count = 0
    # for comment in comment_list:
    #     count += 1
    #     print count
    #     comment_parts = re.split(re.compile(u'：'), comment)
    #     print comment_parts
    #     comment_map[comment_parts[0]] = comment_parts[1]

    for idx, origin in enumerate(origin_list):
        result.append({
            "original_text": origin,
            "vernacular_text": vernacular_list[idx],
            "comment": get_line_contains_comment(origin, comment_map)
        })

    print result[0]
    return json.dumps({"success": "true", "formatData": result})


def get_line_contains_comment(origin, comment_map):
    res = {}
    for (key, value) in comment_map:
        if key in origin and key not in res:
            res[key] = value
    return res


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
    rel = [strB2Q(uc) for uc in origin_text if strB2Q(uc) != strB2Q(u' ')]
    rel = u''.join(rel)
    return re.sub(re.compile('(\r\n)+|(\n)+'), '\r\n' + strB2Q(u' ') + strB2Q(u' '), rel)
