from flask import render_template
import flask
import pickle
import pandas as pd
import numpy as np
import json
from jinja2 import Template

app = flask.Flask(__name__, template_folder='templates')

#-------- MODEL GOES HERE -----------#



pipe = pickle.load(open("pipe.pkl", 'rb'))
data=pd.DataFrame({
    "close_to_water" : True,
    'city':'Toronto',
    "weather":'Foggy',
    "temperature":[25.5],
    "day" :'Thursday',
    "morning" : True,
    "afternoon": False,
    "night": False
})
pipe.predict(data)


#-------- ROUTES GO HERE -----------#

@app.route('/')
def index():
    with open("templates/index.html", 'r') as p:
       return p.read()

@app.route('/hist', methods=['POST'])
def trial():
    args= (flask.request.form)
    args = dict(flask.request.form)
    temp=False
    if args.get('smoker')=='Yes':
        temp=True
    setter=[True,False,False]
    if  args.get('timeofday')=='morning':
        setter=[True,False,False]
    elif args.get('timeofday')=='afternoon':
        setter=[False,True,False]
    else:
        setter=[False,False,True]

    data=pd.DataFrame({
        "close_to_water" : temp,
        'city':args.get('city'),
        "weather":args.get('weather'),
        "temperature": [args.get('temp')],
        "day" :args.get('day'),
        "morning" : setter[0],
        "afternoon": setter[1],
        "night": setter[2],
    })
    print(pipe.predict(data)[0])
    return render_template('result.html', trial=pipe.predict(data)[0])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
