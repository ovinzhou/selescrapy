# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy_splash import SplashRequest

# splash lua script
script = """
         function main(splash, args)
             assert(splash:wait(0.5))
             assert(splash:go(args.url))
             return splash:html()
         end
         """

get_url = 'https://www.amazon.cn/s/ref=nb_sb_noss_2?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99' \
          '&url=search-alias%3Daps&field-keywords=%E6%89%8B%E6%9C%BA%E5%A3%B3'


class AmazonSpider(Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']

    # def start_requests(self):
    #     yield SplashRequest(get_url, callback=self.parse, endpoint='execute', args={'lua_source': script})
    #
    # def parse(self, response):
    #     # 获取请求头
    #     headers = response.request.headers.get('User-Agent')
    #     print(headers.decode('utf-8'))
    #     print(response)

    start_urls = ['https://www.amazon.cn/s/ref=nb_sb_noss_2?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=%E6%89%8B%E6%9C%BA%E5%A3%B3']

    def parse(self, response):
        print(response.text)
