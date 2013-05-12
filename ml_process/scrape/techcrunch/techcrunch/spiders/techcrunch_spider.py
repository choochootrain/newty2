from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from techcrunch.items import TechcrunchItem

class TechcrunchSpider(BaseSpider):
  name = 'techcrunch'
  allowed_domains = ['techcrunch.com']
  start_urls = ['http://techcrunch.com/tag/apple/']

  def parse(self, response):
    hxs = HtmlXPathSelector(response)

    article_urls = hxs.select('//div[contains(@class, "post")]/h2/a/@href').extract()
    url_next = hxs.select('//div[contains(@class, "page-next")]/a/@href').extract()

    if url_next and len(url_next) > 0:
      print 'GRABBING PAGE', url_next[0]
      yield Request(url_next[0])

    for article_url in article_urls:
      yield Request(article_url, callback=self.parse_article)

  def parse_article(self, response):
    hxs = HtmlXPathSelector(response)
    body = hxs.select('//div[contains(@class, "module-post-detail")]')

    item = TechcrunchItem()
    item['title'] = body.select('h1[contains(@class, "headline")]/text()').extract()[0]
    item['author'] = body.select('div/h4/span/a/span[contains(@class, "name")]/text()').extract()[0]
    item['date'] = body.select('div/div[contains(@class, "post-time")]/text()').extract()[0]
    item['text'] = body.select('div[contains(@class, "body-copy")]').extract()[0]
    item['link'] = response.url

    return item
