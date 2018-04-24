from manageTweets import ManageTweets

#----------------------------- MAIN -----------------------------
def worker(city):
	path_read = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/'	# caminho para o arquivo de dados
	path_heatMap = '/Users/luizeduardocartolano/Dropbox/DUDU/Unicamp/Iniciacao_Cientifica/workspace/Dados/heatMaps/'	# caminho para a pasta onde serao salvos os heatMaps

	manager = ManageTweets()

	print("Reading json: ")
	docs = manager.read(path_read,'tweets_campinas.json')

	print("Deleting bots: ")
	docs = manager.deleteBot(docs)

	print("Slicing docs: ")
	tweets_hour = manager.slicingDocsHour(docs)
	tweets_day = manager.slicingDocsDay(docs)
	tweets_range = manager.slicingDocsRange(docs)
	del docs[:]

	print("Plotting heat map: ")
	manager.plotMap(path_heatMap + "hours/", tweets_hour, city)
	manager.plotMap(path_heatMap + "days/", tweets_day, city)
	manager.plotMap(path_heatMap + "ranges/", tweets_range, city)

	return

def main():
    # lista com as cidades onde dados foram coletados
    cities = ['campinas']

    # for percorrendo as cidades e realizando o processo para cada uma delas
    for city in cities:
        # funcao que cuida do processo para cada cidade
        worker(city)
	return

if __name__ == '__main__':
	main()
