import os
import json
import requests

import numpy as np
from datetime import datetime as dt
from dateutil.tz import gettz
from matplotlib import pyplot as plt

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
import config
bearer_token = config.BEARER_TOKEN

# Optional params: start_time,end_time,since_id,until_id,next_token,granularity
query_params = {'query': 'game update','granularity': 'hour'}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    #r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def count_tweets(query):
    count_url = "https://api.twitter.com/2/tweets/counts/recent"
    query_params = {
        'query': query,
        'granularity': 'hour',
    }
    json_response = connect_to_endpoint(count_url, query_params)
    return json_response["data"]

def search_tweets(query, search_datetime):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
        'query': query,
        'end_time': search_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        #'query': '"game update" AND place:"Fukuoka" AND since:2022-10-05 AND until:2022-10-05',
    }
    json_response = connect_to_endpoint(search_url, query_params)
    return json_response["data"]

def parse_search_category(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data["designations"], data["relates"]