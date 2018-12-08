import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def homepage():
    """List of all returnable API routes."""
    return(
        f"Available Routes:<br/>"
        f"(Note: Most recent available date is 2017-08-23 while the latest is 2010-01-01).<br/>"

        f"/api/v1.0/precipitation<br/>"
        f"- Query dates and temperature from the last year. <br/>"

        f"/api/v1.0/stations<br/>"
        f"- Returns a json list of stations. <br/>"

        f"/api/v1.0/temperature<br/>"
        f"- Returns list of Temperature for previous year. <br/>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"- Returns a Max, Average, and Min temperature for given date.<br/>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"- Returns a Max, Average, and Min temperature for given period.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()
    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    return jsonify(results)


@app.route("/api/v1.0/temperature")
def temperature():
    results = session.query(Measurement.date, Measurement.tobs).all()
    return jsonify(results)


@app.route('/api/v1.0/<date>')
def given_date(date):
    results = session.query(func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date == "2017-08-23").all()
    data_list = []
    for result in results:
        row = {}
        row['Date'] = result[0]
        row['Highest Temperature'] = float(result[1])
        row['Average Temperature'] = float(result[2])
        row['Lowest Temperature'] = float(result[3])
        data_list.append(row)
    return jsonify(data_list)


@app.route('/api/v1.0/<start_date>/<end_date>')
def query_dates(start_date, end_date):
    results = session.query(func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Highest Temperature"] = float(result[1])
        row["Lowest Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)