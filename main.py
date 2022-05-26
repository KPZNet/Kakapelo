'''
workouts_to_influxdb.py
Example usage of using pylotoncycle to pull in your workouts and import
them into influxdb.
'''

import argparse
import datetime
import pprint

from consts import db_constants
from consts import ParsePelotonWorkout

import pylotoncycle
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS



if __name__ == '__main__':
    
    conn = pylotoncycle.PylotonCycle(db_constants.username, db_constants.password)

    workouts = conn.GetRecentWorkouts(100)

    client = InfluxDBClient(url="http://localhost:8086", token=db_constants.token)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data_points = []
    for w in workouts:
        pprint.pprint(w)
        created_at, wt, wf = ParsePelotonWorkout(w)
        json_body = [
            {
                'measurement': 'peloton_workouts',
                'tags': wt,
                'time': created_at,
                'fields': wf
            }
        ]
        pprint.pprint(json_body)
        data_points.extend(json_body)
        write_api.write(db_constants.bucket, db_constants.org, json_body)

    #write_api.write(db_constants.bucket, db_constants.org, data_points)
    print("Done")

