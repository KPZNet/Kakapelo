'''
workouts_to_influxdb.py
Example usage of using pylotoncycle to pull in your workouts and import
them into influxdb.
'''

import argparse
import datetime
import pprint

import pylotoncycle

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class db_constants:
    bucket = "KOne"
    token = "_22qQ9rTQarySaVAE1VIbK3i1X5bbfO-zfx8A96CngZwAVoZvPVZL-xblnDuZcyxq_lwwVz-5NfP90m-3MUgbA=="
    org = "kpznet"
    username = "KenCeglia@hotmail.com"
    password = "Viper.12k"


if __name__ == '__main__':

    client = InfluxDBClient(url="http://localhost:8086", token=db_constants.token)

    query = f'from(bucket: "{db_constants.bucket}") |> range(start: -100d)'
    tables = client.query_api().query(query, org=db_constants.org)

    print(tables)





