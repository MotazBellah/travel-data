# -*- coding: utf-8 -*-
import scrapy

class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['www.booking.com', 'www.expedia.com']

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',}

    def start_requests(self):
        yield scrapy.Request(url='''https://www.booking.com/searchresults.html?label=gen173nr-1FCAQoggJCDGNpdHlfLTI5MDI2M0gBWARoQ4gBAZgBAbgBF8gBDNgBAegBAfgBAogCAagCA7gCx_7q_AXAAgHSAiQ3ZjNmMWU3My0wOTZhLTQ5YjMtOGE0Zi1kZGU2OTAyM2JiMWXYAgXgAgE;sid=12a8b409f259b2760cdf245b9e549b54;tmpl=searchresults;checkin_year_month_monthday={1};checkout_year_month_monthday={2};class_interval=1;dest_type=city;group_adults={4};group_children=0;label_click=undef;no_rooms={3};offset=0;raw_dest_type=city;sb_price_type=total;shw_aparth=1;slp_r_match=0;srpvid=90a28466542d013c;ss={0};ss_all=0;ssb=empty;sshis=0;top_ufis=1&;selected_currency=USD'''.format(self.city, self.checkin, self.checkout, self.room, self.traveler),
        callback=self.parse_booking, headers=self.header)


        yield scrapy.Request(url='''https://www.expedia.com/Hotel-Search?adults={4}%2C1&d1={1}&d2={2}&destination={0}&endDate={2}&rooms={3}&semdtl=&sort=RECOMMENDED&startDate={1}&theme=&useRewards=false&userIntent'''.format(self.city, self.checkin, self.checkout, self.room, self.traveler),
        callback=self.parse_expedia)


    def parse_expedia(self, response):
        expedia_hotels = response.xpath("//ol[@class='results-list no-bullet']/li")
        for i in expedia_hotels:
            name = i.xpath(".//div/div/div/h3/text()").get()
            link = i.xpath(".//div/div/a/@href").get()
            rating = i.xpath(".//div/div/div[2]/div/div/div/div/span/span/text()").get()
            total_rating = i.xpath(".//div/div/div[2]/div/div/div/div/span/span/text()[2]").get()
            price = i.xpath(".//div/div/div[2]/div/div[2]/div/div/div[3]/text()").get()
            location = i.xpath(".//div/div/div/div[@class='uitk-grid all-cell-fill']/div/div/text()").get()
            img = i.xpath(".//div/section/span/div/div/div[2]/figure/div/img/@src").get()
            if not img:
                img = i.xpath(".//div/section/div/div/div[2]/figure/div/img/@src").get()

            yield {
                "source": 'Expedia',
                'name': name,
                "rating": str(rating) + str(total_rating),
                "price": price.split(',')[0],
                "location": location,
                "link": "https://www.expedia.com"+link,
            }

    def parse_booking(self, response):

        hotels = response.xpath("//div[@id='hotellist_inner']/div")

        for hotel in hotels:
            # print(hotel)
            img = hotel.xpath(".//img/@src").get()
            title = hotel.xpath("normalize-space(.//h3/a/span/text())").get()
            rating = hotel.xpath("normalize-space(.//div[@class='bui-review-score__badge']/text())").get()
            link = hotel.xpath("normalize-space(.//h3/a/@href)").get()
            room = hotel.xpath("normalize-space(.//div[@class='sr_item_content sr_item_content_slider_wrapper ']/div[@class='sr_rooms_table_block clearfix sr_card_rooms_container']/div/div/table/tbody/tr/td[3]/div/div/div/text())").get()

            if not room:
                room = hotel.xpath("normalize-space(.//div[@class='sr_item_content sr_item_content_slider_wrapper ']/div[@class='sr_rooms_table_block clearfix sr_card_rooms_container']/div/div/div/div/div[@class='roomPrice roomPrice_flex  sr_discount ']/div/div[1]/div[@class='bui-price-display__label prco-inline-block-maker-helper']/text())").get()
            pric = hotel.xpath("normalize-space(.//div[@class='sr_item_content sr_item_content_slider_wrapper ']/div[@class='sr_rooms_table_block clearfix sr_card_rooms_container']/div/div/table/tbody/tr/td[3]/div/div[2]/div/div[@class='bui-price-display__value prco-inline-block-maker-helper ']/text())").get()
            if not pric:
                pric = hotel.xpath("normalize-space(.//div[@class='sr_item_content sr_item_content_slider_wrapper ']/div[@class='sr_rooms_table_block clearfix sr_card_rooms_container']/div/div/div/div/div[@class='roomPrice roomPrice_flex  sr_discount ']/div/div[2]/div/div/text())").get()
            try:
                # pass
                yield response.follow(url=link, callback=self.parse_hotel, meta={'title': title, 'rating': rating, 'img': img, 'pric': pric, 'room': room, "link":link})
            except Exception as e:
                yield {
                    "source": 'Booking',
                    "name": title,
                    "rating": rating,
                    "price": str(yy.replace('\xa0', ' ')) + ' - ' + str(room),
                    'location':'N/A',
                    "link": 'N/A'
                }


    def parse_hotel(self, response):
        img = response.request.meta['img']
        title = response.request.meta['title']
        rating = response.request.meta['rating']
        price = response.request.meta['pric']
        room = response.request.meta['room']
        link = response.request.meta['link']


        loc = response.xpath("normalize-space(//p[@id='showMap2']/span/text())").get()

        yield {
            "source": 'Booking',
            "name": title,
            "rating": rating,
            "price": str(price.replace('\xa0', ' ')) + ' - ' + str(room),
            'location':loc,
            "link": "https://www.booking.com"+link,
        }
