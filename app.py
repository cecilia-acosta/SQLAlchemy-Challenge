import numpy as np

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
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/2016-08-24<br/>"
        f"/api/v1.0/start-end/2016-08-242017-08-23<br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into a list
    stations = []
    for name in results:
        stations_dict = {}
        stations_dict["station"] = name
        stations.append(stations_dict)

    return jsonify(stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    precipitations = []
    for date, prcp in results:
        precipitations_dict = {}
        precipitations_dict["date"] = date
        precipitations_dict["prcp"] = prcp
        precipitations.append(precipitations_dict)

    return jsonify(precipitations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    tobs1 = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs1.append(tobs_dict)

    return jsonify(tobs1)

@app.route("/api/v1.0/start/<start>")
def start_date(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    # results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    #     filter(Measurement.date >= start).\
    # order_by(Measurement.date).all()

    max_temp = session.query(Measurement.date, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            order_by(Measurement.date).all()

    min_temp = session.query(Measurement.date, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            order_by(Measurement.date).all()

    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            order_by(Measurement.date).all()

    session.close()
    
    return jsonify(max_temp, min_temp, avg_temp)

@app.route("/api/v1.0/start-end/<start><end>")
def range(start,end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    # results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    #     filter(Measurement.date >= start).\
    #     filter(Measurement.date <= end).\
    # order_by(Measurement.date).all()

    max_temp = session.query(Measurement.date, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
            order_by(Measurement.date).all()

    min_temp = session.query(Measurement.date, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
            order_by(Measurement.date).all()

    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
            order_by(Measurement.date).all()

    session.close()
    
    return jsonify(max_temp, min_temp, avg_temp)

if __name__ == '__main__':
    app.run(debug=True)
