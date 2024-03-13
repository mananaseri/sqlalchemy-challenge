# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine,reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Homepage"""
    return (
        f"Welcome to the Hawaii Weather Data!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

# Create a session from Python to the DB
    session = Session(engine)

# Starting from the most recent data point
    recent_date = dt.date(2017, 8, 23)

# Calculate the date one year from the last date in data set.
    one_year_ago = recent_date - dt.timedelta(days=365)

 # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
    filter(Measurement.date <= recent_date).all()

    session.close()

# convert the list to Dictionary 
    
    all_prcp_list = []
    for date, prcp in precipitation_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp_list.append(prcp_dict)

    return jsonify(all_prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
   
# Query all stations
    Total_stations = session.query(Station.station).\
                 order_by(Station.station).all()
    session.close()
# JSON list
    all_stations = list(np.ravel(Total_stations))
    return jsonify(all_stations)  

@app.route("/api/v1.0/tobs")
def tobs():
    # creat a session 
    session = Session(engine)

    """Return a list of all TOBs"""

    # Query for all tobs 
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
                        group_by(Measurement.station).\
                        order_by(func.count(Measurement.station).desc()).all()
    
    # showing the most active station
    the_most_active_station= most_active_stations[0][0]

    # Starting from the most recent data point
    recent_date = dt.date(2017, 8, 23)

    # Calculate the date one year from the last date in data set.
    one_year_ago = recent_date - dt.timedelta(days=365)
    
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram

    temperature_data = session.query(Measurement.tobs).\
    filter(Measurement.station == the_most_active_station).\
    filter(Measurement.date >= one_year_ago).\
    filter(Measurement.date <= recent_date).all()

    session.close()

    # JSON list of temperatures

    temp_list = list(np.ravel(temperature_data))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start_date(start):

# Create our session from Python to the db
    session = Session(engine)

"""Return a list of min, avg and max temperature for a start date """

# Query all tobs

tobs_start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
session.close()

#Create a dictionary for start_date_tobs

start_tobs = []
for min, avg, max in tobs_start_date
    start_tobs_dict = {}
    start_tobs_dict["min_temp"] = min
    start_tobs_dict["avg_temp"] = avg
    start_tobs_dict["max_temp"] = max
    start_tobs.append(start_tobs_dict)   
    return jsonify(start_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):

# Create our session
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""

# Query
    start_end_tobs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionory 

    all_tobs = []
    for min, avg, max in start_end_tobs:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        all_tobs.append(start_end_tobs_dict) 
    

    return jsonify(all_tobs)

if __name__ == "__main__":
    app.run(debug=True)
