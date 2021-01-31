# JD_books_spider

### 京东图书爬取
#### 目标
- https://book.jd.com/booksort.html
将该网站上分类中的所有图书爬取下来

#### 步骤
- 通过研究发现上面的所有分类都是通过请求接口来渲染
- 所以通过抓包找到https://pjapi.jd.com/book/sort?source=bookSort&callback=jsonp_1606557102964_82922
伪造请求头获取数据
- 根据数据格式获取对于分类的详情页地址
- 进入详情页获取需要的信息
 - 因为页面是懒加载生成图书信息
 - 需要用到selenium作为中间件渲染页面
 
#### 新增
- 将原代码修改为scrapy-redis分布式爬虫
