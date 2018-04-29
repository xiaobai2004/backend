# -*- coding: utf-8 -*-
import json
import os
import re
import time
from datetime import datetime
import uuid

from global_vars import CHAR_SPLIT_REGEX
from global_vars import COOKIE_FILENAME_MAP
from . import main
from ..models import TabConfig
import jieba
from flask import render_template, request, make_response, send_file, send_from_directory
import xlsxwriter
import config



@main.route('/zangjing/today_list', methods=['GET'])
def today_list():
    resp = make_response("""
    { "date": "20180429 04:30:00",
      "list" : [ { "title" : "妙法莲华经卷1",
               "section" : 1,
               "section_id" : 123456

            },

            { "title" : "妙法莲华经卷1",
               "section" : 2,
               "section_id" : 123457
            }
        ]
    }
    """)

    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'

    return resp
@main.route('/zangjing/section/<int:section_id>', methods=['GET'])
def get_section(section_id):
    resp = make_response("{'error' : 'section not found' }")

    if section_id == 123456:
        resp = make_response("""
        {
          "date": "20180429 04:30:00",
          "list": [
            {
              "title": "妙法莲华经卷1",
              "section": 1,
              "section_id": 123456
            },
            {
              "title": "妙法莲华经卷1",
              "section": 2,
              "section_id": 123457
            }
          ]
        }
        """)

    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'

    return resp

