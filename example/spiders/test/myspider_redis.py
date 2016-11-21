from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'myspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)
        #with open("aa.txt","w") as f:
        #    f.write("".join(args))  
        #    f.write("\n"+str(kwargs)) 
        print args
        print kwargs

    def parse(self, response):
        print "zzzzzzzzzzzzzzzzzzz"
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
