import scrapy
import base64

class Generator_names(scrapy.Spider):
    name = "genrator_names_scraper"
    start_urls = ["https://www.behindthename.com/random/random.php?gender=both&number=1&sets=1&surname=&all=yes"]

    def parse(self, response):

        proxy = 'p.webshare.io:80'
        user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()

        for loop in range(0, 1000):
            link = "https://www.behindthename.com/random/random.php?gender=both&number=1&sets=1&surname=&all=yes&my_rand="+str(loop)
            yield scrapy.Request(link, callback=self.scrape_random_name,
                                 meta={'proxy': 'http://' + proxy},
                                 headers={'Proxy-Authorization': 'Basic ' + user_pass})

    def scrape_random_name(self, response):
        ramdom_name = response.css('div.random-results a.plain::text').extract_first()
        if ramdom_name != None:
            print("===============================================================")
            print("Name is : "+ramdom_name)
            print("===============================================================")