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
                try:
                    # initialize the dictionary of each route
                    route = {}
                    # associates the route timestamp with the "time" key in the dict
                    route["time"] = data["timestamp"]
                    # associates the route distance with the distance key
                    route["distance"] = data["legs"]["distance"]["value"]
                    # associates the route duration_in_traffic with the traffic key
                    route["traffic"] = data["legs"]["duration_in_traffic"]["value"]
                    # associates the route duration with the duration key
                    route["duration"] = data["legs"]["distance"]["duration"]
                    # add the timezone of each tweet
                    route["timezone"] = "America/Sao_Paulo"
                    # add the dictionary to the list
                    routes.append(route)
                except:
                    pass

        # returns a list of dictionaries
        return routes

    '''
        Find the date of a tweet based on his timestamp
    '''
    def getDate(self, chartime, tz):
        timestamp = float(chartime)
        try:
            # if the timestamp is in seconds, the timestamp conversion to p / date occurs without errors
            date = datetime.fromtimestamp(timestamp)
        except:
            # otherwise, I need to convert from microseconds to sec first
            date = self.convertTimestamp(timestamp)
        date_aware = timezone(tz).localize(date)
        # converts according to tweet timezone
        new_date = date_aware.astimezone(timezone(tz))
        return new_date

    '''
        Convert the timestamp of a tweet from microseconds to seconds
    '''
    def convertTimestamp(self, timestamp):
        if timestamp > 1519231541:  # Date of today - UTC: Wednesday 21st February 2018 04:45:41 PM
            timestamp /= 1000       # convert from microseconds to seconds
        return datetime.fromtimestamp(timestamp)

    def slicingDocs(self, dates, docs):
        list_routes = {}
        for doc in docs:
            date = str(self.getDate(doc["time"],doc["timezone"]))
            date = date.split(' ',1)
            if date[0] in dates:
                try:
                    list_routes[date[0]] += [doc]
                except:
                    list_routes[date[0]] = [doc]
        
        del docs[:]
        return list_routes