'''
workouts_to_influxdb.py
Example usage of using pylotoncycle to pull in your workouts and import
them into influxdb.
'''

import argparse
import datetime
import pprint

from consts import db_constants

import pylotoncycle

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



if __name__ == '__main__':

    client = InfluxDBClient(url="http://localhost:8086", token=db_constants.token)

    query = f'from(bucket: "{db_constants.bucket}") |> range(start: -100d)'
    tables = client.query_api().query(query, org=db_constants.org)

    print(tables)





