#coding=utf-8
from datetime import datetime
import os
import time as o_time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
def tick():
    print('Tick! The time is: %s' % datetime.now())
 
 
if __name__ == '__main__':
    #scheduler = BlockingScheduler()
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
 
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

	
    while True:
    	print "hello"
    	
    	o_time.sleep(1)