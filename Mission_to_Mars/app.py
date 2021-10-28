from typing import Text
import scrape_mars
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect
import pandas as pd

# Setting up a flask connection
app = Flask(__name__)

# installed PyMongo and using it to establish a connection with Mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


# Setting up the first route to render index.html template
@app.route("/")
def index():
    mars_dict = mongo.db.mars.find_one()
    return render_template("index.html", mars_dict=mars_dict)


# Setting up second route to trigger scrape function
@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars
    mars_data  = scrape_mars.scrape()
    mars_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

# Set to False
if __name__ == "__main__":
    app.run(debug=True)