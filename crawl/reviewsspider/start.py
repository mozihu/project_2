#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 21:28:22 2020

@author: zq
"""

from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler


def tick():
    os.system("scrapy crawl tripadvisor")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'cron', hour=23, minute=50)
    print(
        'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
