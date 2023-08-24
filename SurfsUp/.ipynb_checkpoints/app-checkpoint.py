# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/start<br/>"
         f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    one_ago = dt.date(2017,8,23)-dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=one_ago).all()

    session.close()
    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in prcp_data}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    

#Return a JSON list of stations from the dataset.
    station_data = session.query(Station.station).all()
    session.close()
    stations=list(np.ravel(station_data))
    return jsonify(stations=stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
     
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    
#query the database

    result = session.query(Measurement.tobs).\
    filter(Measurement.station== 'USC00519281').\
    filter(Measurement.date>=prev_year).all()
    
    session.close()
    
    temps = list(np.ravel(result))
    
    return jsonify(temps=temps)
    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def end(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    selection = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)
    if not end:
                              
    pass 
                              
if __name__ == '__main__':
    app.run(debug=True)