__author__ = 'luizcartolano'

from manageTweets import ManageTweets
from manageGoogle import ManageGoogle
import os

#----------------------------- MAIN -----------------------------
def workerTwitter(city, path_twitter, path_heatMapT):
    # instance the managerTweets object
    manager = ManageTweets()

    # reading the json file and store in a dictionary
    print("Reading json: ")
    docs = manager.read(path_twitter,'tweets_campinas.json')

    # deleting possible bots on the saved tweets
    print("Deleting bots: ")
    docs = manager.deleteBot(docs)

    print("Slicing docs: ")
    # slicing the tweets by hour
    tweets_hour = manager.slicingDocsHour(docs)
    # slicing the tweets by day
    tweets_day = manager.slicingDocsDay(docs)
    # slicing tweets by periods of a day (dawm, morning, afternoon, night)
    tweets_range = manager.slicingDocsRange(docs)
    # deleting the non-split list of tweets
    del docs[:]

    print("Plotting heat map: ")
    # plotting the heatMaps for the list of tweets sliced by hours
    manager.plotMap(path_heatMapT + "hours/", tweets_hour, city)
    # plotting the heatMaps for the list of tweets sliced by days
    manager.plotMap(path_heatMapT + "days/", tweets_day, city)
    # plotting the heatMaps for the list of tweets sliced by ranges
    manager.plotMap(path_heatMapT + "ranges/", tweets_range, city)

    return

def workerGoogle(dates, path_google, path_googleD):
    
    # instance the managerTweets object
    manager = ManageGoogle()
    
    # reading the json file and store in a dictionary
    print("Reading json: ")
    docs = manager.read(path_google)
    
    print("Getting interest dates: ")   
    routes = manager.slicingDocs(dates,docs)
    
    print("Printing routes datas on a specific file:")
    manager.printFileRoutes(routes,path_googleD)

def main():
    # path to the google json file
    path_google = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/google/'
    # path to the twitter json file
    path_twitter = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/'
    # path to the heatMap directory
    path_heatMapT = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/heatMaps/'
    # path to write datas from google
    path_googleD = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/routesTimes/'

    # list with cities where data was collected
    cities = ['campinas']
    dates = ['2018-02-12','2018-02-13','2018-02-14','2018-02-15']
    
    workerGoogle(dates,path_google,path_googleD)

    # for going through the cities and carrying out the process for each one of them
    # for city in cities:
    #     # function that takes care of the process for each city
    #     workerTwitter(city)



    return

if __name__ == '__main__':
    main()
