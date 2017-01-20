from datetime import datetime
from datetime import timedelta
import time
import config


def get_time():
    return time.strftime(config.datetime_format)


def get_time_x_seconds_ago(seconds):
    return (datetime.now() - timedelta(seconds=seconds)).strftime(config.datetime_format)


def seconds_between(d1, d2):
    d1 = datetime.strptime(d1, config.datetime_format)
    d2 = datetime.strptime(d2, config.datetime_format)
    return abs((d2 - d1).seconds)
