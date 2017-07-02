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
    # return json.dumps({'success': 'true', 'parts': {
    #     'origin': origin_content
    # }})
    # print chardet.detect(origin_content)
    parts = re.split(re.compile(u'【原典】|【白话语译】|【注释】'), origin_content)
    print len(parts)
    if len(parts) != 4:
        return json.dumps({'success': 'false', 'message': 'file format error'})

    title = translate(parts[0])
    origin = translate(parts[1])
    vernacular = translate(parts[2])
    comment = translate(parts[3])

    return json.dumps({'success': 'true', 'parts': {
        'title': parts[0],
        'origin': parts[1],
        'vernacular': parts[2],
        'comment': parts[3]
    }})


def translate(origin_text):
    """
    filter special char in origin text
    :param origin_text:
    :return:
    """
    final_text = origin_text
    for (key, value) in CHAR_FILTER_MAP.items():
        final_text = final_text.replace(key, value)

    return final_text