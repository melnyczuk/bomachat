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

app = Flask(__name__)
CORS(app)

k = aiml.Kernel()
for f in glob.glob(DIR_PATH + '/xml/*.xml'):
    k.learn(f)
   
with tf.Session() as sess:
    predictor = BotPredictor(
        sess, 
        corpus_dir=os.path.join(PROJECT_ROOT, 'Data', 'Corpus'), 
        knbase_dir=os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase'),
        result_dir=os.path.join(PROJECT_ROOT, 'Data', 'Result'), 
        result_file='basic'
    )   

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'
   
@app.route('/chat', methods=['POST'])
def chat():
    session_id = predictor.session_data.add_session()
    question = str(request.get_json()['body'])

    aiml_reply = k.respond(question)

    if len(aiml_reply):
        sleep(1.5)
        print('question:', question, 'aiml-reply:', aiml_reply, sep=' ')
        return aiml_reply

    else:
        nmt_reply = predictor.predict(session_id, q)
        print('question:', question, ' nmt-reply:', nmt_reply, sep=' ')
        return nmt_reply


if __name__ == ('__main__'):
    host = str(os.environ.get('HOST', '0.0.0.0'))
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)
