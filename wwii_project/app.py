# import necessary libraries
import numpy as np
import pandas as pd 
import datetime as dt
import random
import os   
import csv

from flask import (
    Flask,
    render_template,
    json,
    jsonify,
    request,
    redirect,
    url_for)

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, and_
from sqlalchemy import MetaData

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///static/wwii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Population = Base.classes.population
Gdp = Base.classes.gdp
Density = Base.classes.density
Life_Expectancy = Base.classes.life_expectancy

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():

    return render_template("index.html")

@app.route('/years')
def years():
    """Return a list of years."""

    years = []
    result = session.query(Population).all()
    for c in Population.__table__.c:
        if c.name != "country" and c.name != "id":
            years.append(c.name)
            
    return jsonify(years)

@app.route("/population/<year>")
def population(year):

    years = []
    result = session.query(Population).all()
    for c in Population.__table__.c:
        if c.name != "country" and c.name != "id":
            years.append(c.name)
    
    column_name = "Population.year_" + year

    sel = [Population.country, column_name]
    results = session.query(*sel).\
    filter(Population.country.in_(["Andorra","Armenia","Austria","Azerbaijan","Belarus","Belgium","Bulgaria","Croatia","Cyprus","Czech Republic",
    "Denmark", "Estonia","Finland","France","Georgia","Germany", "Greece","Hungary","Iceland","Ireland","Italy",
    "Latvia","Liechtenstein","Lithuania","Luxembourg","Malta","Moldova","Monaco","Netherlands","Norway","Poland",
    "Portugal","Romania","Russia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Ukraine","United Kingdom"])).\
    order_by(Population.country).all()


    country = [result[0] for result in results]
    pop_value = [result[1] for result in results]

    pop_data = {
        'name': country,
        'population': pop_value  
    }

    return jsonify(pop_data)
#    """Return a list dictionaries containing `otu_ids` and `sample_values`."""
#     stmt = session.query(Samples).statement
#     df = pd.read_sql_query(stmt, session.bind)

#     # Make sure that the sample was found in the columns, else throw an error
#     if sample not in df.columns:
#         return jsonify("Error! Sample: %s Not Found!" % (sample), 400)

#     # Return any sample values greater than 1
#     try:
#         df = df[df[sample] > 1]
#     except:
#         print('balls')
#     # Sort the results by sample in descending order
#     df = df.sort_values(by=sample, ascending=0)

#     # Format the data to send as json
#     data = [{
#         "otu_ids": df[sample].index.values.tolist(),
#         "sample_values": df[sample].values.tolist()
#     }]
#     return jsonify(data)

@app.route("/gdp/<year>")
def gdp(year):

    # sel = [Gdp.country]
    # results = session.query(*sel).all()
    sel = [Gdp.country, Gdp.year_1941]
    results = session.query(*sel).\
    filter(Gdp.country.in_(["Andorra","Armenia","Austria","Azerbaijan","Belarus","Belgium","Bulgaria","Croatia","Cyprus","Czech Republic",
    "Denmark", "Estonia","Finland","France","Georgia","Germany", "Greece","Hungary","Iceland","Ireland","Italy",
    "Latvia","Liechtenstein","Lithuania","Luxembourg","Malta","Moldova","Monaco","Netherlands","Norway","Poland",
    "Portugal","Romania","Russia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Ukraine","United Kingdom"])).\
    order_by(Gdp.country).all()
    # countries = list(np.ravel(results))

    country = [result[0] for result in results]
    gdp_value = [result[1] for result in results]

    gdp_data = [
        country,
        gdp_value 
    ]

    return jsonify(gdp_data)


@app.route("/life_exp/<year>")
def life_exp(year):

    # sel = [Gdp.country]
    # results = session.query(*sel).all()
    sel = [Life_Expectancy.country, Life_Expectancy.year_1941]
    results = session.query(*sel).\
    filter(Life_Expectancy.country.in_(["Andorra","Armenia","Austria","Azerbaijan","Belarus","Belgium","Bulgaria","Croatia","Cyprus","Czech Republic",
    "Denmark", "Estonia","Finland","France","Georgia","Germany", "Greece","Hungary","Iceland","Ireland","Italy",
    "Latvia","Liechtenstein","Lithuania","Luxembourg","Malta","Moldova","Monaco","Netherlands","Norway","Poland",
    "Portugal","Romania","Russia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Ukraine","United Kingdom"])).\
    order_by(Life_Expectancy.country).all()
    # countries = list(np.ravel(results))

    country = [result[0] for result in results]
    life_exp_value = [result[1] for result in results]

    life_exp_data = [
        country,
        life_exp_value 
    ]

    return jsonify(life_exp_data)
















# @app.route("/metadata/<sample>")
# def metadata(sample):
#     sample = sample

#     result = session.query(Samples).all()
#     names2 = []
#     for c in Samples.__table__.c:
#         if c.name != "otu_id":
#            names2.append(c.name)

#     sel = [Samples_metadata.AGE,
#         Samples_metadata.BBTYPE,
#         Samples_metadata.ETHNICITY,
#         Samples_metadata.GENDER,
#         Samples_metadata.LOCATION,
#         Samples_metadata.SAMPLEID,
#       ]

#     results = session.query(*sel).\
#         order_by(Samples_metadata.SAMPLEID).all()

#     meta_samples = results

#     keys = ["Age", "BBType", "Ethnicity", "Gender", "Location", "SampleID"]
#     data = meta_samples

#     meta_samples_dict = [dict(zip(keys, d)) for d in data]
    
#     final_meta_dict = dict(zip(names2, meta_samples_dict))

#     for k, v in final_meta_dict.items():
#         if k == sample:
            
#             return jsonify(v)

# @app.route("/wfreq/<sample>")
# def wfreq(sample):

#     result = session.query(Samples).all()
#     names3 = []
#     for c in Samples.__table__.c:
#         if c.name != "otu_id":
#            names3.append(c.name)

#     sel = [Samples_metadata.WFREQ]

#     results = session.query(*sel).\
#         order_by(Samples_metadata.SAMPLEID).all()

#     washes = results

#     # keys = ["Wash Frequency"]
#     data = washes

#     # washes_dict = [dict(zip(keys, d)) for d in data]
    
#     final_wash_dict = dict(zip(names3, data))

#     for k, v in final_wash_dict.items():
#         if k == sample:
            
#             return jsonify(v)

# @app.route("/samples/<sample>")
# def samples(sample):

#     result = session.query(Samples).all()
#     names5 = []
#     for c in Samples.__table__.c:
#         if c.name != "otu_id":
#             names5.append(c.name)
    
#     # sel = [Samples.otu_id]

#     # results = session.query(*sel).all()

#     otu_ids = [1166, 2858, 481, 2263, 40, 1188, 351, 188, 2317, 1976]
#     values = [163, 126, 113, 80, 15, 45, 63, 12, 36, 8]

#     # otus = results
#     # otus_dict = dict(zip(names5, otus))

#     # for k, v in otus_dict.items():
#     #     if k == sample:
            
#     return jsonify(otu_ids, values) 

#     # samplesq = engine.execute('SELECT * FROM Samples').fetchall()

#     # samples_zip = list(zip(names5, samplesq)) 

#     # samples_list = list(np.ravel(samples_zip))
#     # for k, v in samples_dict.items():
#     #     if k == sample:
            
#     # return jsonify(otus)

# @app.route("/wfreq2")
# def wfreq2():

#     names5 = []
#     result = session.query(Samples).all()
#     for c in Samples.__table__.c:
#         if c.name != "otu_id":
#             names5.append(c.name)

#     sel = [Samples_metadata.WFREQ]

#     results = session.query(*sel).all()

#     washes = results
    
#     wash_dict = dict(zip(names5, washes))   

#     washes2 = list(np.ravel(washes))

#     for k, v in wash_dict.items():
        
#         return jsonify(washes2)

# @app.route("/samples/<sample>")
# def samples(sample):

# # sample_names = []
# # otus = []
# # values = []

#     f = open("belly_button_biodiversity_samples.csv", 'r')
#     reader = csv.reader(f)
#     headers = reader.__next__()

    # column = {}
    # otus = []
    # headers = []
    # values = []

    # for h in headers:
    #     headers.append(h)

    # for row in reader:
    #     otus.append(row[0])
    #     values.append(row[1:])
    # return jsonify(otus, values, headers)



    # column = {}
    # otus = []
    # for h in headers:
    #     column[h] = []
        
    # for row in reader:
    #     if row[0] != '0':
    #         otus.append(row[0])
    #         for h, v in zip(headers, row):
    #             if (v) != '0':
    #                 column[h].append(v)

    #     # columns = dict(zip(column, otus))

    # for k, v in column.items():
        
    #     zips = dict(zip(v, otus))
        
    #     if k == sample:
            
    #         return jsonify(k, otus, v)
    
    # return jsonify(column)

if __name__ == '__main__':
    app.run(debug=True) 
    