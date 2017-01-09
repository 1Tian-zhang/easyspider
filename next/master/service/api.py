#coding=utf-8

from flask import Flask
from background_work.base_redis import BaseRedis
from flask import jsonify
from detect_online_slave import Check_online_slave

"""
先启动slave机器的：
python /home/zhanghang/桌面/workspace/easyspider/next/slave/web-accesser/api/listen_master.py &

然后启动主机器;

python /home/zhanghang/桌面/workspace/easyspider/next/master/web_controller/www/api/api.py 

"""

app = Flask(__name__)


slaves = Check_online_slave(slave_list_file="../../conf/slave_list.json")




@app.route("/")
def index():
	online_slave = slaves.get_online_slave()
	return online_slave


app.run(host="0.0.0.0",debug=True)