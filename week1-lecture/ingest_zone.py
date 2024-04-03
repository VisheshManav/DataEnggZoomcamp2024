from sqlalchemy import create_engine
import pandas as pd
import os

url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
os.system(f'wget {url} -O taxi_zone_lookup.csv')

df_zones = pd.read_csv('taxi_zone_lookup.csv')

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

df_zones.to_sql(name='zones', con=engine, if_exists='replace')