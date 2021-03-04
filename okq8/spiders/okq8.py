import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from okq8.items import Article


class Okq8Spider(scrapy.Spider):
    name = 'okq8'
    start_urls = ['https://www.okq8.se/om-okq8/press/']

    def parse(self, response):
        links = response.xpath('(//div[@class="crate "])[1]//a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//time/@datetime').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="panel__text"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
