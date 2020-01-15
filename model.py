import pandas as pd

import pickle


from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import StandardScaler, LabelEncoder, LabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

df1 = pd.read_csv('data/new_data.csv')
df = pd.read_csv('data/pokefinal.csv')

df = pd.merge(left=df, right=df1['type'], how='left', left_on=df.index, right_on=df1.index)

df['morning'] = ((df['time'] >=357) & (df['time'] <= 1200))
df['afternoon'] = ((df['time'] >=1201) & (df['time'] <= 1800))
df['night'] = ((df['time'] >=1801) & (df['time'] <= 2400))

del df['time']
del df['types_one']

target = 'type'
y = df[target]
X = df.drop(target, axis=1)


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mapper = DataFrameMapper([
    ('close_to_water', LabelEncoder()),
    ('city', LabelBinarizer()),
    ('weather', LabelBinarizer()),
    ('temperature', None),
    ('day', LabelBinarizer()),
    ('morning', LabelEncoder()),
    ('afternoon', LabelEncoder()),
    ('night', LabelEncoder()),
], df_out=True)

Z_train = mapper.fit_transform(X_train)
Z_test = mapper.transform(X_test)

model = LogisticRegression().fit(Z_train, y_train)
model.score(Z_test, y_test)

pipe = make_pipeline(mapper, model)
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)
pickle.dump(pipe, open('pipe.pkl', 'wb'))


