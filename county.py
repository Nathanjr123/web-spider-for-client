# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import csv
import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
with open(os.path.join(__location__, 'Mohave_Input.csv'), 'r') as f:
    reader = csv.reader(f)
    Parcel_list = list(reader)
    Parcel_list.pop(0)

class CountySpider(scrapy.Spider):
    name = 'county'
    allowed_domains = ['www.eagletw.mohavecounty.us']
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
    

    script = '''

        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15")
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(3))
            btn = assert(splash:select("input[type='submit']"))
            btn:mouse_click()
            assert(splash:wait(3))
            input_box = assert(splash:select("#TaxAParcelID"))
            input_box:focus()
            input_box:send_text('{0}')
            assert(splash:wait(0.5))
            btn1 = assert(splash:select("input[type='submit']"))
            btn1:mouse_click()
            assert(splash:wait(3))
            btn2 = assert(splash:select("font[color='#990000']"))
            btn2:mouse_click()
            assert(splash:wait(4))
            
            return splash:html()
        end

        


    '''
    for i in range(2):
        script=script.format(Parcel_list[i][0])
        def start_requests(self):
            yield SplashRequest(url="https://eagletw.mohavecounty.us/treasurer/web/splash.jsp", dont_filter=True,callback=self.parse,endpoint = "execute",args={
                'lua_source':self.script
            })


        def parse(self, response):
            print(response.body)
            print("--------------------------\n------------------------")
        
