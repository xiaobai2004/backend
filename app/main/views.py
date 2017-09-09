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


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@main.route('/upload', methods=['POST'])
def upload():
    file_name = request.files['file'].filename
    origin_content = u""
    raw_bytes = ""
    try:
        raw_bytes = request.files['file'].stream.read()
        origin_content = raw_bytes.decode('utf8')
        print "orginal content decoded as utf8"
    except:
        print "Faield to decoded as utf8"
        try:
            origin_content = raw_bytes.decode('gbk')
            print "orginal content decoded as gbk"
        except:
            print "Faield to decoded as gbk"
            origin_content = u''


    parts = split( origin_content )


    if len( parts['classic'] ) == 0 or len( parts['morden']) == 0:
        return json.dumps({'success': 'false', 'message': u'未找到合适的分隔符：【原典】，【译文】，【注释】'})

    title = u''.join(translate(u''.join(parts['heading'])))
    origin = devide(translate(u''.join(parts['classic'])))
    vernacular = devide(translate(u''.join(parts['morden'])))
    comment =  u''.join([strB2Q(uc) for uc in u'\r\n'.join(parts['comment']) if strB2Q(uc) not in [ strB2Q(u' '), strB2Q(u'\t') ]])
    collation = ''

    if len(parts['comment']) > 0:
        collation = translate(u''.join(parts['comment']))

    # may do
    cookie_file_key =  uuid.uuid4().hex
    cookie_file_name = file_name

    resp = make_response( json.dumps({'success': 'true',
                       'parts': {'title': title, 'origin': origin, 'vernacular': vernacular, 'comment': comment,
                                 'collation': collation},
                       'cookie_file_key': cookie_file_key,
                       'cookie_file_name': cookie_file_name
                       }) )
    resp.set_cookie( 'cookie_file_key', cookie_file_key )
    resp.set_cookie( 'cookie_file_name', cookie_file_name )
    return resp

def split( contents ):
    rel = { 'heading': [], 'classic': [], 'morden': [], 'comment': [], 'special_comment': [] }
    currentTag = None
    parts = re.split( re.compile( u'[\r\n]+' ), contents )
    for apart in parts:
        if len( apart.strip() ) == 0:
            continue

        if currentTag == None:
            tag = findTag( apart )
            if tag:
                currentTag = tag
            else:
                rel['heading'].append( apart )
        else:
            nextTag = findTag( apart )
            if nextTag:
                currentTag = nextTag
            else:
                rel[currentTag].append( apart )

    return rel

def findTag( apart ):
    if apart.strip().strip( u'\u200b\ufeff' ) in [ u'【原典】']:
        return 'classic'
    
    if apart.strip().strip( u'\u200b\ufeff' )  in [ u'【白话语译】', u'【译文】' ]:
        return 'morden'

    if apart.strip().strip( u'\u200b\ufeff' )  in [ u'【注释】']:
        return 'comment'

    if apart.strip().strip( u'\u200b\ufeff' )  in [ u'【校勘注释】', u'【校勘记】']:
        return 'special_comment'

    return None

@main.route('/convert', methods=['POST'])
def convert():
    params = request.json
    result = []

    origin_list = re.split(re.compile( u'[\r\n]+' ), u''.join(translate( params['original_text'], reserve_r_n=True)))
    vernacular_list = re.split(re.compile(u'[\r\n]+'), u''.join(translate(params['vernacular_text'], reserve_r_n=True)))
        
    comment_list = re.split(re.compile(u'[\r\n]+'), params['comment'])
    comment_map = []
    for i, comment in enumerate( comment_list ):

        if len(comment) == 0:
            continue
        comment_parts = re.split(re.compile(u'：'), comment)
        if len(comment_parts) < 2:
            continue
        comment_map.append( (i, comment_parts[0].strip(),  u'【%s】：%s' % ( comment_parts[0].strip(),  u'：'.join(comment_parts[1:]) ) ) )

    cookie_file_key = str(request.cookies["cookie_file_key"])
    cookie_file_name = unicode(request.cookies["cookie_file_name"])

    vernacular_idx = 0
    for idx, origin in enumerate(origin_list):
        if vernacular_idx < len( vernacular_list ):
            vernacular = vernacular_list[vernacular_idx]
        else:
            vernacular = ""
        vernacular_idx += 1
        result.append({
            "original_text": origin,
            "vernacular_text": vernacular,
            "comment": get_line_contains_comment(origin, comment_map)
        })

    while vernacular_idx < len( vernacular_list ):
        result.append({
            "original_text": "",
            "vernacular_text": vernacular_list[vernacular_idx],
            "comment": get_line_contains_comment(origin, comment_map)
        })
        vernacular_idx += 1

    save2excel( cookie_file_key, cookie_file_name, result )
    return json.dumps({"success": "true", "formatData": result})

@main.route('/excel/<file>', methods=['GET'])
def download_excel(file):
    path = config.cur_cfg.EXCEL_OUTPUT_PATH
    cookie_file_name = request.cookies["cookie_file_name"].replace(u'.txt', u'') + u'.xlsx'
    response = make_response(send_from_directory(path, file, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; mimetype=application/vnd.ms-excel; filename=%s" % cookie_file_name.encode('utf8')
    return response


def get_line_contains_comment(origin, comment_map):
    res = []
    for i, key,value in comment_map:
        if key in origin:
            res.append( ( i, key, value ) )

    for i, key, value in reversed( res ):
        comment_map[i] = ( i, u'#-#-#-not-exist-#-#', u'' )
    rel = u'' 
    for i,key,value in res:
        rel += value + strB2Q( u' ' ) 
    return u'\r\n'.join( map( lambda (i,k,value): value, res ) )


def translate(origin_text, reserve_r_n = False):
    """
    filter special char in origin text
    :param origin_text:
    :return:
    """
    if reserve_r_n:
        return [strB2Q(uc) for uc in origin_text  if strB2Q(uc) not in [ strB2Q(u' '), strB2Q(u'\t') ]]
    else:
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

def matchSentences( classic, morden ):
    classic = re.split( re.compile( u'[\r\n]+' ), classic )
    morden = re.split( re.compile( u'[\r\n]+' ), morden )
    morden_matched = []
    idx_begin = 0
    idx_end = idx_begin + 1 
    for sentence in classic:
        score = 0
        count = 0
        while idx_begin < len( morden ) and count < 5:
            count += 1
            classic_factor = makeFactor( sentence )
            morden_factor = makeFactor( morden[idx_begin, idx_end] )
            new_score = calcScore( classic_factor, morden_factor )
            if new_score >= score + 2:
                score = new_score
            else:
                break


        
        

def find_next_split_point( paragraph, begin_idx ):
    idx = begin_idx
    while idx < len( paragraph ):
        if CHAR_SPLIT_REGEX.match(paragraph[idx]):
            if idx + 1 < len( paragraph ) and paragraph[idx+1] in [ u'’', u'”' ]:
                idx += 1
            return idx
        idx += 1

    return idx

            
def save2excel(cookie_file_key, filename, table):
    path = config.cur_cfg.EXCEL_OUTPUT_PATH
    if not os.path.exists( path ):
        os.makedirs( path )
    workbook = xlsxwriter.Workbook(u'%s/%s.xlsx' % (path, cookie_file_key))

    try:
        worksheet = workbook.add_worksheet()
        formater_vjustify = workbook.add_format()
        formater_vjustify.set_text_wrap()
        formater_vjustify.set_align( 'vjustify' )

        formater_center = workbook.add_format()
        formater_center.set_align( 'center' )

        heads = [u'aWB出版篇码',u'书籍名称', u'句对序号', u'文言文', u'白话文', u'注释']
        widths = { 'A:A' : 12, 'B:B': 32, 'C:C' : 8, 'D:D' : 32 , 'E:E': 48, 'F:F' : 24 }

        for col in widths:
            worksheet.set_column( col , widths[col])
        
        for i, head in enumerate( heads ): 
            worksheet.write(0, i, heads[i])

        for i, row in enumerate( table ):
            worksheet.write(i + 1, 1, filename.replace(u'.txt', ''), formater_center)
            worksheet.write(i + 1, 2, i+1, formater_center)
            worksheet.write(i + 1, 3, remove_placeholder(row['original_text']), formater_vjustify)
            worksheet.write(i + 1, 4, remove_placeholder(row['vernacular_text']), formater_vjustify)
            worksheet.write(i + 1, 5, remove_placeholder(row['comment']), formater_vjustify)
    finally:
        workbook.close()
    
def remove_placeholder( content ):
    if content.strip() in [ u'#无#', u'＃无＃' ]:
        return u''
    return content
