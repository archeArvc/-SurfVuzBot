import scrapy


class VuzySpider(scrapy.Spider):
    name = "vuzy"
    allowed_domains = ["vuzoteka.ru"]
    start_urls = ["https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B/%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%B0"]

    def parse(self, response):
        information = response.xpath('//div[@class="label-part main-top-region first"]/div[@class="label-value"]/a/text()').getall()
        city_link = response.xpath('//div[@class="label-part main-top-region first"]/div[@class="label-value"]/a/@href').getall()
        for i in range(len(information)):
            yield {
                "City": information[i],
                "Link": city_link[i]
            }
