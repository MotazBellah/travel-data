import crochet
crochet.setup()

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

import os
import sys
from flask import Flask , render_template, jsonify, request, redirect, url_for, session, escape
import flask_excel as excel
import time
import datetime

sys.path.insert(0, './hotels/travelData/spiders')

from booking import BookingSpider

app = Flask(__name__)

app.secret_key = "Super_secret_key"

excel.init_excel(app)

crawl_runner = CrawlerRunner()
output_data = []
desCity = ''
checkinDate = ''
checkoutDate = ''
room = 1
traveler = 1

@app.route('/')
def index():
    return render_template("index.html")

# After clicking the Submit Button FLASK will come into this
@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Getting the user input, city, checkin,...
        city = request.form['city']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        noOfRoom = request.form['room']
        noOfTraverlers = request.form['traveler']

        global desCity
        global checkinDate
        global checkoutDate
        global room
        global traveler
        # Assign the user input to the global variable, to be used in scray function
        desCity = city
        checkinDate = checkin
        checkoutDate = checkout
        room = noOfRoom
        traveler = noOfTraverlers

        d1 = datetime.datetime.strptime(checkin, "%Y-%m-%d").date()
        d2 = datetime.datetime.strptime(checkout, "%Y-%m-%d").date()
        # Validate the checkin and checkout date
        if ((d1 > d2)):
            return jsonify({"error": "Please check the date"})

        if city and checkin and checkout:
            return jsonify({"cool": "Please fill all the fields"})
        else:
            return jsonify({"error": "Please fill all the fields"})


@app.route("/scrape")
def scrape():
    # Get the output_data and reset it
    global output_data
    output_data = []

    try:
        # Passing the user input to our Scraping Function
        scrape_with_crochet(desCity=desCity, checkinDate=checkinDate, checkoutDate=checkoutDate, room=room, traveler=traveler)
    except Exception as e:
        pass
    # Downlpad excel file with scrapped data
    return excel.make_response_from_records(output_data, "xls", file_name="hotelsdata")


@crochet.wait_for(timeout=800)
def scrape_with_crochet(desCity, checkinDate, checkoutDate, room, traveler):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    try:
        # This will connect to the BookingSpider function in our scrapy file and after each yield will pass to the crawler_result function.
        eventual = crawl_runner.crawl(BookingSpider, city=desCity, checkin=checkinDate, checkout=checkoutDate, room=room, traveler=traveler)
        return eventual
    except Exception as e:
        print(e)


#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
