import scrapy
from games_information.items import GamesInformationItem


class GameScrapy(scrapy.Spider):
    name = 'game'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search?term=%D0%B8%D0%BD%D0%B4%D0%B8&supportedlang=russian&page=1&ndl=1',
                  'https://store.steampowered.com/search?term=%D0%B8%D0%BD%D0%B4%D0%B8&supportedlang=russian&page=2&ndl=1',
                  'https://store.steampowered.com/search?term=minecraft&supportedlang=russian&page=1&ndl=1',
                  'https://store.steampowered.com/search?term=minecraft&supportedlang=russian&page=2&ndl=1',
                  'https://store.steampowered.com/search?term=%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B5%D0%B3%D0%B8%D0%B8&supportedlang=russian&page=1&ndl=1',
                  'https://store.steampowered.com/search?term=%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B5%D0%B3%D0%B8%D0%B8&supportedlang=russian&page=2&ndl=1',
                  'https://store.steampowered.com/search?term=%D0%B8%D0%BD%D0%B4%D0%B8&supportedlang=russian&page=1&ndl=1',
                  ]

    def start_requests(self):
        for link in self.start_urls:
            yield scrapy.Request(link, self.parse_games, meta={'link': link})

    def parse_games(self, response):
        urls = response.css('a.search_result_row::attr(href)').getall()
        for page in urls:
            item = GamesInformationItem()
            item['url'] = page
            yield scrapy.Request(page, self.parse, meta={'item': item})

    def parse(self, response):
        item = response.meta['item']
        item['name'] = response.css('div.apphub_AppName::text').get()
        if item['name'] is None or item['name'] == "":
            return
        item['release_date'] = response.css('div.release_date div.date::text').get()
        date = item['release_date'][-4:]
        if int(date) < 2020:
            return

        item['developer'] = response.css('div.dev_row a::text').get()
        item['price'] = response.css('div.discount_final_price::text').get()
        if item['price'] == "":
            item['price'] = 0
        else:
            try:
                item['price'] = item['price'].split()[0]
            except:
                pass
        item['platforms'] = ''
        if response.css('div.game_area_purchase_platform span.win').get():
            item['platforms'] += 'windows '
        if response.css('div.game_area_purchase_platform span.mac').get():
            item['platforms'] += 'mac '
        if response.css('div.game_area_purchase_platform span.linux').get():
            item['platforms'] += 'linux '

        try:
            item['category'] = response.css('div.breadcrumbs a::text').getall()[1:]
        except:
            pass

        try:
            item['reviews_score_and_quan'] = response.css('div.glance_ctn.glance_ctn div.summary.column span::text').getall()
            item['reviews_score_and_quan'] = item['reviews_score_and_quan'][0].strip() + item['reviews_score_and_quan'][1].strip()
        except:
            pass

        return item
