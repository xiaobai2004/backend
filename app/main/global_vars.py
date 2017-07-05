# -*- coding: utf-8 -*-

import re

CHAR_FILTER_MAP = {
    "\\n": "<br/>"
}

CHAR_SPLIT_REGEX = re.compile(u'。|！|；|：|？')


COOKIE_FILENAME_MAP = {}
