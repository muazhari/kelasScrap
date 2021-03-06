import scrapy
import os


class spiderKelas(scrapy.Spider):
    tingkat = ['1', '2', '3', '4', '5']
    name = 'spiderKelas'
    allowed_domains = ['baak.gunadarma.ac.id']
    start_urls = ['https://baak.gunadarma.ac.id/kuliahUjian/3/' + x for x in tingkat]

    fileFormat = 'csv'
    fileName = 'kelas' + '.' + fileFormat
    fileAvailable = os.path.isfile(fileName)

    if fileAvailable:
        open(fileName, 'w+')

    custom_settings = {
        'FEED_FORMAT': fileFormat,
        'FEED_URI': fileName
    }

    def parse(self, response):
        MAIN_XPATH = '/html/body/div[1]/main/section/div/div/div/div[3]/div/div[2]/div[3]'

        TABLE_XPATH = MAIN_XPATH + '/table[1]'
        TABLE_SELECTOR = response.xpath(TABLE_XPATH)

        RECORD_XPATH = './/tr[position()>1 and position()<=last()]'
        RECORD_SELECTOR = TABLE_SELECTOR.xpath(RECORD_XPATH)

        for rset in RECORD_SELECTOR:
            yield {
                'nomor': rset.xpath('.//td[1]/text()').extract_first(),
                'kelas': rset.xpath('.//td[2]/text()').extract_first(),
                'dosen': rset.xpath('.//td[3]/text()').extract_first(),
            }

        NEXT_PAGE_SELECTOR = MAIN_XPATH + '/center/nav/ul/ul/li[last()]/a/@href'
        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
