# This contains functions to build and commit data to database ready for use as training data
# based on tutorial src = https://pythonprogramming.net/chatbot-deep-learning-python-tensorflow/

import sqlite3
import json
from datetime import datetime as dt
import boma_preproc as pp

timeframe = "2015-05"
sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()


def create_table():
    c.execute(
        """CREATE TABLE IF NOT EXIST parent_reply(
            parent_id TEXT PRIMARY KEY, 
            comment_id TEXT UNIQUE, 
            parent TEXT, 
            comment TEXT, 
            subreddit TEXT, 
            unix INT, 
            score INT)
            """)


def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(
            pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return 0
    except:
        return 0


def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return True


def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []


def sql_insert(row, update=False, parent=False):
    if update:
        try:
            sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id = ?;""".format(
                row['parent_id'],
                row['comment_id'],
                row['parent_data'],
                row['body'],
                row['subreddit'],
                int(row['created_utc']),
                row['score'],
                row['parent_id'])
        except Exception as e:
            print('s-UPDATE insertion error: ', str(e))
    elif parent:
        try:
            sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(
                row['parent_id'],
                row['comment_id'],
                row['parent_data'],
                row['body'],
                row['subreddit'],
                int(row['created_utc']),
                row['score'])
        except Exception as e:
            print('s-PARENT insertion error: ', str(e))
    else:
        try:
            sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(
                row['parent_id'],
                row['comment_id'],
                row['body'],
                row['subreddit'],
                int(row['created_utc']),
                row['score'])
        except Exception as e:
            print('s-NO_PARENT insertion error: ', str(e))
    if sql:
        try:
            transaction_bldr(sql)
        except Exception as e:
            print('transaction failed to build', str(e))


if __name__ == "__main__":
    create_table()
    row_counter = 0
    pairs = 0

    with open("./chatdata/reddit_data/{}/RC_{}".format(timeframe.split('-')[0], timeframe)) as rc:
        for rc_row in rc:
            row_counter += 1
            rc_row = json.loads(rc_row)
            row = {}
            row['parent_id'] = rc_row['parent_id']
            row['body'] = pp.format_data(rc_row['body'])
            row['created_utc'] = rc_row['created_utc']
            row['score'] = rc_row['score']
            row['comment_id'] = rc_row['name']
            row['subreddit'] = rc_row['subreddit']
            row['parent_data'] = pp.find_parent(row['parent_id'])

            if row['score'] >= 2 and acceptable(row['body']):
                if row['score'] > find_existing_score(row['parent_id']):
                    sql_insert(row, update=True)
                else:
                    sql_insert(row, parent=row['parent_data'])

            if row_counter % 100000 == 0:
                print("Total rows read: {}, Paired rows: {}, Time: {}").format(
                    row_counter, pairs, str(dt.now())))
