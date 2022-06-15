import scrapy
class YpSpider(scrapy.Spider):
    name = 'yp'
    
    def start_requests(self):
        yield scrapy.Request(url=f"https://www.yellowpages.com/search?search_terms={self.query}&geo_location_terms={self.location}",callback=self.parse_links)

    def parse_links(self, response):
        urls = response.xpath("//h2/a/@href").getall()
        for url in urls:
            # yield scrapy.Request("https://www.yellowpages.com" + url, callback=self.parse_data)
            yield {'url':"https://www.yellowpages.com" + url, 'ref':response.request.url}
        
        next_page = response.xpath("//a[@class='next ajax-page']/@href").get()
        if(next_page):
            yield scrapy.Request(url="https://www.yellowpages.com"+next_page, callback=self.parse_links)
