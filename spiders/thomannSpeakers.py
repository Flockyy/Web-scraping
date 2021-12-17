import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from thomannScraping.items import ThomannItem


class ThomannSpeakersSpider(CrawlSpider):
    name = 'thomannSpeakers'
    allowed_domains = ['thomann.de']
    start_urls = ['https://www.thomann.de/fr/haut_parleurs_passive_fullrange.html?ls=100&gk=PALPPF',
                  'https://www.thomann.de/fr/haut_parleurs_passive_fullrange.html?ls=100&pg=2&gk=PALPPF',
                  'https://www.thomann.de/fr/haut_parleurs_passive_fullrange.html?ls=100&pg=3&gk=PALPPF',
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//a[@class="product__content"]']), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
        item = ThomannItem()
        item['name'] = Selector(response).xpath('//h1[@class="fx-product-headline product-title__title"]/text()').extract()[0]
        item['observer'] = Selector(response).xpath('//span[@class="meta-box-value"][1]/text()').extract()[0]
        item['observer'] = ''.join(c for c in item['observer'] if c not in '\r\t\n')
        
        item['sell_rank'] = Selector(response).xpath('//span[@class="meta-box-value"]/a/text()').extract()[0]
        item['sell_rank'] = ''.join(c for c in item['sell_rank'] if c not in '\r\t\n')
        
        item['price'] = Selector(response).xpath('//div[@class="price-wrapper"]/div/text()[1]').extract()[0]
        item['price'] = ''.join(c for c in item['price'] if c not in '\r\t\n')
        
        item['features'] = Selector(response).xpath('//div[@class="text-original js-prod-text-original"]/ul/li/span/text()').extract()
        item['rating'] = Selector(response).xpath('//div[@class="rating"]/span/text()').extract()[0]
        item['nb_evaluation'] = Selector(response).xpath('//div[@class="product-reviews-header"]/div/h2/span/text()').extract()[0]
        yield item