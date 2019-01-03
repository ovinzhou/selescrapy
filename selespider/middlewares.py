# -*- coding: utf-8 -*-
import random

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy_splash import SplashRequest
from selenium import webdriver

from selespider.settings import USER_AGENT_LIST

# splash lua script
script = """
         function main(splash, args)
             assert(splash:wait(0.5))
             assert(splash:go(args.url))
             return splash:html()
         end
         """


# class SplashDownloaderMiddleware(object):
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         yield SplashRequest(request.url, endpoint='execute', args={'lua_source': script}, callback=self.process_response)
#
#     def process_response(self, request, response, spider):
#         print('-'*50)
#         print(request.url)
#         return response
#
#     def process_exception(self, request, exception, spider):
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


class SelespiderDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # request.url  为当前请求的URL
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get(request.url)
        content = driver.page_source
        driver.quit()
        return HtmlResponse(url=request.url, body=content, request=request, status=200, encoding='utf-8')

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
