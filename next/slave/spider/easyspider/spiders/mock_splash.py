#coding=utf-8
from scrapy.spiders import CrawlSpider
import scrapy
import time
from scrapy_splash import SplashRequest

#import test

"""
成功的一次:
sudo docker run -p 8050:8050 scrapinghub/splash -v3
另外加上超时：

sudo docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 3600
sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
sudo docker run -p 8050:8050 scrapinghub/splash

sudo docker run -p 8050:8050 scrapinghub/splash -v3 --max-timeout 3600

"""

#test_crawl_url = "https://detail.1688.com/offer/1119287538.html"
#test_crawl_url = "https://www.bwcmall.com/"
test_crawl_url = "https://www.bwcmall.com/goods/detail.html?id=285133"
#test_crawl_url = "http://www.easygot.cn/this_page_id_not_exist.php"
#test_crawl_url = "http://www.easygot.cn/show_headers.php"
#test_crawl_url = "http://baike.baidu.com/link?url=lC0MAOAehOAwO_ua56_tVcHWH4OlrcAl6LkXuZB3M77U3LhY4PjlthbbeUtX0hAMQXS1X0pHr-soupIxhKG633plVEn59qW9P2Ss5GC0cpW"

#test_crawl_url = "https://zhidao.baidu.com/question/2138739646126399468.html"


#test_crawl_url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=218.77.55.134&rsv_pq=d1f909f50005954d&rsv_t=e6cd549U82EiXyegwUIxDCjfrJEkoDeqcECVq60U2N0fI9euINXHzZhksI8&rqlang=cn&rsv_enter=1&rsv_n=2&rsv_sug3=1&rsv_sug2=0&inputT=297&rsv_sug4=298"
splash_args = {
        # 'html': 1,
        # 'png': 1,
        # 'width': 600,
        # 'render_all': 1,
        "timeout":120,
        "wait":0.5


    }
class TestSpider(CrawlSpider):
	name = "mock_splash"
	start_urls = [test_crawl_url ]
	#allowed_domain = ["easygot.cn"]
	#start_urls = ["http://www.easygot.cn/show_headers.php","http://www.easygot.cn/show_cookies.php"]



	def start_requests(self,):
		for url in self.start_urls:
			#yield SplashRequest(url,callback=self.splash_parse,args={"wait":0.5}, endpoint='render.json',dont_filter=True)
			yield SplashRequest(url,callback=self.splash_parse,args=splash_args,dont_filter=True)


	def splash_parse(self,response):
		#@print request.header
		#print response.request.headers
		#print "cookie %s"%response.request.cookies
		print "you are in spider"
		#print response.body
		#print dir(response)
		print response.body
		#print response.text
		print "\n\n\n\n"
		import re
		print re.findall("GSR12-2",response.body)
		#print re.findall(response.body,"GSR12-2")

		#yield scrapy.http.Request(url="http://www.baidu.com",callback=self.parse)
		#return {
		#	"time":time.ctime(),
		#	"url":response.url,
		#	"content":response.body
		#}
