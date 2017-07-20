# -*- coding: utf-8 -*-  
from docx import Document
from docx.shared import Inches
from sinablog_scrapy import settings
import os
from os.path import isfile, join

def text2docx():
    doc = Document()
    filename = ""
    with open( os.path.join( settings.DOCX_STORE, '100001.meta' ), 'r' ) as f:
        filename = f.readline().strip()
        if filename == None or len( filename ) == 0:
            print "Failed to find the blog meta data"
        title = f.readline().decode('UTF-8')
        content = f.readlines()
        content = u''.join( [ i.decode('UTF-8') for i in content if len( i.decode('UTF-8').strip() ) > 0  ] )
        doc.add_heading( title, 2 )
        doc.add_paragraph( content )

    files = [f for f in os.listdir(settings.DOCX_STORE) if ( 'img' in f or 'text' in f ) and isfile(join(settings.DOCX_STORE, f))]
    sorted( files )

    for afile in files:
        if 'img' in afile:
            img_file = open( os.path.join( settings.DOCX_STORE, afile ), 'r' ).readline().strip()
            doc.add_picture( os.path.join( settings.IMAGES_STORE, img_file  ) )
        elif 'text' in afile:
            with open( os.path.join( settings.DOCX_STORE, afile ), 'r' ) as f:
                print afile
                content = f.readlines()
                content = u''.join( [ i.decode('UTF-8') for i in content if len( i.decode('UTF-8').strip() ) > 0  ] )
                doc.add_paragraph( content )

    doc.save( os.path.join( '/var/tmp/sina_output', filename ))

text2docx()



