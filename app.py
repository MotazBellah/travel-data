import crochet
crochet.setup()

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

import os
import sys
from flask import Flask , render_template, jsonify, request, redirect, url_for, session, escape

sys.path.insert(0, './hotels/travelData/spiders')

# print(sys.path)
from booking import BookingSpider

app = Flask(__name__)

app.secret_key = "Super_secret_key"


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
