# import necessary libraries
import datetime as dt
import numpy as np
import pandas as pd
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Database Setup
#################################################

# Create the connection engine
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
Base.classes.keys()
# Save references to the otu, samples, and meta-data tables
otu = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata = Base.classes.samples_metadata

# Create a session
session = Session(engine)


#################################################
# app.route Setup
################################################# 
  
@app.route("/") 
def home():
    """Return the dashboard homepage.""" 
    return render_template("index.html")

@app.route('/names')
def name():
    """List of sample names.

    Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]

    """

    results = session.query(Samples).statement
    df = pd.read_sql_query(results,session.bind)
    df.set_index('otu_id',inplace=True)
    return jsonify(list(df.columns))
    

@app.route('/otu')
def otu_descriptions():
    """List of OTU descriptions.

    Returns a list of OTU descriptions in the following format

    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """
    results = session.query(otu.lowest_taxonomic_unit_found).all()

    # Convert list of tuples into normal list
    descriptions = list(np.ravel(results))

    return jsonify(descriptions)

@app.route('/metadata/<sample>')
def metadata(sample):

    
    """MetaData for a given sample.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }

    
    """

    sample = sample[3:]
    
    sel = [samples_metadata.AGE, samples_metadata.BBTYPE, samples_metadata.ETHNICITY, samples_metadata.GENDER, samples_metadata.LOCATION, samples_metadata.SAMPLEID]
    results = session.query(*sel).filter(samples_metadata.SAMPLEID == sample).all()

    data = {}
    for result in results:
        data["AGE" ] = result[0]
        data["BBTYPE" ] = result[1]
        data["ETHNICITY"] = result[2]
        data["GENDER"] = result[3]
        data["LOCATION"] = result[4]
        data["SAMPLEID"] = result[5]

    return jsonify(data)


@app.route('/wfreq/<sample>')
def wfreq(sample):
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns an integer value for the weekly washing frequency `WFREQ`
    """
    sample = sample[3:]
 
    results = session.query(samples_metadata.WFREQ).filter(samples_metadata.SAMPLEID == sample).all()
    
    return jsonify(results)

@app.route('/samples/<sample>')
def samples(sample):
    """OTU IDs and Sample Values for a given sample.

    Sort your Pandas DataFrame (OTU ID and Sample Value)
    in Descending Order by Sample Value

    Return a list of dictionaries containing sorted lists  for `otu_ids`
    and `sample_values`

    [
        {
            otu_ids: [
                1166,
                2858,
                481,
                ...
            ],
            sample_values: [
                163,
                126,
                113,
                ...
            ]
        }
    ]

    """
 
    results = session.query(Samples).statement
    df = pd.read_sql_query(results,session.bind) 

    df=df[df[sample]>1]
    
    sample_data = [{
            "otu_ids": df[sample].index.values.tolist(),
            "sample_values": df[sample].values.tolist()
        }]
    return jsonify(sample_data)


if __name__ == '__main__':
    app.run(debug=True)