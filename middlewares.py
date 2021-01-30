# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time
import random
from selenium import webdriver
from scrapy.http import HtmlResponse


class JdBookDownloaderMiddleware:
    def __init__(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument('--headless')  # 浏览器不提供可视画面
        opt.add_argument('--user-agent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"')  # 设置请求头
        opt.add_argument('https://book.jd.com/booksort.html')
        self.driver = webdriver.Chrome(options=opt)

    def process_request(self, request, spider):
        if 'page' in request.url:
            self.driver.get(request.url)
            time.sleep(1)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 滚动滑动条触发懒加载
            time.sleep(1)
            html = self.driver.page_source  # 获取页面源码
            return HtmlResponse(url=request.url, body=html.encode())
        if "sort?source=bookSort" in request.url:
            t = int(time.time() * 1000)
            t1 = int(random.randint(10000, 99999))
            request.headers["callback"] = "jsonp_{0}_{1}".format(t, t1)
            request.headers["referer"] = "https://book.jd.com/"
        return None

    def close(self, spider):
        self.driver.quit()
