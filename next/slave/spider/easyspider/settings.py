#coding=utf-8

#-----------mysql配置---------------------

MYSQL_HOST = "123.56.16.155"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "zhanghang123321"
MYSQL_DBNAME = "Network_Information_Monitoring"

RECORD_DB_NAME = "crawl_records"

#-------------------------------------------

#---------使用scrapyjs-------------------

#SPLASH_URL = "http://localhost:8050"
SPLASH_URL = "http://www.easygot.cn:8050"

SPIDER_MIDDLEWARES = {
    "scrapy_splash.SplashDeduplicateArgsMiddleware":100
}

DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"

HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"

#--------使用scrapyjs----------


DOWNLOAD_TIMEOUT = 3600
DOWNLOAD_DELAY = 5

#为什么只能取到大写的settings，小写的取不到，没有作用？？？
#看源码，读取解析settings文件，是在settings/__init__.py中，函数 overridden_settings(settings)
#函数overridden_settings() 是根据 iter_default_settings一个个的去遍历 settings/下的default_settings.py，一个个的对比
#而 iter_default_settings() 是
# if name.isupper() 才会添加进去对比，所以只有大写的项目设定才会被添加进去对比
test="测试是否在settings文件中写什么都能被提取到"
#一定要大写才能被提取到，小写取不到
TEST="测试是否在settings文件中写什么都能被提取到 \n\n 一定要大写才能被提取到，小写取不到"

SPIDER_MODULES = ['easyspider.spiders']
NEWSPIDER_MODULE = 'easyspider.spiders'



SQLITE_DB="用来引发 check_deprecated_settings 的响应"

#如果需要账号密码的redis链接
REDIS_URL = "redis://:zhanghang1003@123.56.16.155:6379/0"
#如果不需要账号密码的本地连接
#local_url = "redis://:@localhost:6379/0"


#=====================scrapy-redis替换的文件==============================

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    'easyspider.pipelines.pipelines.ExamplePipeline': 300,
    #'scrapy_redis.pipelines.RedisPipeline': 400,
    "easyspider.pipelines.Baidu_search_pipelines.MysqlPipeline":500
}

#=====================scrapy-redis替换的文件==============================




# 几个点：
# 1. 这里定义的中间件，不会覆盖默认的中间件，而是去合并，根据大小的顺序去和默认的中间件合并，然后得到一个有序列表
# 2. 既然不会覆盖，想禁用怎么办...那就将他设置为None，就达到了禁用的效果，关闭了这个中间件，否则不会被禁用
# 3. 顺序问题：合并后的中间件有序列表，第一个中间件是最靠近引擎的，最后一个中间件是最靠近下载器的
DOWNLOADER_MIDDLEWARES = {
	#该中间件过滤所有被robots.txt禁止的requests.
	#但是起效，必须同时设置尊重robots.txt协议，也就是settings中设置 【ROBOTSTXT_OBEY = True . 】这个默认值是False
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    #该中间件完成某些使用HTTP认证请求的过程，开启http认证。 什么是http认证，就是比如路由器弹出的对话框要你输入账号密码来打开。http://www.cnblogs.com/youxilua/archive/2013/06/15/3137236.html
    #但是要使用这个认证，必须要在spider中设置关键字 http_user 和 http_pass 这两个属性，这样就会自动的去认证.比如
    #Class Domz(CrawlSpider):
    #   http_user = "someuser"
    #   http_pass = "somepass"
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    #该中间件设置 【DOWNLOADER_TIMEOUT】指定的超时时间
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,

   

    #------------------------------------------------------------------------------
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
 	#修改UA头
	"scrapy.downloadermiddlewares.useragent.UserAgentMiddleware":None,
	"easyspider.middlewares.useragent.UserAgentMiddleware":400,
	#------------------------------------------------------------------------------
    
	#该中间件控制由于临时的问题(连接超时或者500的错误)是否继续重试的动作
	#注意：这里收集的失败页面，是在spider 抓取完所有的 正常 网页之后再进行的重试...一旦没有更多的需要重试的失败的页面..该中间件就会发送一个【retry_complete】的信号...其他的插件可以监听这个信号
	#同时注意，这个中间件是配合其他的settings共同作用的。这里的配合的中间件主要有：
	#【RETRY_ENABLE】默认为True
	#【RETRY_TIMES】包括第一次下载，包括第一次，最多的重试次数。默认为 2
	#【RETRY_HTTP_CODES】 需要重试的http codes的返回值，默认是数组[500, 502, 503, 400, 408]  但是注意：其他的错误，比如DNS查找问题，链接失败或者其他，一定会进行重试的 
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    #该中间件用来设置默认的请求头request header 比如默认的
 	# Host : www.easygot.cn
	# Accept-Language : en
	# Accept-Encoding : gzip,deflate
	# Accept : text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
	#这个，就是由这个中间件控制的...
	#注意：这个中间件其效果，是要配合settings中的 【DEFAULT_REQUEST_HEADERS】来产生的，而【DEFAULT_REQUEST_HEADERS】默认值是：
	# {
	#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	#     'Accept-Language': 'en',
	# }
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    #该中间件提供对压缩(gzip,default)数据的支持
    #该中间件同时需要配合settings中的【COMPRESSION_ENABLED】来使用...【COMPRESSION_ENABLED】用来标志压缩中间件是否开启，默认为True

    #-------------------------------------------------
    #为了在使用 splash 中...避免混淆干脆让他注释掉，不出现
    #splash 说是需要为了什么高级响应的问题，而需要调整   HttpCompressionMiddleware 出现的顺序 
    #-------------------------------------------------
    #'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    #该中间件是根据response的状态来处理重定向的request
    #同样的，他也需要settings的配合来使用，控制的两个值是这样的
    #【REDIRECT_ENABLED】默认为True
    #【REDIRECT_MAX_TIMES】单个request被重定向的最大次数 默认为20


    #'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    




    #为了记录着想，升级到960试试
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    "easyspider.middlewares.redirect.RedirectMiddleware":600,
    










    #该中间件的存在使得爬去需要cookies的网站成为可能。它负责追踪web_server 发送的cookies，然后在之后的requests中发送回去
    #同样的，这个中间件也要配合settings里面的设置起作用。相关的两个设置是：
    #【COOKIES_ENABLED】默认为True 如果关闭,cookies将不会被发送给 web server
    #【COOKIES_DEBUG】默认为False 如果为True，那么将会在日志中打印所有的cookies
    #另外文档中有说到，单个spider追踪多个cookies sessions 如果有空请注意看一下
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,







    #-------------加载splash--------------------------------

    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,

    #-------------------------------------------------------



    #该中间件用来提供对request设置代理。但是我觉得她没什么用...因为这个中间件的启用，是去读取的环境变量的代理...也就是说，读取到的代理始终是一个死的..没有意义
    #他读取的环境变量是：
    #【http_proxy】
    #【https_proxy】
    #【no_proxy】
    #也就是说，如果使用这个中间件的话，还需要预先配置好环境变量中的代理...比如说是
    #C:\>set http_proxy=http://proxy:port
    #此外...如果要设置代理的话，可以去request对象中设置proxy元数据来开启代理，也就是说，可以对每个请求分别设置代理proxy   
    #什么是设置元数据 ？？？ 就是在meta里面加上键proxy,比如
    # request = Request(url = "http://example.com")
    # request.meta["proxy"] = "host:port"
    # yield request
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    #该中间件添加了对 chunk transfer encoding 的支持
    # ？？？ 什么是chunk transfer encoding
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
    #该中间件用来保存所有通过的request, response,以及exception
    # ？？？ 保存 ？？？ 保存在哪
    #注意：同样的，是需要配合settings的设置来开启，相关的设置是在
    #【DOWNLOADER_STATS】是否收集下载器的数据 默认为True 
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    #该中间件用来为所有的request 和response 提供底层的缓存支持。其由cache存储后端和cache策略组成
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    "easyspider.middlewares.step_records.Step_records_Middleware":950,
    #"easyspider.middlewares.redirect.RedirectMiddleware":960,
}






# 同样的,spider中间件...第一个中间件是最靠近引擎的，最后一个中间件是最靠近spider的

SPIDER_MIDDLEWARES = {
	# 该中间件过滤出所有失败(错误)的相应，因为spider不需要处理这些request。处理意味着需消耗更多的资源，并且毫无意义...
	# 什么是成功的response,返回值在200-300之间的就是成功的response
	# 比如忽略的状态就是
	# [scrapy] DEBUG: Ignoring response <404 http://www.easygot.cn/this_page_id_not_exist.php>: HTTP status code is not handled or not allowed
	# 根本就不会传到spider去了...直接就不给spider处理
	# 同样的这个可以配合setting使用...两个关键字
	# 【HTTPERROR_ALLOWED_CODES】忽略该列表中所有的非200的response 默认是 []
	# 【HTTPERROR_ALLOW_ALL】 忽略所有的response, 不管其状态值
	# 如果设置了 HTTPERROR_ALLOW_ALL = True的话...也会传给spider进行处理...
	# 比如设置了之后，返回如果是404的话，404的页面也会被处理，被逻辑处理
	#
	#
	# 这个的一个好处，是可以做验证，验证是否爬虫被封，如果验证了爬虫被封，那么就不去继续的检查了
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,


    "easyspider.middlewares.is_spider_ban.Is_Spider_ban":60,

    # 该中间件过滤出所有主机名不在spider的属性【allowed_domain】中的request
    # 注意：如果没有定义 【allowed_domain】，或者这个属性为空...那么就是允许所有的request
    # 还有一点要注意的是...如果request设置了dont_filter ，即使网站不在允许列表里面，offsite中间件也会允许该request
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    # 该中间件用来根据request的response的URL，来设置request的 Refer 字段
    # 同样的，这个也是配合settings 中的设置一起使用的，关键字是
    # 【REFERER_ENABLED】 是否启用referer，默认是True
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    # 过滤出URL比限定长度更长的request。url 的最大长度，也是在settings中设置的
    # 【URLLENGTH_LIMIT】 允许爬去的url的最大长度，默认是 2083
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    # 该中间件用来限制网站的爬取深度。如果超过深度了的request 就被舍弃
    # 同样的，他也是配合settings中的设置来启用的，依赖的三个关键字主要是：
    # 【DEPTH_LIMIT】爬取允许的最大深度，如果为0，就是表示没有限制。默认为0，没有限制
    #【DEPTH_STATS】是否收集爬取状态。默认为True
    #【DEPTH_PRIORITY】 是否根据深度来对request安排优先级. 注意，这个值是整数值，用来根据深度调整request优先级。 如果为0，就是表示不会根据深度进行优先级调整。 默认，默认为0，默认不根据深度进行优先级调整
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}











#=======================其他默认无需配置的选项==============================

#打印日志级别 默认为DEBUG
#LOG_LEVEL = 'DEBUG'


#=======================其他默认无需配置的选项==============================



# DEFAULT_REQUEST_HEADERS = {
# 	"hello":"i'm easyspider"
# }

#禁用cookies
COOKIES_ENABLED = False


#HTTPERROR_ALLOW_ALL = True