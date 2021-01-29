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


def ParseCommandLine():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',
                        help='number of workouts',
                        dest='num_results',
                        action='store',
                        type=int,
                        default=10)
    parser.add_argument('--debug',
                        help='provide some debugging output',
                        dest='DEBUG',
                        action='store_true',
                        default=False)
    return parser


if __name__ == '__main__':
    #parser = ParseCommandLine()
    #args = parser.parse_args()
    #DEBUG = args.DEBUG

    conn = pylotoncycle.PylotonCycle(db_constants.username, db_constants.password)

    workouts = conn.GetRecentWorkouts(200)

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

    print("Done")


