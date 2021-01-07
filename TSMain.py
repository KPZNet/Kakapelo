import argparse
import datetime
import pprint
import random
import numpy as np


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time


class db_constants:
    bucket = "Denver"
    token = "b5htN9v9bARzZEHLT512UR2nC_T5PkYuZTz28Bd1UrAV0P88uo0wZ4dmyQmL-2EfYRAS8Vg2dX_iaqPDA_dpPw=="
    org = "kpznet"
    username = "KenCeglia@hotmail.com"
    password = "Viper.12k"


class last_reads:
    last_pressure = 0
    last_temperature = 0

def GetDataValue(workout_dict):
    # wt is short for 'workout tags'
    wt = {}

    # wf is short for 'workout fields'
    wf = {}

    w = workout_dict
    wt['City'] = "Phoenix"
    # wt['created_at'] = w.created_at

    epoch_time = time.time_ns() 
    
    created_at = epoch_time
    wt['State'] = "Arizona"

    new_temperature = last_reads.last_temperature + np.random.normal()
    new_pressure = last_reads.last_pressure + np.random.normal()
    last_reads.last_temperature = new_temperature
    last_reads.last_pressure = new_pressure
    wf['Temperature'] = new_temperature
    wf['Pressure'] = new_pressure

    return created_at, wt, wf


if __name__ == '__main__':

    client = InfluxDBClient(url="http://localhost:8086", token="b5htN9v9bARzZEHLT512UR2nC_T5PkYuZTz28Bd1UrAV0P88uo0wZ4dmyQmL-2EfYRAS8Vg2dX_iaqPDA_dpPw==")
    write_api = client.write_api(write_options=SYNCHRONOUS)

    last_val = 0
    data_points = []
    for w in range(0,250):
        pprint.pprint(w)
        created_at, wt, wf = GetDataValue(w)
        json_body = [
            {
                'measurement': 'Kata',
                'tags': wt,
                'time': created_at,
                'fields': wf
            }
        ]
        pprint.pprint(json_body)
        data_points.extend(json_body)
        write_api.write(db_constants.bucket, db_constants.org, data_points)
    print('Writing %s to database' % len(data_points))

    #query = f'from(DB_NAME: \\"{DB_NAME}\\") |> range(start: -24h)'
    #tables = client.query_api().query(query, org=org)
    #pprint.pprint(tables)
