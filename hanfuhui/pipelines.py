# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import random
import os
import re

class ImagesPipeline(ImagesPipeline):

    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self,item,info):
        pictures = item["imgs"]
        for img_src in pictures:
            yield scrapy.Request(img_src)



    def item_completed(self,result,item,info):
        image_path = [x["path"] for ok,x in result if ok]
        pattern = re.compile(ur'[\u4e00-\u9fa5]+')
        result = pattern.findall(item["title"])
        imagename = "".join(result)
        path = self.IMAGES_STORE + "\\" + imagename
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        for each in image_path:
            os.rename(self.IMAGES_STORE + "\\" +each,path+'\\'+str(random.randint(1,999))+".jpg")
        return item
