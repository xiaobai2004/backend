# -*- coding: utf-8 -*-
from . import main
from flask import render_template, request, make_response, send_file, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from .. import db

from ..models import Scripture, Chapter, Section, Sentence, Reader, RecentList

#import Xls2DB

import json

@main.route('/wenbai/wenbai_upload', methods=['GET', 'POST'])
def wenbai_upload():
    if request.method == 'GET':
        return render_template("wenbai_reading_upload.html")
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        the_file = request.files['file']
        print the_file
        filename = secure_filename(file.filename)
        return redirect(url_for('main.wenbai_upload', filename=filename))


@main.route('/wenbai/today_list', methods=['GET'])
def today_list():

    scripture = db.session.query(Scripture.id, Scripture.scripture_display)
    rel = []
    for row in scripture:
        rel.append( { "id":row.id, "display":row.scripture_display} )

    resp = make_response(json.dumps(rel))

    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return resp


@main.route('/wenbai/scripture/<int:scripture_id>/section_id_list', methods=['GET'])
def get_section_id_list( scripture_id ):
    scripture = db.session.query(Scripture.id, Scripture.scripture_display).filter(Scripture.id == scripture_id).one()
    chapters = db.session.query(Chapter.id).filter(Chapter.scripture_id == scripture_id).all()
    chapter_id_list = [chapter.id for chapter in chapters]
    sections = db.session.query(Section.id).filter(Section.chapter_id.in_(chapter_id_list)).order_by(Section.id).all()

    rel = {"scripture_id": scripture.id, "scripture_display": scripture.scripture_display, "section_id_list": []}

    for section in sections:
        rel["section_id_list"].append(section.id)

    resp = make_response(json.dumps(rel))
    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return resp


@main.route('/wenbai/scripture/<int:scripture_id>/section/<int:section_id>/sentences', methods=['GET'])
def get_section(scripture_id, section_id):

    scripture = db.session.query(Scripture.id, Scripture.scripture_display).filter(Scripture.id == scripture_id).one()
    chapters = db.session.query(Chapter.id).filter(Chapter.scripture_id == scripture_id).all()
    chapter_id_list = [chapter.id for chapter in chapters]
    sections = db.session.query(Section.id).filter(Section.chapter_id.in_(chapter_id_list)).order_by(Section.id).all()
    sentences = db.session.query(Sentence).filter(Sentence.section_id == section_id ).order_by(Sentence.id).all()

    rel = dict()

    rel["scripture_id"] = scripture.id
    rel["scripture_display"] = scripture.scripture_display

    url_template_func = lambda x, y: "/wenbai/scripture/%d/section/%d/sentences" % (x, y)

    pos = -1
    for i, elem in enumerate(sections):
        if elem[0] == section_id:
            pos = i
            break

    rel["prev_section_url"] = url_template_func(scripture_id, sections[pos-1][0]) if pos > 0 else ""
    rel["next_section_url"] = url_template_func(scripture_id, sections[pos+1][0]) if pos < len(sections)-1 else ""

    section_id = None
    for sentence in sentences:
        if not section_id :
            section_id = sentence.section_id
            rel["section_id"] = section_id
            rel["sentences"] = []

        rel["sentences"].append({"sentence_id": sentence.id,
                                 "classic": sentence.classic_text,
                                 "modern": sentence.modern_text,
                                 "annotation": sentence.annotation_text if sentence.annotation_text else ""})

    resp = make_response(json.dumps(rel))
    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return resp

