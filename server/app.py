#!/usr/bin/env python
import glob
import os
import subprocess
import sys
from time import sleep

import aiml
import tensorflow as tf
from flask import Flask, render_template, request
from flask_cors import CORS

from chatbot.botpredictor import BotPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

bot = Flask(__name__)
CORS(bot)

k = aiml.Kernel()
for f in glob.glob(DIR_PATH + "/xml/*.xml"):
   k.learn(f)

@bot.route("/chat", methods=['GET', 'POST'])
def chat():
    session_id = predictor.session_data.add_session()
    q = str(request.get_json()['body'])
    reply = k.respond(q)
    print(reply)
    if len(reply):
        print('rule')
        sleep(1.5)
        return reply
    else:
        print('nmt')
        reply = predictor.predict(session_id, q)
        print(reply)
        return reply



if __name__ == ("__main__"):
    corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
    knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
    res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')

    with tf.Session() as sess:
        predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir,
                                 result_dir=res_dir, result_file='basic')
        bot.run(port=8070)
