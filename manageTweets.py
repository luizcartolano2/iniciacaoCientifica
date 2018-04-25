import json
from pytz import timezone
from time import time
from datetime import datetime
import gmplot

class ManageTweets(object):
    """docstring for ManageTweets."""
    def __init__(self):
        return

    '''
        Read .json file and store his content in a dictionary
    '''
    def read(self, path, fname):
        # starts an empty list for the tweets
        tweets = []
        # opens the .json file in write mode
        with open(path+fname, 'r') as file_json:
            # assigns the content that was in .json to a list
            jsonData = json.load(file_json)
            # traverses each of the data in the json file
            for data in jsonData:
                # Not all tweets use geospatial location, so we use try/except
            	try:
                    # initialize the dictionary of each tweet
            		tweet = {}
                    # associates the coordinates of the tweet with the key "coords" in the dict
            		tweet["coords"] = data["coordinates"]["coordinates"]
                    # associates the tweet timestamp with the "time" key in the dict
            		tweet["time"] = data["timestamp_ms"]
                    # add the timezone of each tweet
            		tweet["timezone"] = "America/Sao_Paulo"
                    # add the dictionary to the list
            		tweets.append(tweet)
    			except:
                    # if the tweet does not have geolocation then go to the next
            		pass
        # returns a list of dictionaries
        return tweets

    '''
    	Plot heat map a partir de uma lista de coordenadas.
    '''
    def plottingHeatmap(self, path, key, coords, city):
        # sets the filename
        fname = 'heatmap_'+city+'_'+key+'.html'
    	# sets the city center coordinate and zoom level.
    	if city == 'chicago':
    		gmap = gmplot.GoogleMapPlotter(41.878114, -87.629799, 10)
    	elif city == 'london':
    		gmap = gmplot.GoogleMapPlotter(51.507278, -0.127690, 10)
    	elif city == 'ny':
    		gmap = gmplot.GoogleMapPlotter(40.68402, -73.95704, 10)
    	elif city == 'toronto':
    		gmap = gmplot.GoogleMapPlotter(43.653226, -79.383184, 10)
    	elif city == 'campinas':
    		gmap = gmplot.GoogleMapPlotter(-22.907104, -47.063240, 10)
    	else:
    		print("PLOT ERROR: invalid city\n")
    		return
        # select latitudes
    	heat_lats = [coord[1] for coord in coords]
        # select longitudes
        heat_lngs = [coord[0] for coord in coords]
    	if len(heat_lats):
    		# generate the plot
    		gmap.heatmap(heat_lats, heat_lngs,threshold=0)
    		# save as .html file
    		gmap.draw(path+fname)

    	return

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
    		timestamp /= 1000		# convert from microseconds to seconds
    	return datetime.fromtimestamp(timestamp)

    '''
    	Slice the tweets grouping in hours of a day
    '''
    def slicingDocsHour(self, docs):
    	list_docs = {}
    	for doc in docs:
    		date = self.getDate(doc["time"], doc["timezone"])
            # set the key with the format: daymonthhour
            key = str(date.day)+str(date.month)+str(date.year)+str(date.hour)
    		try:
                # if there is already any list of tweets for the key, cocatena the new tweet the list
                list_docs[key] += [doc]
    		except:
                # otherwise, start the list of tweets for the key
                list_docs[key] = [doc]
        # now we have a list with several sublists, where each sublist refers to tweets generated on a particular day and hour.
        return list_docs

    '''
    	Slice the tweets grouping in periods of a day
    '''
    def slicingDocsRange(self, docs):
    	list_docs = {}
    	for doc in docs:
    		date = self.getDate(doc["time"], doc["timezone"])
    		if date.hour >= 8 and date.hour <= 12:
                # the dictionary key is defined by the day, month, year and morning period
    			key = str(date.day)+str(date.month)+str(date.year)+str("morning")
    		elif date.hour > 12 and date.hour <= 20:
                # the dictionary key is defined by the day, month, year and afternoon period
                key = str(date.day)+str(date.month)+str(date.year)+str("afternoon")
    		elif date.hour > 20 and date.hour <= 24:
                # the dictionary key is defined by the day, month, year and night period
                key = str(date.day)+str(date.month)+str(date.year)+str("night")
    		else:
                # the dictionary key is defined by the day, month, year and dawm period
                key = str(date.day)+str(date.month)+str(date.year)+str("dawm")
    		try:
    			# if there is already any list of tweets for the key, cocatena the new tweet the list
    			list_docs[key] += [doc]
    		except:
                # otherwise, start the list of tweets for the key
    			list_docs[key] = [doc]
        # now we have a list with several sublists, where each sublist refers to tweets generated on a particular period of a day.
        return list_docs

    '''
    	Slice the tweets grouping in days
    '''
    def slicingDocsDay(self, docs):
    	list_docs = {}
    	for doc in docs:
    		date = self.getDate(doc["time"], doc["timezone"])
            # set the key with the format: daymonthhour
            key = str(date.day)+str(date.month)+str(date.year)
    		try:
                # if there is already any list of tweets for the key, cocatena the new tweet the list
                list_docs[key] += [doc]
    		except:
                # otherwise, start the list of tweets for the key
                list_docs[key] = [doc]
        # now we have a list with several sublists, where each sublist refers to tweets generated on a particular day.
        return list_docs

    '''
    	Eliminates possible noise of the data obtained
    '''
    def deleteBot(self, docs):
        # initializes a list where the twetts without bots will be stored
        list_docs = []
        # for going through the tweets looking for a bot
    	for doc in docs:
            # counting the number of occurrences of a specific geolocation
    		count = self.countCoords(doc["coords"],docs)
    		if count <= 10:
                # if a specific geolocation appears less than 10 times, we add to our list
    			list_docs.append(doc)

        # deleting the old list of tweets
    	del docs[:]
        # return the new list free of bots
    	return list_docs

    '''
    	Countig the occurrence of same coordinates in a list of coordinates
    '''
    def countCoords(self, coord, docs):
        # define a counter
        counter = 0
    	for tweet in docs:
            # add one to our counter everytime a specific geolocation appears
    		if tweet["coords"] == coord:
    			counter += 1

    	return counter

    '''
    	Function to manage the plotting of heat maps
    '''
    def plotMap(self, path, tweets, city):
        # we go through the dictionary of coordinate lists
        for key,value in tweets.iteritems():
            # initializes the list of coordinates to be plotted
            coords = []
            # each value (tweets list separated by keys in our dictionary), we go through the set of coordinates (lat, long)
            for tweet in value:
                # add the coordinates in the list to be plotted
                coords.append(tweet["coords"])
            # plots the heatmap for each dictionary key
            self.plottingHeatmap(path,key,coords,city)
