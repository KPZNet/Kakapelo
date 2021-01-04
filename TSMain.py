import argparse
import datetime
import pprint
import random


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time


def ParseData(workout_dict):
    # wt is short for 'workout tags'
    wt = {}

    # wf is short for 'workout fields'
    wf = {}

    w = workout_dict
    wt['City'] = "Flagstaff"
    # wt['created_at'] = w.created_at

    epoch_time = time.time_ns() 
    
    created_at = epoch_time
    wt['State'] = "Phoenix"

    wf['Temperature'] = random.random()
    wf['Pressure'] = random.random()

    return created_at, wt, wf


if __name__ == '__main__':

    username = 'KenCeglia@hotmail.com'
    password = 'Viper.12k'


    token = "tLtgfm9pZ3cwIdvqSOEm3pTRw4QdQUBrvtHkEMIQsguxdzo-Aj7uV3j3jd3HrDBOLO5s9qy8e-yflHcipqBFPw=="
    org = "kpznet"
    bucket = "Pede"

    client = InfluxDBClient(url="http://localhost:8086", token=token)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data_points = []
    for w in range(0,20):
        pprint.pprint(w)
        created_at, wt, wf = ParseData(w)
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
    print('Writing %s to database' % len(data_points))
    write_api.write(bucket, org, data_points)
