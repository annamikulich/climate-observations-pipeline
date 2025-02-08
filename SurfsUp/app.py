# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station


# Create our session (link) from Python to the DB
session=Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")

def home_page():
    return(
    "Available Routes:<br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/<start><br/>"
    "/api/v1.0/<start>/<end><br/>"
           )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date= session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d")
    previous_year = recent_date - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()
        
    precipitation_dict = {date: prcp for date, prcp in results if prcp is not None}
    return jsonify(precipitation_dict)
    
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)
    
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station = "USC00519281"
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d")
    previous_year = recent_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= previous_year).all()

    temperatures = [{"date": date, "temperature": tobs} for date, tobs in results]
    return jsonify(temperatures)
    
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    if end:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        ).filter(Measurement.date >= start).all()

    temp_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2],
    }
    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)
