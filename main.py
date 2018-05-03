__author__ = 'luizcartolano'

from manageTweets import ManageTweets

#----------------------------- MAIN -----------------------------
def worker(city):
	# path to the json file
	path_read = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/'	# caminho para o arquivo de dados
	# path to the heatMap directory
	path_heatMap = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/heatMaps/'	# caminho para a pasta onde serao salvos os heatMaps

	# instance the managerTweets object
	manager = ManageTweets()

	# reading the json file and store in a dictionary
	print("Reading json: ")
	docs = manager.read(path_read,'tweets_campinas.json')

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
	manager.plotMap(path_heatMap + "hours/", tweets_hour, city)
	# plotting the heatMaps for the list of tweets sliced by days
	manager.plotMap(path_heatMap + "days/", tweets_day, city)
	# plotting the heatMaps for the list of tweets sliced by ranges
	manager.plotMap(path_heatMap + "ranges/", tweets_range, city)

	return

def main():
    # list with cities where data was collected
    cities = ['campinas']

    # for going through the cities and carrying out the process for each one of them
    for city in cities:
        # function that takes care of the process for each city
        worker(city)
	return

if __name__ == '__main__':
	main()
