import scrapy
import json
from copy import deepcopy
import time
import re


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jd.com']
    start_urls = ['https://pjapi.jd.com/book/sort?source=bookSort']

    def parse(self, response):
        datalist = json.loads(response.body.decode())
        for big_sort in datalist["data"]:
            item = {}
            item["b_cate"] = big_sort["categoryName"]
            b_id = str(int(big_sort["categoryId"]))
            item["b_link"] = "https://channel.jd.com/1713-{}.html".format(b_id)
            for small_sort in big_sort["sonList"]:
                item["s_cate"] = small_sort["categoryName"]
                s_id = str(int(small_sort["categoryId"]))
                item["s_link"] = "https://list.jd.com/list.html?cat=1713,{0},{1}&page=1".format(b_id, s_id)
                yield scrapy.Request(
                    item["s_link"],
                    callback=self.parse_book_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_book_list(self, response):
        # 京东图书是懒加载的，通过selenium作为中间件渲染页面
        item = response.meta["item"]
        li_list = response.xpath("//div[@id='J_goodsList']/ul/li")
        if len(li_list) == 0:
            print("似乎被重定向")
            time.sleep(3)
            print("重新发送请求")
            yield scrapy.Request(
                item["s_link"],
                callback=self.parse_book_list,
                meta={"item": item}
            )
        # 如果最后一页不满60个就会跳过这个判断不会创建请求
        if len(li_list) == 60:
            # https://list.jd.com/list.html?cat=1713,3258,3297&page=1
            list = re.split("&", item["s_link"])
            str1 = str(int(re.findall('\d+', list[1])[0]) + 2)  # 取page中的数字+2后转为字符串
            next_url = list[0] + "&page=" + str1
            print("拼接下一页url", next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_book_list,
                meta={"item": item}
            )
        for li in li_list:
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item["book_name"] = li.xpath(".//div[@class='p-name']//em/text()").extract_first()
            item["book_author"] = li.xpath(".//span[@class='p-bi-name']/a/@title").extract()
            item["book_publish"] = li.xpath(".//span[@class='p-bi-store']/a/@title").extract()
            item["book_publish_date"] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first()
            item["book_price"] = li.xpath(".//div[@class='p-price']//i/text()").extract_first()
            yield item

