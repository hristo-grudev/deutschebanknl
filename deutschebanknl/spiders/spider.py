import scrapy

from scrapy.loader import ItemLoader
from ..items import DeutschebanknlItem
from itemloaders.processors import TakeFirst


class DeutschebanknlSpider(scrapy.Spider):
	name = 'deutschebanknl'
	start_urls = ['https://www.deutschebank.nl/nl/content/over_ons_nieuws_en_publicaties_actueel_nieuws.html',
	              'https://www.deutschebank.nl/nl/content/3972.html']

	def parse(self, response):
		post_links = response.xpath('//td[@class="absoluteleft newslistSimpleHeadline"]/a[1]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="rdtextfield"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@id="cc_02a_NewsArticle"]/text()').get()

		item = ItemLoader(item=DeutschebanknlItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
