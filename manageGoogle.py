__author__ = 'luizcartolano'

import json
from pytz import timezone
from time import time
from datetime import datetime
import gmplot

class ManageGoogle(object):
    """docstring for ManageTweets."""
    def __init__(self):
        return

    '''
        Read .json file and store his content in a dictionary
    '''
    def read(self, path, fname):
        # starts an empty list for the tweets
        routes = []
        # opens the .json file in write mode
        with open(path+fname, 'r') as file_json:
            # assigns the content that was in .json to a list
            jsonData = json.load(file_json)
            # traverses each of the data in the json file
            for data in jsonData:
                # initialize the dictionary of each tweet
                route = {}
                # associates the tweet timestamp with the "time" key in the dict
                route["time"] = data["timestamp"]
                # add the timezone of each tweet
                route["timezone"] = "America/Sao_Paulo"
                # add the dictionary to the list
                routes.append(route)

        # returns a list of dictionaries
        return routes
