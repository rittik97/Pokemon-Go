from flask import render_template
import flask
import pickle
import pandas as pd
import numpy as np
import json
from jinja2 import Template
import catboost as cb
from catboost import Pool
from sklearn_pandas import DataFrameMapper, CategoricalImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder, MultiLabelBinarizer, LabelBinarizer
import calcs as c



app = flask.Flask(__name__, template_folder='templates')


pipe = pickle.load(open("pipe_catboost.pkl", 'rb'))
data=pd.DataFrame({
    "close_to_water" : False,
    'city':'Toronto',
    "weather":'clear',
    "temperature":[2.5],
    "day" :'Friday',
    "morning" : False,
    "afternoon": True,
    "night": False,
    "type": 'Fire',
    "types":'city_hall'
})
pipe.predict(data)
pipe[1].classes_[47]
np.argmax(pipe.predict_proba(data))

############  Routes ###############

@app.route('/')
def index():
    with open("templates/home.html", 'r') as p:
       return p.read()

@app.route('/predictions', methods=['POST'])
def preds():
    args= (flask.request.form)
    args = dict(flask.request.form)
    d = c.calc_attributes(args.get('pokemon'), args.get('city'))
    scrape=pd.read_csv('data/poke_stats.csv')
    #print(d)

    loc1=d['loc'][0]
    loc2=d['loc'][1]
    weather1=d['weather'][0]
    weather2=d['weather'][1]
    time1=d['time'][0]
    time2=d['time'][1]
    day1=d['day'][0]
    day2=d['day'][1]

    return render_template('predictions.html', url=scrape[scrape['name ']==args.get('pokemon')]['url'].values[0], loc1=loc1, loc2=loc2,
        weather1=weather1, weather2=weather2, time1=time1, time2=time2, day1=day1, day2=day2,
        type=scrape[scrape['name ']==args.get('pokemon')]['types_one'].values[0],
        attack=scrape[scrape['name ']==args.get('pokemon')]['attack'].values[0]
        defense=scrape[scrape['name ']==args.get('pokemon')]['defense'].values[0]
        hp=scrape[scrape['name ']==args.get('pokemon')]['hp'].values[0]
    )


@app.route('/temp')
def tr():
    scrape=pd.read_csv('data/poke_stats.csv')
    np.unique(pd.read_csv('data/final.csv')['time'])
    loc1=loc2="Old Toronto"
    return render_template('predictions.html', url=scrape[scrape['name ']=='Growlithe']['url'].values[0], loc1=loc1, loc2=loc2)



@app.route('/dropdown', methods=['POST'])
def dropdown():
    args= (flask.request.form)
    args = dict(flask.request.form)
    drop_list=pd.read_csv('data/dropdowns.csv')
    ret=drop_list[args.get('data')].dropna()
    #ret=drop_list['Toronto'].dropna()
    #ret_str=""
    #for i in ret:
    #    ret_str+=ret_str+'<option value="'+str(i)+'" >'+"\n"

    #print(ret_str)
    return json.dumps(list(ret))


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
