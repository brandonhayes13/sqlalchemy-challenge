# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)
# reflect the tables
Base.classes.keys()

# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify

app = Flask(__name__)
one_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return '''
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/<start><br>
    /api/v1.0/<start>/<end>
    '''

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Query to get the last 12 months of precipitation data
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year).all()
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281', 
                                                      measurement.date >= one_year).all()
    tobs_list = [temp[0] for temp in results]
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    return jsonify(results[0])

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    return jsonify(results[0])