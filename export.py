#!/usr/bin/env python

from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = endpoint
  def collect(self):
    # Fetch the JSON
    response = json.loads(requests.get('https://tower.mydomain.lan/api/v2/instances/',
                         auth=('admin', 'redhat123'), verify=False).content.decode('UTF-8'))

    # Present consumed capacity as gauge
    metric = Metric('consumed_capacity',
        'Consumed Capacity', 'gauge')
    metric.add_sample('consumed_capacity',
        value=response['results'][0]['consumed_capacity'], labels={})
    yield metric

    # Present capacity remaining as gauge
    metric = Metric('percent_capacity_remaining',
        'Percent Capacity Remaining', 'gauge')
    metric.add_sample('percent_capacity_remaining',
        value=response['results'][0]['percent_capacity_remaining'], labels={})
    yield metric

if __name__ == '__main__':
  # Usage: json_exporter.py port endpoint
  start_http_server(int(sys.argv[1]))
  REGISTRY.register(JsonCollector(sys.argv[2]))

  while True: time.sleep(1)
