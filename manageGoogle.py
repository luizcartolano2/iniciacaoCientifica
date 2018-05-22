__author__ = 'luizcartolano'

import json
from pytz import timezone
from time import time
from datetime import datetime
import gmplot
import os

class ManageGoogle(object):
    """docstring for ManageTweets."""
    def __init__(self):
        return

    '''
        Read .json file and store his content in a dictionary
    '''
    def read(self, path):
        # starts an empty list for the tweets
        routes = []
        
        # for going through all routes files
        for filename in os.listdir(path):
            if filename != ".DS_Store":
                # print("filename: " + filename)
                # opens the .json file in write mode
                with open(path+filename, 'r') as file_json:
                    # assigns the content that was in .json to a list
                    jsonData = json.load(file_json)
                    # traverses each of the data in the json file
                    for data in jsonData:
                        # initialize the dictionary of each route
                        route = {}
                        # associates the route timestamp with the "time" key in the dict
                        route["time"] = data["timestamp"]
                        # associates the route distance with the distance key
                        route["distance"] = data["legs"][0]["distance"]["value"]
                        # associates the route duration_in_traffic with the traffic key
                        route["traffic"] = data["legs"][0]["duration_in_traffic"]["value"]
                        # associates the route duration with the duration key
                        # route["duration"] = data["legs"][0]["distance"]["duration"]
                        # # add the timezone of each tweet
                        route["timezone"] = "America/Sao_Paulo"
                        # add the dictionary to the list
                        routes.append(route)

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

    '''
        Slice the routes grouping the days I'm interested
    '''
    def slicingDocs(self, dates, docs):
        list_routes = {}
        for doc in docs:
            date = str(self.getDate(doc["time"],doc["timezone"]))
            day = self.getDate(doc["time"],doc["timezone"])
            date = date.split(' ',1)
            if date[0] in dates:
                if day.hour >= 8 and day.hour <= 12:
                    # the dictionary key is defined by the day, month, year and morning period
                    key = str(date[0])+str("-morning")
                elif day.hour > 12 and day.hour <= 20:
                    # the dictionary key is defined by the day, month, year and afternoon period
                    key = str(date[0])+str("-afternoon")
                elif day.hour > 20 and day.hour <= 24:
                    # the dictionary key is defined by the day, month, year and night period
                    key = str(date[0])+str("-night")
                else:
                    # the dictionary key is defined by the day, month, year and dawm period
                    key = str(date[0])+str("-dawm")
                
                try:
                    list_routes[key] += [doc]
                except:
                    list_routes[key] = [doc]
        
        del docs[:]
        return list_routes

    def printFileRoutes(self, docs, path, filename):
        file = str(filename).split(".")
        filename = file[0] + "_times.txt"
        filepath = os.path.join(path, filename)
        f = open(filepath,"w+")
        # print(docs)
        for key,value in docs.iteritems():
            for data in value:                
                f.write("\n")
                f.write(key + ": \n")
                f.write('\t time: ' + str(data["time"]) + '\n')
                f.write('\t distance:' + str(data["distance"]) + '\n')
                f.write('\t traffic:' + str(data["traffic"]) + '\n')
                # f.write('duration:' + str(data["duration"]))
                f.write("\n")

        f.close()
