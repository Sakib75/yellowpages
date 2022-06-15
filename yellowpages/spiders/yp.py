import scrapy
import math
class YpSpider(scrapy.Spider):
    name = 'yp'
    
    def start_requests(self):
        yield scrapy.Request(url=f"https://www.yellowpages.com/search?search_terms={self.query}&geo_location_terms={self.location}",callback=self.get_total_page_no)

    def get_total_page_no(self, response):
        total = response.xpath("//div[@class='pagination']/span/text()").get()
        total_page = math.ceil(int(total.split('of')[-1].strip())/30)
        for i in range(0,total_page+2):
            page_url = f"https://www.yellowpages.com/search?search_terms={self.query}&geo_location_terms={self.location}&page={i}"
            print(page_url)
            yield scrapy.Request(url=page_url,callback=self.parse_links,dont_filter=True)

    def parse_links(self, response):
        urls = response.xpath("//h2/a/@href").getall()
        for url in urls:
            # yield scrapy.Request("https://www.yellowpages.com" + url, callback=self.parse_data)
            yield {'url':"https://www.yellowpages.com" + url}
    def parse_data(self, response):
        f = dict()
        f['name'] = response.xpath("//h1/text()").get()
        f['owner'] = ''
        f['general_info'] = "\n".join(response.xpath("//dd[@class='general-info']//text()").getall())
        f['location']  = ", ".join(response.xpath("//span[@class='address']//text()").getall())
        f['phone'] = response.xpath("//p[@class='phone']/text()").get()
        try:
            f['email'] = response.xpath("//a[@class='email-business']/@href").get().split(':')[-1]
        except:
            f['email'] = ''
        services = response.xpath("//dd[@class='features-services']//text()").getall()
        f['services'] = "".join(services)
        cats  = response.xpath("//dd[@class='categories']//text()").getall()
        f['categories'] = "".join(cats)
        f['source_url'] = response.request.url
        # f['source_code'] = response.body
        yield f