# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
import urllib
from selespider.items import SelespiderItem

# splash lua script
script = """
         function main(splash, args)
             assert(splash:wait(0.5))
             assert(splash:go(args.url))
             return splash:html()
         end
         """

# 目前先请求第一页 然后获取下一页按钮的url 请求余下的页
base_url = 'https://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99' \
          '&url=search-alias%3Daps&field-keywords={}&rh=i%3Aaps%2Ck%3A{}'


base_link = 'https://www.amazon.cn/s/ref=sr_pg_{}?rh=i%3Aaps%2Ck%3A%E6%89%8B%E6%9C%BA%E5%A3%B3' \
            '&page={}&keywords=%E6%89%8B%E6%9C%BA%E5%A3%B3&ie=UTF8&qid=1546482631'


class AmazonSpider(Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']

    def start_requests(self):
        for page in range(1, 2):
            link = base_link.format(page, page)
            yield SplashRequest(link, callback=self.parse, endpoint='execute', args={'lua_source': script})

    def parse(self, response):
        # 获取请求头
        # headers = response.request.headers.get('User-Agent')
        # print(headers.decode('utf-8'))

        # with open('amazon.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)

        url_list = response.xpath('//*[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href').extract()
        name_list = response.xpath('//*[@class="s-access-image cfMarker"]/@alt').extract()
        image_list = response.xpath('//*[@class="s-access-image cfMarker"]/@src').extract()
        price_list = response.xpath('//*[@class="a-size-base a-color-price s-price a-text-bold"]/text()').extract()

        for url, name, image, price in zip(url_list, name_list, image_list, price_list):
            yield_url = 'https://www.amazon.cn' + url
            yield SplashRequest(yield_url, callback=self.next_parse, endpoint='execute', args={'lua_source': script}, meta={
                'name': name,
                'image': image,
                'price': price[1:],
            })

    def next_parse(self, response):
        print(response.meta)
        with open('amazon_detail.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        return
