import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Datbase Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return last 12 months of precipitation data"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago_dt = dt.datetime.strptime(most_recent, '%Y-%m-%d') - dt.timedelta(days=365)
    year_ago = year_ago_dt.strftime('%Y-%m-%d')

    # Query the last year of precipitation
    prev_year = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= year_ago).\
      order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    prev_year_dict = {}
    for date, prcp in prev_year:
        prev_year_dict[date] = prcp

    return jsonify(prev_year_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return list of active stations """
    # Create our session (link) from Python to the DB
    session = Session(engine)

    active_stations = session.query(Measurement.station).\
        group_by(Measurement.station).\
        all()

    # Convert list of tuples into normal list
    active_stations_list = list(np.ravel(active_stations))

    return jsonify(active_stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return last 12 months of temperature data for the most active station"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        all()

    # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
    most_active_station = active_stations[0][0]

    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago_dt = dt.datetime.strptime(most_recent, '%Y-%m-%d') - dt.timedelta(days=365)
    year_ago = year_ago_dt.strftime('%Y-%m-%d')

    # Query the last year of temperatures for the most active station
    prev_year = session.query(Measurement.date, Measurement.tobs).\
      filter(Measurement.station == most_active_station).\
      filter(Measurement.date >= year_ago).\
      order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    prev_year_dict = {}
    for date, tobs in prev_year:
        prev_year_dict[date] = tobs

    return jsonify(prev_year_dict)

@app.route("/api/v1.0/<start>")
def start_period(start):
    '''When given the start only, calculate TMIN, TAVG, and TMAX for all dates
        greater than and equal to the start date.'''

    return calc_period(start)

@app.route("/api/v1.0/<start>/<end>")
def full_period(start, end):
    '''When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates
        between the start and end date inclusive.'''
    return calc_period(start, end)

def calc_period(start, end=None):
    '''Return a JSON list of the minimum temperature, the average temperature,
        and the max temperature for a given start or start-end range'''

    # Create our session (link) from Python to the DB
    session = Session(engine)

    if (end == None):
        end = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        all()

    # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
    most_active_station = active_stations[0][0]

    # Query the period of temperature measurements
    temp_metrics = session.query(
                                  func.min(Measurement.tobs),
                                  func.avg(Measurement.tobs),
                                  func.max(Measurement.tobs)).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date <= end).\
        filter(Measurement.date >= start).\
        order_by(Measurement.date).all()

    temp_metrics_list = list(np.ravel(temp_metrics))

    session.close()

    return jsonify(temp_metrics_list)

@app.route("/")
def welcome():
    return (
        f"<html>"
        f"<head>"
        f"<title>Climate API</title>"
        f"</head>"
        f"<body>"
        f"<h1>Welcome to the Climate API!</h1>"
        f"<h2>Available Routes:</h2>"
        f"<ul>"
        f"<li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a></li>"
        f"<li><a href='/api/v1.0/stations'>/api/v1.0/stations</a></li>"
        f"<li><a href='/api/v1.0/tobs'>/api/v1.0/tobs</a></li>"
        f"<li>/api/v1.0/&#60;start&#62;"
        f"<ul><li>e.g. <a href='/api/v1.0/2015-08-20'>/api/v1.0/2015-08-20</a></li></ul></li>"
        f"<li>/api/v1.0/&#60;start&#62;/&#60;end&#62;</li>"
        f"<ul><li>e.g. <a href='/api/v1.0/2015-08-20/2017-08-18'>/api/v1.0/2015-08-20/2017-08-18</a></li></ul></li>"
        f"<li>Note: &#60;start&#62; and &#60;end&#62; refer to dates starting/ending from 2010-01-01 to 2017-08-18</li>"
        f"<li>Dates should be formatted as YYYY-MM-DD format</li>"
        f"</ul>"
        f"</body>"
        f"</html>"
    )


if __name__ == "__main__":
    app.run(debug=True)
