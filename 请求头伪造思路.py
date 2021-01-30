import requests
import time
import json
import random

t = int(time.time()*1000)  # 生成时间戳
t1 = int(random.randint(10000, 99999))  # 生成五位数的随机数
url = "https://pjapi.jd.com/book/sort?source=bookSort"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "callback": "jsonp_'str(t)'_'str(t1)'",
    "referer": "https://book.jd.com/"
}

response = requests.get(url, headers=headers)
datalist = json.loads(response.content.decode())
for big_sort in datalist["data"]:
    b_id = big_sort["categoryId"]
    a = str(b_id)
    print(a)


