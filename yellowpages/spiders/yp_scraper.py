import scrapy
import math
import pandas as pd
class YpSpider(scrapy.Spider):
    name = 'yp_scraper'
    
    input_file = './output_links/0-Alabama.csv'
    def start_requests(self):
        df = pd.read_csv(self.input_file)
        for i in range(0,len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_data)
    
    def start_requests(self):
        yield scrapy.Request(url="https://www.yellowpages.com/little-rock-ar/mip/river-valley-horticulture-products-11893886?lid=1002001917282",callback=self.parse_data)
        
    def parse_data(self, response):
        f = dict()
        f['name'] = response.xpath("//h1/text()").get()
        f['owner'] = ''
        f['general_info'] = "\n".join(response.xpath("//dd[@class='general-info']//text()").getall())
        f['location']  = ", ".join(response.xpath("//span[@class='address']//text()").getall())
        f['phone'] = response.xpath("//p[@class='phone']/text()").get()
        if(f['phone']):
            f['phone'] = f['phone'].strip()
        try:
            f['email'] = response.xpath("//a[@class='email-business']/@href").get().split(':')[-1]
        except:
            f['email'] = ''
        services = response.xpath("//dd[@class='features-services']//text()").getall()
        f['services'] = "".join(services)
        cats  = response.xpath("//dd[@class='categories']//text()").getall()
        f['categories'] = "".join(cats)

        f['website'] = response.xpath("//p[@class='website']/a/@href").get()
        f['logo'] = response.xpath("//dd[@class='logo']/img/@src").get()
        f['AKA'] = response.xpath("//dd[@class='aka']/p/text()").get()

        socials = response.xpath("//dd[@class='social-links']/a")
        for social in socials:
            f[social.xpath("./@class")] = social.xpath("./@href")
        
        f['Other_links'] = ", ".join(response.xpath("//a[@class='other-links']").getall())
        f['Other_Info'] = " ".join(response.xpath("//dd[@class='other-information']//text()").getall())
        f["Open_Hour"] = " ".join(response.xpath("//dd[@class='open-hours']//text()").getall())
        f['source_url'] = response.request.url
        # f['source_code'] = response.body
        yield f