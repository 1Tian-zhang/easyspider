#coding=utf-8

from flask import Flask
app = Flask(__name__)


import redis

@app.route("/show_result")
def show_result():
	pass



def get_result_from_redis():


if __name__ == '__main__':
	#app.run()