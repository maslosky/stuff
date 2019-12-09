#!/usr/local/bin/python
from datetime import datetime
from datetime import timedelta  
import os
import sys
import time
import ox3apiclient
import logging
import requests
import json
import my_creds

# LOAD CREDS FROM 'my_creds.py' - in the Python lib dir
email = my_creds.email
password = my_creds.password
domain = my_creds.domain
realm = my_creds.realm
consumer_key = my_creds.consumer_key
consumer_secret = my_creds.consumer_secret

ox = ox3apiclient.Client(
  email = email,
  password = password,
  domain = domain,
  realm = realm,
  consumer_key = consumer_key,
  consumer_secret = consumer_secret,
  api_path = '/data/1.0')

ox.logon(email, password)

ox.logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ox.logger.addHandler(ch)

list_dates = ['2019-12-02', '2019-12-03', '2019-12-04']
#let 's start with the first 2 dates
for report_date in list_dates[0: 2]:

#loop through all listed dates uncomment this and comment the line above:
#for report_date in list_dates:

  while True:
    print("\n----------------")
    print("Running report for " + report_date)
    report_date_object = datetime.strptime(report_date, '%Y-%m-%d')
    report_date_end = report_date_object + timedelta(days=1) 
    settings = {
    "startDate": report_date + "T00:00:00Z",
    "endDate": report_date_end.strftime('%Y-%m-%d') + "T00:00:00Z",
    "attributes": [{
        "id": "publisherAdUnitName"
    }, {
        "id": "publisherCurrency"
    }],
    "metrics": [{
        "id": "marketRequests"
    }, {
        "id": "clicks"
    }, {
        "id": "marketImpressions"
    }, {
        "id": "marketPublisherRevenue"
    }],
    }
    print(settings)

    print("   Waiting 60 seconds for the report to download...")
    time.sleep(60)

    response = ox.post('/report/', data = json.dumps(settings));
    json_data = json.dumps(response)
    file = open("report_" + report_date + ".json","w")
    file.write(json_data)
    file.close()
    print("   File saved: report_" + report_date + ".json")
    break;
