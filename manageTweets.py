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
    	tweets = []												# inicia uma lista vazia para os tweets
    	with open(path+fname, 'r') as file_json:				# abre o arquivo .json em modo de escrita
    		jsonData = json.load(file_json)						# atribui o conteudo que estava no .json a uma lista
    		for data in jsonData:								# percorre cada um dos dados do arquivo json
    			try:											# nem todos os tweets usam localizacao geoespacial, por isso usa-se o try/except
    				tweet = {}									# inicializa o dicionario de cada tweet
    				tweet["coords"] = data["coordinates"]["coordinates"]	# associa as coordenadas do tweet a chave "coors" no dict
    				tweet["time"] = data["timestamp_ms"]					# associa o timestamp do tweet a chave "time" no dict
    				tweet["timezone"] = "America/Sao_Paulo"					# adiciona o timezone de cada tweet
    				tweets.append(tweet)									# adiciona o dicionario a lista
    			except:
    				pass													# caso o tweet nao possua geolocalizacao segue-se para o proximo
    	return tweets											# retorna se uma lista de dicionarios

    '''
    	Plot heat map a partir de uma lista de coordenadas.
    '''
    def plottingHeatmap(self, path, key, coords, city):
    	fname = 'heatmap_'+city+'_'+key+'.html'
    	# Define a coordenada central da cidade e o nivel de zoom.
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
    	heat_lats = [coord[1] for coord in coords] # Seleciona as latitudes
    	heat_lngs = [coord[0] for coord in coords] # Seleciona as longitudes
    	if len(heat_lats):
    		# Gera o plot
    		gmap.heatmap(heat_lats, heat_lngs,threshold=0)
    		# Salva como arquivo .html
    		gmap.draw(path+fname)

    	return

    '''
    	Find the date of a tweet based on his timestamp
    '''
    def getDate(self, chartime, tz):
    	timestamp = float(chartime)
    	try:
    		date = datetime.fromtimestamp(timestamp) # Se o timestamp estiver em segundos, a conversao de timestamp p/ date ocorre sem erros
    	except:
    		date = self.convertTimestamp(timestamp)		 # Caso contrario, e preciso converter de microsegundos p/ segundos primeiro
    	date_aware = timezone(tz).localize(date)
    	new_date = date_aware.astimezone(timezone(tz))	# Converte de acordo com a timezone do tweet
    	#print date_aware, new_date
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
    		key = str(date.day)+str(date.month)+str(date.year)+str(date.hour)
    		try:
    			list_docs[key] += [doc]						   # Se ja houver alguma lista de tweets para a chave, cocatena o novo tweet a lista
    		except:
    			list_docs[key] = [doc]						   # Caso contrario, inicia a lista de tweets para a chave
    	return list_docs									   # agora temos uma lista com varias sublistas, onde cada sublista e referente
    														   # aos tweets gerados em um determinado dia e horario.

    '''
    	Slice the tweets grouping in periods of a day
    '''
    def slicingDocsRange(self, docs):
    	list_docs = {}
    	for doc in docs:
    		date = self.getDate(doc["time"], doc["timezone"])
    		if date.hour >= 8 and date.hour <= 12:
    			key = str(date.day)+str(date.month)+str(date.year)+str("manha") # A chave do dicionario e definida pelo dia, mes, ano e hora
    		elif date.hour > 12 and date.hour <= 20:
    			key = str(date.day)+str(date.month)+str(date.year)+str("tarde") # A chave do dicionario e definida pelo dia, mes, ano e hora
    		elif date.hour > 20 and date.hour <= 24:
    			key = str(date.day)+str(date.month)+str(date.year)+str("noite") # A chave do dicionario e definida pelo dia, mes, ano e hora
    		else:
    			key = str(date.day)+str(date.month)+str(date.year)+str("madrugada") # A chave do dicionario e definida pelo dia, mes, ano e hora
    		try:
    			# print(key)
    			list_docs[key] += [doc]						   # Se ja houver alguma lista de tweets para a chave, cocatena o novo tweet a lista
    		except:
    			list_docs[key] = [doc]						   # Caso contrario, inicia a lista de tweets para a chave
    	return list_docs									   # agora temos uma lista com varias sublistas, onde cada sublista e referente
    														   # aos tweets gerados em um determinado dia e horario.

    '''
    	Slice the tweets grouping in days
    '''
    def slicingDocsDay(self, docs):
    	list_docs = {}
    	for doc in docs:
    		date = self.getDate(doc["time"], doc["timezone"])
    		key = str(date.day)+str(date.month)+str(date.year)
    		try:
    			list_docs[key] += [doc]						   # Se ja houver alguma lista de tweets para a chave, cocatena o novo tweet a lista
    		except:
    			list_docs[key] = [doc]						   # Caso contrario, inicia a lista de tweets para a chave
    	return list_docs									   # agora temos uma lista com varias sublistas, onde cada sublista e referente
    														   # aos tweets gerados em um determinado dia e horario.

    '''
    	Eliminates possible noise of the data obtained
    '''
    def deleteBot(self, docs):
    	list_docs = []											# inicializa-se uma lista onde serao armazenados os twetts sem bots
    	for doc in docs:
    		count = self.countCoords(doc["coords"],docs)
    		if count <= 10:
    			list_docs.append(doc)

    	del docs[:]
    	return list_docs

    '''
    	Countig the occurrence of same coordinates in a list of coordinates
    '''
    def countCoords(self, coord, docs):
    	counter = 0
    	for tweet in docs:
    		if tweet["coords"] == coord:
    			counter += 1

    	return counter

    '''
    	Function to manage the plotting of heat maps
    '''
    def plotMap(self, path, tweets, city):
        for key,value in tweets.iteritems():					# percorremos o dicionario de listas de coordenadas
    		coords = []											# inicializa-se a lista de coordenadas a serem plotadas
    		for tweet in value:									# cada valor (lista de tweets separada por chaves no nosso dicionario), percorremos o conjunto de coordenadas (lat,long)
    			coords.append(tweet["coords"])					# adiciona-se as coordenadas na lista a ser plotada
    		self.plottingHeatmap(path,key,coords,city)		    # plota o heatmap para cada chave do dicionario
