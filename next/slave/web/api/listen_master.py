#coding=utf-8

from flask import Flask
from flask import jsonify
import json
import libs.tools as tools


app = Flask(__name__)


interface_name = "wlp3s0"
flask_port=9510

@app.route("/detect_alive")
def response_master_detect():
	flag,my_ip = tools.get_ip(interface_name)
	if not flag[0]:
		print flag[1]
		return jsonify(
				ip=flag[1],
				status=-1
			)

	return jsonify(
			ip=my_ip,
			status=200
		)
	#return "i am alive"



app.run(host="0.0.0.0",port=flask_port,debug=True)