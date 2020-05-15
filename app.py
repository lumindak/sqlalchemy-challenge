# 1. import Flask
from flask import Flask, jsonify

#import python database toolkit
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import numpy as np

###################

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)

#
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return(
	 f"Welcome to my 'Weather' API!<br/>"
	 "<br/>"
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
	 f"/api/v1.0/stations<br/>"
	 f"/api/v1.0/tobs<br/>"
	 f"/api/v1.0/yyyy-mm-dd<br/>"
	 f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
	session = Session(engine)
	results = session.query(Measurement.date,Measurement.prcp).all()
	session.close()
	data = list(np.ravel(results))
	data_dict=[]
        #data_dict ={data[x]:data[x+1] for x in range(0,len(data),2)}
	for x in range(0,len(data),2):
		temp = {data[x]:data[x+1]}
		data_dict.append(temp)
	return jsonify(data_dict)
	
@app.route("/api/v1.0/stations")
def stations():
	session = Session(engine)
	results1 = session.query(Station.station,Station.name).all()
	session.close()
	data1 = list(np.ravel(results1))
	data1_dict=[]
	for x in range(0,len(data1),2):
		temp={data1[x]:data1[x+1]}
		data1_dict.append(temp)
	return jsonify(data1_dict)

@app.route("/api/v1.0/tobs")
def tobs():
	session = Session(engine)
	results2 = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > '2016-08-23').\
filter(Station.station=="USC00519281").all()
	session.close()
	data2=list(np.ravel(results2))
	data2_dict=[]
	for x in range(0,len(data2),2):
		temp={data2[x]:data2[x+1]}
		data2_dict.append(temp)
	return jsonify(data2_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
	session = Session(engine)
	result3 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
filter(Measurement.date >= start).all()
	session.close()
	data3=list(np.ravel(result3))
	data3_dict={'TMIN':result3[0][0],'TAVG':result3[0][1],'TMAX':result3[0][2]}
	return jsonify(data3_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
        session = Session(engine)
        result4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        session.close()
        data4=list(np.ravel(result4))
        data4_dict={'TMIN':result4[0][0],'TAVG':result4[0][1],'TMAX':result4[0][2]}
        return jsonify(data4_dict)


if __name__ == "__main__":
    app.run(debug=True)
