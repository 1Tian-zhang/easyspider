#easyspider

##简介
-------------------------
easyspider 是由python编写的,继承scrapy和scrapy-redis, 致力于打造一个**通用**的,**可配置规则**,支持**分布式**的一个爬虫系统。
目的是把爬虫开发的代价降低,只需要配置逻辑规则,其他的请求处理全部由easyspider自动完成。同时提供很高的扩展性。

##结构说明
-------------------------

在不编写扩展的情况下,用户需要更改的只有 task.json 文件,这个文件储存了爬虫的规则,定义爬虫的入口地址,如何跟进,如何截取信息。

##task.json 说明

task.json 可以是一个任务,也可以是多个任务的集合,但是任何都被包含在整体任务的task的列表中。

        {
          "task":[
              ...
          ]
        }

每一个单独的task是一个任务,它是字典类型,一个完整的task应该包含如下关键字
<table>
<thead>
<tr>
<td>关键字名</td>
<td>含义</td>
<tr>
</thead>
<tbody>
<tr>
<td>task_name</td>
<td>任务名,必有，用来确定任务启动信息</td>
</tr>

</tbody>
</table>

##task.json 样例

下面是一个抓取西域工业全站数据的规则task.json 文件样例

      {
          "task":[
              {
                  "task_name":"ehsy",
                  "root_info":{
                      "root_url_type":"list",
                      "root_urls":[
                          "http://www.ehsy.com/"
                      ]
                  },
                  "route_url":[
                      "http://www.ehsy.com",
                      "http://www.ehsy.com/office-supplies",
                      "http://www.ehsy.com/category-16580",
                      "http://www.ehsy.com/product-RAM622"
                  ],
                  "page_step":[
                      {
                          "step_index":1,
                          "next_step_url_rule_type":"xpath",
                          "next_step_url_rule":"//div[@class="partners1"]/ul/li/a/@href",
                          "prefix":"http://www.ehsy.com",
                          "example_extract_url":"http://www.ehsy.com/office-supplies",
                          "example_now_url":"http://www.ehsy.com/",
                          "extract_index":1
                      },
                      {
                          "step_index":2,
                          "next_step_url_rule_type":"xpath",
                          "next_step_url_rule":"//div[@class="nodeImg"]/a/@href",
                          "prefix":"http://www.ehsy.com",
                          "example_extract_url":"http://www.ehsy.com/category-16580",
                          "example_now_url":"http://www.ehsy.com/office-supplies",
                          "extract_index":1
                      },
                      {
                          "step_index":3,
                          "next_step_url_rule_type":"xpath",
                          "next_step_url_rule":"//div[@class="product"]/@data-text",
                          "example_extract_url":"http://www.ehsy.com/product-RAM622",
                          "example_now_url":"http://www.ehsy.com/category-16580",
                          "prefix":"http://www.ehsy.com/product-",
                          "page_divid":{
                              "page_divid_rule_type":"xpath",
                              "page_divid_rule":"//div[@class="pagintion"]/li[@class="pg-next"]/a/@href",
                              "example_extract_url":"http://www.ehsy.com/category-16580?p=2"
                          },
                          "last_step":true,
                          "extract_index":1,
                          "comment":"全部都遍历一遍，花的时间太长了"
                      }
                  ],
                  "extract_info":[
                      {
                          "extract_step":1,
                          "detail":[
                              {
                                  "key":"first_category",
                                  "match_type":"xpath",
                                  "val":[
                                      {
                                          "pattern":"//span[@class="category-name1"]/text()",
                                          "extract_index":0
                                      }
                                  ],
                                  "example_extract_val":"工具",
                                  "example_extract_url":"http://www.ehsy.com/"
                              }
                          ]
                      },
                      {
                          "extract_step":2,
                          "detail":[
                              {
                                  "key":"second_category",
                                  "match_type":"xpath",
                                  "val":[
                                      {
                                          "pattern":"//div[@class="nodeImg"]/a/img/@title",
                                          "extract_index":0,
                                          "replace":""
                                      }
                                  ],
                                  "example_extract_val":"办公用品",
                                  "example_extract_url":"http://www.ehsy.com/office-supplies",
                                  "comment":"这一段感觉无解。无法提取进入的二级分类...通用爬虫模块做不到...因为二级分类数目和三级分类数目不匹配...而单独提取二级分类，又会损失三级分类。除非我先定位到三级分类，然后再退回二级分类，从而保证数目大小一致 所以还是先忽视这个处理吧...再添加一个关键词ignore 把这个当作后续需要处理的任务",
                                  "ignore":true
                              },
                              {
                                  "key":"third_category",
                                  "match_type":"xpath",
                                  "val":[
                                      {
                                          "pattern":"//div[@class="nodeImg"]/a/img/@title",
                                          "extract_index":0
                                      }
                                  ],
                                  "example_extract_val":"笔类",
                                  "example_extract_url":"http://www.ehsy.com/office-supplies"
                              }
                          ]
                      },
                      {
                          "extract_step":3,
                          "detail":[
                              {
                                  "key":"",
                                  "ignore":true
                              }
                          ]
                      },
                      {
                          "extract_step":4,
                          "detail":[
                              {
                                  "key":"prod_name",
                                  "match_type":"xpath",
                                  "val":[
                                      {
                                          "pattern":"//h1/text()",
                                          "extract_index":"all"
                                      }
                                  ]
                              },
                              {
                                  "key":"prod_price",
                                  "match_type":"xpath",
                                  "val":[
                                      {
                                          "pattern":"//div[@class="price clearfix"]/span[2]/text()",
                                          "extract_index":"all"
                                      }
                                  ]
                              },
                              {
                                  "key":"imgs",
                                  "match_type":"xpath",
                                  "val":[
                                      {
                                          "pattern":"//ul[@class="previewImage"]/li/img/@src",
                                          "extract_index":"all",
                                          "comment":"xpath 可以把所有li的图片同时获取到，放心不会遗失"
                                      }
                                  ]
                              }
                          ]
                      }
                  ]
              }
          ]
      }
