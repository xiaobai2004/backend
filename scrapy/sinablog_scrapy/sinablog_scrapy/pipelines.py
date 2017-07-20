# -*- coding: utf-8 -*-
from sinablog_scrapy.items import BlogMetaItem, PrevBlogItem, ErrorItem, TextItem, ImageItem
from scrapy.exceptions import DropItem
import time, os
from sinablog_scrapy import settings



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



title = None
publish_date = None

def save_text(item, content):
    suffix = ""
    if isinstance( item, BlogMetaItem ):
        suffix = ".meta"
    elif isinstance( item, PrevBlogItem ):
        suffix = ".prev"
    elif isinstance( item, ErrorItem ):
        suffix = ".err"
    elif isinstance( item, TextItem ):
        suffix = ".text"
    elif isinstance( item, ImageItem ):
        suffix = ".img"
    elif isinstance( item, PrevBlogItem ):
        suffix = ".next"

    print "================================================================================"
    print os.path.join( settings.DOCX_STORE, item['seq'] + suffix )
    f = open( os.path.join( settings.DOCX_STORE, item['seq'] + suffix ), 'ab+' )
    f.write( content.encode('UTF-8') + u'\n'.encode('UTF-8') )
    f.close()
    print "================================================================================"

class ErrorItemPipeline(object):
    def process_item(self, item, spider):
        global title
        global publish_date
        if not isinstance( item, ErrorItem ):
            return item
        try:
            if title != None:
                title = None
                publish_date = None
        finally:
            raise DropItem(item['error_msg'])

class BlogMetaPipeline(object):
    def process_item(self, item, spider):
        global title
        global publish_date 
        if not isinstance( item, BlogMetaItem ):
            return item

        if title == None:
            title = item['title'][0]
            publish_date = item['publish_date'][0].replace(u')', u'').replace(u'(', u'' ).replace( u'-', u'' ).replace( u':', u'' ).replace( u' ', u'-' )

        save_text(item, publish_date + u'-' + title + u'.docx' )
        save_text(item, item['title'][0])
        save_text(item, u"博客原文： " + item['src_url'] + u" \n")
        save_text(item, u"发布日期：" + item['publish_date'][0] + u"\n")
        save_text(item, u"标签： " + u'，'.join(item['tags']) + u"\n")
        save_text(item, u"分类： " + u''.join(item['classes']) + u"\n")


        return item

class PrevBlogPipeline(object):
    def process_item(self, item, spider):
        global title
        global publish_date
        if not isinstance( item, PrevBlogItem ): 
            return item

        title = None
        publish_date = None

        if item['spans'] != None and len ( item['spans'] ) > 0:
            has_prev_blog = u'前' in item['spans'][0]
            if has_prev_blog :
                next_url = item['urls'][0]
                save_text( item, next_url )


        return item 

class TextItemPipeline(object):
    def process_item(self, item, spider):
        if not isinstance( item, TextItem ):
            return item

        save_text( item, item['text'] )

        return item

class ImageItemPipeline(object):
    def process_item(self, item, spider):
        if not isinstance( item, ImageItem ):
            return item

        save_text( item, item['images'][0]['path'] )

        return item

