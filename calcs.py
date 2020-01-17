import pandas as pd
import numpy as np
import json
from jinja2 import Template
import catboost as cb
from catboost import Pool
from sklearn_pandas import DataFrameMapper, CategoricalImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder, MultiLabelBinarizer, LabelBinarizer


def temperature_changer(x):
  if x<=17.5:
    return 'Cool'
  elif  (x>17.5) and (x<25):
    return 'Mild'
  else:
      return 'Hot'

def calc_attributes(name,city):
  data=pd.read_csv('data/final.csv')
  #ids=[142]
  pokemon=data[data['city']==city]
  pokemon['temp_new']=pokemon['temperature'].apply(temperature_changer)
  weather_classes=['Foggy', 'Clear', 'PartlyCloudy', 'MostlyCloudy', 'Overcast',
       'Rain', 'BreezyandOvercast', 'LightRain', 'Drizzle',
       'BreezyandPartlyCloudy', 'HeavyRain', 'BreezyandMostlyCloudy',
       'Breezy', 'Windy', 'WindyandFoggy', 'Humid', 'Dry',
       'WindyandPartlyCloudy', 'DangerouslyWindy', 'DryandMostlyCloudy',
       'DryandPartlyCloudy', 'DrizzleandBreezy', 'LightRainandBreezy',
       'HumidandPartlyCloudy', 'HumidandOvercast', 'RainandWindy']
  day_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  time_of_day=["Morning", "Afternoon", "Evening", "Night"]
  mapper = DataFrameMapper([
      ('close_to_water', LabelEncoder()),
      ('weather', MultiLabelBinarizer(classes=weather_classes)),
      ('temp_new', MultiLabelBinarizer(classes=['Cool','Mild','Hot'])),
      ('day', MultiLabelBinarizer(classes=day_of_week)),
      ('time', MultiLabelBinarizer(classes=time_of_day)),
      (['level_one'],[SimpleImputer(strategy='constant', fill_value='most_frequent'), LabelBinarizer()]),
      ('population_density',MultiLabelBinarizer(classes=['Low','Medium','High'])),
  ], df_out=True)
  def pokemon_target(x):
    #print(id)
    if name==x:
      return 1
    else:
      return 0
  pokemon['target']=pokemon['name'].apply(pokemon_target)
  target='target'
  y=pokemon[target]
  X=pokemon.drop(target, axis=1)
  X=mapper.fit_transform(X)
  #X_train, X_val, y_train, y_val = train_test_split(X, y, random_state=117, test_size=0.85)
  train_pool = Pool(X, y)
  #val_pool = Pool(X_val, y_val)
  model = cb.CatBoostClassifier(
    iterations=150,

    logging_level='Silent',
    custom_loss=['AUC'],
    depth=None,
    l2_leaf_reg=7)
  model.fit(X, y, plot=False,verbose=False)

  res=pd.DataFrame(zip(X.columns,model.feature_importances_),columns=['Feature','Score']).sort_values(by='Score', ascending=False)
  loc=[]
  weather=[]
  day=[]
  density=[]
  time=[]
  for res in (list(res.Feature.values)):
    if (res.find("level_one")>=0) and (len(loc)<=1):
     loc.append(res.split('_')[-1])
    elif (res.find("weather")>=0) and (len(weather)<=1):
      weather.append(res.split('_')[-1])
    elif (res.find("time")>=0) and (len(time)<=1):
      time.append(res.split('_')[-1])
    elif (res.find("day")>=0) and (len(day)<=1):
      day.append(res.split('_')[-1])
    elif (res.find("density")>=0) and (len(density)<=1):
      density.append(res.split('_')[-1])

  res=pd.DataFrame(zip(loc,weather,day,density,time), columns=['loc','weather','day','density','time',])

  return res
