# This is for building rules that define how the training data is cleaned up and preprocessed
# based on tutorial src = https://pythonprogramming.net/chatbot-deep-learning-python-tensorflow/

import sqlite3
import json
from datetime import datetime as dt

timeframe = "2015-05"

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()


def format_data(data):
    d = data.replace("\n", " newlinechar ").replace(
        "\r", " newlinechar ").replace('"', "'")
    return d


def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(
            pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except:
        return False
