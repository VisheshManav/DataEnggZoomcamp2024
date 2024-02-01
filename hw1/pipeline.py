import pandas as pd
from sqlalchemy import create_engine
import argparse
from time import time

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

engine.connect()

df_iter = pd.read_csv('green_tripdata_2019-09.csv', iterator=True, chunksize=100000)
i=0
while True:
    df = next(df_iter)
    if i==0:
        df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
        i+=1
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.to_sql(name='green_taxi_data', con=engine, if_exists='append')
    print('inserted another chunk')
