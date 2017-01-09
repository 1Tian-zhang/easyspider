#coding=utf-8
from scrapy.utils.project import inside_project, get_project_settings


settings = get_project_settings()
#print settings.getdict()
print dir(settings)