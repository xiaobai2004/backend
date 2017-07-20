# -*- coding: utf-8 -*-
import random, time
import scrapy
from scrapy.loader import ItemLoader
from sinablog_scrapy.items import BlogMetaItem, PrevBlogItem, ErrorItem, TextItem, ImageItem
from scrapy.selector import Selector
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import html2text


count = 0

next_url = None 

class SinaSpider(scrapy.Spider):
    name = "sina"
    urls = ["http://blog.sina.com.cn/s/blog_489e98b90102xd2e.html"]
    def start_requests(self):
        for i, url in enumerate(self.urls):
            self.cur_url = url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bmItem = BlogMetaItem()
        bmItem['src_url'] = response.url
        l = ItemLoader(item=bmItem, response=response)
        bm_l = l.nested_xpath( '//div[@id="articlebody"]' )
        bm_l.add_xpath( 'title', './div[@class="articalTitle"]/h2/text()' )
        bm_l.add_xpath('publish_date', './div[@class="articalTitle"]/span[@class="time SG_txtc"]/text()')
        bm_l.add_xpath('tags',    '//div[@id="sina_keyword_ad_area"]/table/tr/td[@class="blog_tag"]//a/text()')
        bm_l.add_xpath('classes', '//div[@id="sina_keyword_ad_area"]/table/tr/td[@class="blog_class"]//a/text()')
        yield bm_l.load_item()


        try:
            for item in self.extract_content( response.xpath( '//div[@id="sina_keyword_ad_area2"]/*' ) ):
                 yield item

        except BaseException as e:
            e_i = ErrorItem()
            e_i['error_msg'] = str(e)
            yield e_i
        
        
        pbItem = PrevBlogItem()
        pb_l = ItemLoader(item=pbItem, response=response)
        pb_l.add_xpath( 'spans', '//div[@class="articalfrontback SG_j_linedot1 clearfix"]/div/span/text()' )
        pb_l.add_xpath( 'urls', '//div[@class="articalfrontback SG_j_linedot1 clearfix"]/div/a/@href' )
        yield pb_l.load_item()



    def extract_content(self, selector, indent=0):
        for section_selector in selector:
            tag_name =  section_selector.xpath( 'name()' ).extract_first()
            if 'wbr' == tag_name:
                continue
            if 'br' == tag_name:
                continue
            if tag_name == 'p' :
                #print ('    ' * indent ) + "===========tag_name==========="
                #print ('    ' * indent ) + tag_name
                text = html2text.html2text( section_selector.extract() )
                #print (u'    ' * indent ) + text
                if u'![' not in text:
                    yield TextItem(text=text)

            if tag_name == 'font' :
                #print ('    ' * indent ) + "===========tag_name==========="
                #print ('    ' * indent ) + tag_name
                text = html2text.html2text( section_selector.extract() )
                #print (u'    ' * indent ) + text
                yield TextItem(text=text)

 
            if tag_name == 'span' :
                #print ('    ' * indent ) + "===========tag_name==========="
                #print ('    ' * indent ) + tag_name
                text = html2text.html2text( section_selector.extract() )
                #print (u'    ' * indent ) + text
                yield TextItem(text=text)

            if tag_name == 'div' :
                #print ('    ' * indent ) + "===========tag_name==========="
                #print ('    ' * indent ) + tag_name
                text = html2text.html2text( section_selector.extract() )
                #print (u'    ' * indent ) + text
                sub_selector = section_selector.xpath( './*' )
                if sub_selector != None and len( sub_selector ) > 0:
                    pass
                else:
                    yield TextItem(text=text)

            if tag_name == 'a' :
                #print ('    ' * indent ) + "===========tag_name==========="
                #print ('    ' * indent ) + tag_name
                #print (u'    ' * indent ) + text
                sub_selector = section_selector.xpath( './text()' )
                if sub_selector != None and len( sub_selector ) > 0:
                    text = sub_selector.extract_first().strip()
                    if len( text ) > 0 and u'![' not in text :
                        yield TextItem(text=text)

            if tag_name == 'img':
                img_url = section_selector.xpath( '@real_src' ).extract_first()
                #print ('    ' * indent ) + "===========tag_name==========="
                #print ('    ' * indent ) + tag_name
                #print (u'    ' * indent ) + img_url
                yield ImageItem(image_urls=[img_url])

            sub_selector = section_selector.xpath( './*' )
            if sub_selector != None and len( sub_selector ) > 0:
                for item in  self.extract_content( sub_selector, indent + 1 ):
                    yield item

