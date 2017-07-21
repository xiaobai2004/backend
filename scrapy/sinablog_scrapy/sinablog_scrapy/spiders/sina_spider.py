# -*- coding: utf-8 -*-
import random, time
import scrapy
from scrapy.loader import ItemLoader
from sinablog_scrapy.items import BlogMetaItem, PrevBlogItem, ErrorItem, TextItem, ImageItem, next_seq
from scrapy.selector import Selector
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import html2text
import bs4


count = 0

class SinaSpider(scrapy.Spider):
    name = "sina"
    urls = ["http://blog.sina.com.cn/s/blog_489e98b90102xd2e.html"]
    def start_requests(self):
        for i, url in enumerate(self.urls):
            self.cur_url = url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_seq(1)
        bmItem = BlogMetaItem()
        bmItem['src_url'] = response.url

        bs = bs4.BeautifulSoup( response.body, 'html5lib' )
        
        bmItem['title'] = bs.find( 'div', {'class':'articalTitle'} ).h2.string
        bmItem['publish_date'] = bs.find( 'div', {'class':'articalTitle'} ).find( 'span', {'class':['time', 'SG_txtc']} ).string 
        bmItem['tags'] = u''.join( [ i.string + u'　'  for i in bs.find( 'div', id='sina_keyword_ad_area').table.tr.find( 'td', {'class':'blog_tag'}).find_all('a') ] ) 
        bmItem['classes'] = u''.join( [ i.string + u'　'  for i in bs.find( 'div', id='sina_keyword_ad_area').table.tr.find( 'td', {'class':'blog_class'}).find_all('a') ] ) 
        yield bmItem
        
        bs_body = bs.find( 'div', id="sina_keyword_ad_area2" )
        for aitem in self.extract_items( bs_body ):
            yield aitem

        
        next_seq(1)
        pbItem = PrevBlogItem()
        has_prev = [ i for (i, t) in enumerate( bs.find( 'div', {'class':['articalfrontback', 'SG_j_linedot1', 'clearfix']}).find_all( 'span')) if u'前' in t.string ] 
        if len( has_prev ) > 0:
            pbItem['url'] = bs.find( 'div', {'class':['articalfrontback', 'SG_j_linedot1', 'clearfix']}).find_all( 'a')[has_prev[0]]['href'] 
        else:
            pbItem['url'] = None
        yield pbItem

    def extract_items(self, item , indent=0):
        last_item = None
        inc = 1
        for sub_item in item.children:
            if last_item != None and last_item.name == 'wbr':
                inc = 0
            else:
                inc = 1
            last_item = sub_item

            print '    ' * indent + " ======= " + str(sub_item.name)

            if sub_item.name != u'img' and sub_item.string != None and len( sub_item.string.strip() ) > 0:
                if isinstance ( sub_item, bs4.element.NavigableString ):
                    next_seq(inc)
                    yield TextItem(text=sub_item.string) 
            if sub_item.name == u'img' and sub_item.get('real_src') != None:
                next_seq(1)
                yield ImageItem(image_urls=[ sub_item['real_src'] ])

            if 'children' in  dir( sub_item ) :
                for aitem in self.extract_items( sub_item, indent + 1 ):
                    yield aitem

