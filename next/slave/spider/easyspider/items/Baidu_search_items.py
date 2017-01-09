#coding=utf-8

from scrapy.item import Item,Field

from easyspider.items.items import ExampleItem

#class Baidu_search_items(Item):
class Baidu_search_items(ExampleItem):


	search_key_word = Field()
	search_highlight_title = Field()
	search_highlight_content = Field()
	search_engine = Field()
	search_page_index = Field()
	source_page_title = Field()
	source_page_key_word = Field()
	source_page_description = Field()
	source_page_content = Field()
	aaaasource_page_url = Field()



	# insert_map = {}

	# insert_map["search_key_word"] = item.get("key_word","null")
	# insert_map["search_highlight_title"] = item.get("search_highlight_title","null")
	# insert_map["search_highlight_content"] = item.get("search_highlight_content","null")
	# insert_map["search_engine"] = item.get("search_engine","null")
	# insert_map["search_page_index"] = item.get("search_page_index","null")

	# insert_map["source_page_title"] = item.get("source_page_title","null")
	# insert_map["source_page_key_word"] = item.get("source_page_key_word","null")
	# insert_map["source_page_description"] = item.get("source_page_description","null")
	# insert_map["source_page_content"] = item.get("source_page_content","null")
	# insert_map["source_page_url"] = item.get("source_page_url","null")