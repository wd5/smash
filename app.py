# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
from flask import Flask, render_template, redirect, request

from smash import *

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('layout.html', result=None)

@app.route('/sha1/')
@app.route('/sha1/<name>')
def hello(name=None):
    result = RedisStore.get(r, "%s" % name)
    return render_template('layout.html', result=result)

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)