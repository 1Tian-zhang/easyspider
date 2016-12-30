#coding=utf-8

from scrapy.exceptions import IgnoreRequest

from scrapy.spidermiddlewares.httperror import logger

#这个 IgnoreRequest是继续自 Exception，所以能够做raise用，抛出异常
class Ban_Error(IgnoreRequest):
	def __init__(self,response,*args,**kwargs):
		self.response = response
		super(Ban_Error,self).__init__(*args,**kwargs)



class Is_Spider_ban(object):

    def process_spider_input(self, response, spider):
        check = "请输入验证码"
    	if check in response.body:
        	raise Ban_Error(response, 'Ignoring non-200 response')
        print "验证通过~"
        return 

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, Ban_Error):
            logger.debug(
                "Ignoring response %(response)r: Spider is ban...",
                {'response': response}, extra={'spider': spider},
            )
            return []