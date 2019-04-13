# -*- coding: utf-8 -*-
import json

import scrapy
from WineZero.items import WinezeroItem


class WineSpider(scrapy.Spider):
    name = 'Wine'
    allowed_domains = ['www.yesmywine.com']
    start_urls = ['https://list.yesmywine.com/z2-c1-p' + str(i) for i in range(1, 100)]

    def parse(self, response):
        for i in response.css('.pimg::attr(href)'):
            yield scrapy.Request('https:'+i.extract(),  callback=self.parse_wine_page)

    def parse_wine_page(self, response):
        item = WinezeroItem()
        item['name'] = response.css('.pro-name li h1::text').extract()[0].strip()  # 名称
        price = response.css('.myPrice em::text').extract()
        if len(price) == 0:
            item['price'] = '售罄'
            return item
        else:
            item['price'] = response.css('.myPrice em::text').extract()[0]   # 价格
            item['goodsId'] = response.css('.temperature span::text').extract()[0]  # 商品ID
            item['recentComments'] = response.css('.pro-data span a::text').extract()[0]  # 近期评论数
            item['recentSales'] = response.css('.pro-data span::text')[1].extract()  # 近期售出总数
            item['detail'] = json.dumps([{i.css('span b::text').extract()[0]: i.css('span::text')[1].extract().strip()}
                                         for i in response.css('.xiangqing ul li')])
            yield scrapy.Request('https://www.yesmywine.com/comment/v3/initGoodsComments.jspa?goodsId=' + item['goodsId'], callback=self.parse_comment, meta={'item': item})

    def parse_comment(self, response):
        item = response.meta['item']
        item['score'] = response.css('.m-score-circle em::text').extract()[0]  # 评分
        item['rank'] = ','.join(list(filter(lambda x:len(x) > 0, [i.extract().strip() for i in response.css('.m-percent dd::text')])))
        item['totalSale'] = response.css('.comment-grade span strong::text').extract()[0]
        return item

