#!/usr/bin/env python
import glob
import os
import subprocess
import sys
from time import sleep

import aiml
import tensorflow as tf

from flask import Flask, request, abort
from flask_cors import cross_origin

from chatbot.botpredictor import BotPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

k = aiml.Kernel()
for f in glob.glob(DIR_PATH + '/data/xml/*.xml'):
    k.learn(f)
   
with tf.compat.v1.Session() as sess:
    predictor = BotPredictor(
        sess, 
        corpus_dir=os.path.join(PROJECT_ROOT, 'data', 'corpus'), 
        knbase_dir=os.path.join(PROJECT_ROOT, 'data', 'knowledge_base'),
        result_dir=os.path.join(PROJECT_ROOT, 'data', 'result'), 
        result_file='basic'
    )   

@app.route('/ping', methods=['GET'])
@cross_origin(origins='*')
def ping():
    return 'pong'
   
@app.route('/chat', methods=['POST'])
@cross_origin(origins=['https://gail-the-bomachat.netlify.app', 'localhost'])
def chat():
    session_id = predictor.session_data.add_session()
    resp = request.get_json()
    question = str(resp.get('body'))

    if not question:
        abort(404, description='¯\_(ツ)_/¯') 
        return

    aiml_reply = k.respond(question)

    if len(aiml_reply):
        sleep(1.5)
        print('question:', question, 'aiml-reply:', aiml_reply, sep=' ')
        return aiml_reply

    else:
        nmt_reply = predictor.predict(session_id, q)
        print('question:', question, ' nmt-reply:', nmt_reply, sep=' ')
        return nmt_reply
