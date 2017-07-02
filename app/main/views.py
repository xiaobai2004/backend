## -*- coding: utf-8 -*-  
import time
from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, TabConfig
from ..email import send_email
from . import main
from .forms import NameForm
import json


seq=0

@main.route('/config/<path:key>', methods=['GET'] )
def get_config(key):
    timeout = TabConfig.query.filter_by( key='biaodian/execise/time_limit').first().value
    return int(timeout)

@main.route('/config/<path:key>', methods=['POST'] )
def set_config(key):
    if key not in [ '', ]:
    value = None
    try:
        value=int(request.data)
    exept:
        abort(401)

    timeout = TabConfig.query.filter_by( key='biaodian/execise/time_limit').first().value
    return int(timeout)


@main.route('/', methods=['GET', 'POST'])
def index():
    content=u""" { "开始一个新的测试": {
      "request": "[GET, POST] test/new/<user>",
       "response": {
                "user": "<user>",
                "testid": "<testid>",
                 "number": 1,
                 "question": "观自在菩萨行深般若波罗密多时照见五蕴皆空度一切苦厄"
                }
        }
    }
    """
    obj=json.loads(content)
    output=json.dumps( json.loads(content), encoding=None)
    return output

@main.route('/test/new/<user>')
def new_test(user):
    global seq
    seq += 1
    return json.dumps( json.loads( u"""{
                "user": "%s",
                "testid": "%s",
                 "number": 1,
                 "question": "观自在菩萨行深般若波罗密多时照见五蕴皆空度一切苦厄"
                }""" %( user, str(int(time.time())) + str(seq) ) ) )


