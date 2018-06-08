__author__ = 'luizcartolano'

import json
from pytz import timezone
from time import time
from datetime import datetime
import gmplot
import os
from HTML_Page import HTML_Page


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
                        #
                        route["name"] = data["summary"].encode('utf-8').replace(" ","")
                        # associates the route timestamp with the "time" key in the dict
                        route["polyline"] = data["overview_polyline"]["points"]
                         # associates the route summary with the "summary" key in the dict
                        route["summary"] = data["summary"]
                        # associates the route timestamp with the "time" key in the dict
                        route["time"] = data["timestamp"]
                        # associates the route distance with the distance key
                        route["distance"] = data["legs"][0]["distance"]["value"]
                        # associates the route duration_in_traffic with the traffic key
                        route["traffic"] = data["legs"][0]["duration_in_traffic"]["value"]
                        # associates the route duration_in_traffic with the traffic key
                        route["lat_init"] = data["legs"][0]["start_location"]["lat"]
                        # associates the route duration_in_traffic with the traffic key
                        route["lng_init"] = data["legs"][0]["start_location"]["lng"]
                        # associates the route duration_in_traffic with the traffic key
                        route["lat_fim"] = data["legs"][0]["end_location"]["lat"]
                        # associates the route duration_in_traffic with the traffic key
                        route["lng_fim"] = data["legs"][0]["end_location"]["lng"]
                        # add the timezone of each tweet
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
        Make an HTML page with the routes information
    '''
    def makeHTML(self, routes):
        htmlPage = HTML_Page()
        path = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/html_routes/'
        for route in routes:
            time = self.getDate(chartime=route["time"],tz=route["timezone"])
            name = route["name"] + "_" + str(time).replace(" ","")
            # print(name)
            htmlPage.print_html(path=path, name=name, title=name, polyline=route["polyline"], lat_init=route["lat_init"], lng_init=route["lng_init"], lat_fim=route["lat_fim"], lng_fim=route["lng_fim"], distance=route["distance"], time_of_trip=route["traffic"], timestamp=time, traffic=route["traffic"], dist=route["distance"])

        return

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

    '''
        Print the interest datas from GoogleMaps routes
    '''
    def printFileRoutes(self, docs, path):
        for key,value in docs.iteritems():
            file = key
            filename = file + "_times.txt"
            filepath = os.path.join(path, filename)
            f = open(filepath,"w")
            for data in value:                
                f.write("\n")
                f.write('\t summary: ' + repr(data["summary"]) + '\n')
                f.write('\t polyline: ' + str(data["polyline"]) + '\n')
                f.write('\t time: ' + str(data["time"]) + '\n')
                f.write('\t distance:' + str(data["distance"]) + '\n')
                f.write('\t traffic:' + str(data["traffic"]) + '\n')
                f.write('\t latitude:' + str(data["lat"]) + '\n')
                f.write('\t longitude:' + str(data["lng"]) + '\n')
                f.write("\n")

        f.close()

    '''
        Plot heat map a partir de uma lista de coordenadas.
    '''
    def plottingHeatmap(self, path, key, lats, lons, city):
        
        # sets the filename
        fname = 'heatmap_'+city+'_'+key+'.html'        
        
        # sets the city center coordinate and zoom level.
        if city == 'campinas':
            gmap = gmplot.GoogleMapPlotter(-22.907104, -47.063240, 10)
        else:
            print("PLOT ERROR: invalid city\n")
            return
        
        # gmap.circle(lats, lons)
        # gmap.plot(lats, lons, 'cornflowerblue', edge_width=10)
        gmap.scatter(lats=lats, lngs=lons, color='#000000',size=40, marker=False)
        # gmap.grid(slat=lats[0], elat=lats[-1], latin=0.001, slng=lons[0], elng=lons[-1], lngin=0.001)

        # save as .html file
        gmap.draw(path+fname)

        return

    # This function is free of any dependencies.
    # code from https://github.com/geodav-tech/decode-google-maps-polyline
    def decode_polyline(self,polyline_str):
        '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs'''
        index, lat, lng = 0, 0, 0
        coordinates = []
        changes = {'latitude': 0, 'longitude': 0}

        # Coordinates have variable length when encoded, so just keep
        # track of whether we've hit the end of the string. In each
        # while loop iteration, a single coordinate is decoded.
        while index < len(polyline_str):
            # Gather lat/lon changes, store them in a dictionary to apply them later
            for unit in ['latitude', 'longitude']: 
                shift, result = 0, 0

                while True:
                    byte = ord(polyline_str[index]) - 63
                    index+=1
                    result |= (byte & 0x1f) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break

                if (result & 1):
                    changes[unit] = ~(result >> 1)
                else:
                    changes[unit] = (result >> 1)

            lat += changes['latitude']
            lng += changes['longitude']

            coordinates.append((lat / 100000.0, lng / 100000.0))

        return coordinates
