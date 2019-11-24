import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt 

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    first_date=session.query(Measurement.date).order_by(Measurement.date).first()
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date 1 year ago from the last data point in the database

    end_date=dt.datetime.strptime(last_date, "%Y-%m-%d")
    start_date = end_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores

    print(end_date)
    print(start_date)

    one_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()

    session.close()

    return jsonify(one_year)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    active_stations = session.query(Measurement.station,
                                func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()
    return jsonify(active_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    first_date=session.query(Measurement.date).order_by(Measurement.date).first()
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date 1 year ago from the last data point in the database

    end_date=dt.datetime.strptime(last_date, "%Y-%m-%d")
    start_date = end_date - dt.timedelta(days=365)

    station_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).all()
    session.close()
    return jsonify(station_temp)

@app.route("/api/v1.0/<start>")
def start(start):
    temp = session.query(func.min(Measurement.tobs), 
                             func.max(Measurement.tobs), 
                             func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    temp = session.query(func.min(Measurement.tobs), 
                             func.max(Measurement.tobs), 
                             func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date<= end).all()
    session.close()
    return jsonify(temp)


if __name__ == '__main__':
    app.run(debug=True)