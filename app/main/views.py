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
    origin_content = request.files['file'].stream.read()
    print chardet.detect(origin_content)
    parts = re.split(r'(\xe3\x80\x90\xe5\x8e\x9f\xe5\x85\xb8\xe3\x80\x91|\xe3\x80\x90\xe7\x99\xbd\xe8\xaf\x9d\xe8\xaf\xad\xe8\xaf\x91\xe3\x80\x91|\xe3\x80\x90\xe6\xb3\xa8\xe9\x87\x8a\xe3\x80\x91)\s*', origin_content)
    print len(parts)
    if len(parts) != 4:
        return json.dumps({'success': 'false', 'message': 'file format error'})
    title = parts[0]
    origin = parts[1]
    vernacular = parts[2]
    comment = parts[3]

    return json.dumps({'success': 'true', 'parts': {
        'title': parts[0],
        'origin': parts[1],
        'vernacular': parts[2],
        'comment': parts[3]
    }})
