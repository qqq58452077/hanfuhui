# -*- coding: utf-8 -*-
import scrapy
import random
import sys
import  lxml.html
from hanfuhui.items import HanfuhuiItem

reload(sys)

def LoadUserAgents(uafile):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile,'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas


class HanfuSpider(scrapy.Spider):
    name = 'hanfu'
    allowed_domains = ['www.hanfuhui.cn']
    page = 1
    url = "http://www.hanfuhui.cn/comm/album.ashx?action=loadAlbumGood&count=50&page="+str(page)
    start_urls = [url]
    uas = LoadUserAgents("user_agents.txt")


    def start_requests(self):
        ua = random.choice(self.uas)
        head = {'User-Agent': ua,
                'Host': 'www.hanfuhui.cn',
                'Referer':'http://www.hanfuhui.cn/album/'
                }
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 headers=head,
                                 dont_filter=True)



    def parse(self,response):
        tree = lxml.html.fromstring(response.text)
        album_list = tree.cssselect('ul.album_list >li')
        for album in album_list:
            item = HanfuhuiItem()
            a_name = album.cssselect('div.foot > p.top.long_hide > a.name')[0]
            a_nick = album.cssselect('div.foot > p.buttom > a.nick')[0]
            href = a_name.get('href')
            title = a_name.text
            author = a_nick.text
            item["href"] = href
            item["title"] = title
            item["author"] = author
            ua = random.choice(self.uas)
            head = {'User-Agent': ua,
                    'Host': 'www.hanfuhui.cn',
                    'Referer': 'http://www.hanfuhui.cn/album/'
                    }
            request = scrapy.Request('http://www.hanfuhui.cn'+href,callback=self.av_parse,headers=head,dont_filter=True)
            request.meta['item'] = item
            yield request
        self.page += 1
        ua = random.choice(self.uas)
        head = {'User-Agent': ua,
                'Host': 'www.hanfuhui.cn',
                'Referer': 'http://www.hanfuhui.cn/album/'
                }
        yield scrapy.Request("http://www.hanfuhui.cn/comm/album.ashx?action=loadAlbumGood&count=50&page="+str(self.page),callback=self.parse,
                                 headers=head,
                                 dont_filter=True)



    def av_parse(self,response):
        tree = lxml.html.fromstring(response.text)
        item = response.meta['item']
        list = []
        imgs = tree.cssselect('#mainer > div > div.data_info_main > div.life_piclist > li')
        for img in imgs:
            imgurl = img.cssselect('a > img')[0]
            href = imgurl.get('src')
            list.append(href[0:href.find('.jpg')+4])
        imgurls = set(list)
        item["imgs"] = imgurls
        yield item