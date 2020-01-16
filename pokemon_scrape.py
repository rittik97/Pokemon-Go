from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

data=pd.read_csv('data/pokemon_go.csv')
url='https://pokemondb.net/go/pokedex'
r=requests.get(url)
html=r.text
soup=BeautifulSoup(html)



id=[]
#id.append(0)
name=[]
types_one=[]
types_two=[]
attack=[]
defense=[]
hp=[]
catch=[]
flee=[]
candy=[]
last_id=0
count=0
while count<250:
        count+=1
        x=soup.find('table').find_all('tr')[count].find_all('td')
        ids=int(x[0].text)
        if ids==last_id:
            continue

        id.append(ids)
        '''if (not(not id)):
                id.append(ids)#find('span', class_="cell-num cell-fixed")
        else:
            if (ids == id[i-1]):
                break

        if(i>1):
            if(ids == id[i-1]):
                break
        '''


        name.append(x[1].text)
        types=[]
        for i in x[2].find_all('a'):
            types.append(i.text)
            #elif i==1:
            #    types_two.append(i.text)
        types_one.append(types)
        attack.append(x[3].text)
        defense.append(x[4].text)
        hp.append(x[5].text)
        catch.append(x[6].text)
        flee.append(x[7].text)
        candy.append(x[8].text)
        last_id=ids


d=pd.DataFrame(zip(
id,

name,
types_one,
attack,
defense,
hp,
catch,
flee,
candy,
), columns=[
'id',
'name',
'types_one',
'attack',
'defense',
'hp',
'catch',
'flee',
'candy',
])

new_data=pd.merge(left=data, right=d, how='left', left_on='pokedex_id', right_on='id')

def extractor(x):
    return x[0]
d['type']=d['types_one'].apply(extractor)

new_data.head(2)['type']

d.to_csv('data/scrape.csv',index=False)
d
for i in np.unique(data['city']):
    print(f'<option value="{i}">')

'Breezy'
'BreezyandMostlyCloudy'
'BreezyandOvercast'
'BreezyandPartlyCloudy'
'Clear'
'DangerouslyWindy'
'Drizzle'
'DrizzleandBreezy'
'Dry'
'DryandMostlyCloudy'
'DryandPartlyCloudy'
'Foggy'
'HeavyRain'
'Humid'
'HumidandOvercast'
, 'HumidandPartlyCloudy'
, 'LightRain',
       'LightRainandBreezy', 'MostlyCloudy', 'Overcast', 'PartlyCloudy',
       'Rain', 'RainandWindy', 'Windy', 'WindyandFoggy',
       'WindyandPartlyCloudy'
