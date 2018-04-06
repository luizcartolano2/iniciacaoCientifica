import json
import time
from datetime import datetime
import googlemaps

CONSUMER_KEY_2 = 'YOUR_CONSUMER_KEY'
#Ultimo dia de coleta
time_final = 1577836799  #Tue, 31 Dec 2019 23:59:59 GMT
current_time = time.time()
gmaps = googlemaps.Client(key=CONSUMER_KEY_2)
#Determinar no maximo 10 origens e 10 destinos para nao ultrapassar o limite diario
avenidas = ['Av Prestes Maia_ida','Av Prestes Maia_volta',
            'Av Albino J B de Oliveira_ida', 'Av Albino J B de Oliveira_volta',
            'Av Jose de Souza Campos_ida', 'Av Jose de Souza Campos_volta',
            'Av John Boyd Dunlop_ida', 'Av John Boyd Dunlop_volta',
            'Av Franciso Glicerio',
            'Av Benjamin Constant']

origens = ['-22.924725,-47.067356', '-22.931458,-47.071272',
           '-22.833240,-47.078880', '-22.825156,-47.079862',
           '-22.905227,-47.046635', '-22.899715,-47.047656',
           '-22.919720,-47.111035', '-22.913917,-47.101171',
           '-22.897493,-47.064660',
           '-22.904543,-47.064909']

destinos =['-22.931400,-47.071330', '-22.924764,-47.067228',
           '-22.825139,-47.079759', '-22.833233,-47.079021',
           '-22.899715,-47.047656', '-22.905281,-47.046931',
           '-22.914007,-47.100981', '-22.919611,-47.111081',
           '-22.907329,-47.058598',
           '-22.906044,-47.068219']

# 01:30, 05:30, 09:30, 13:30,17:30, 21:30 (60 requisicoes por dia)
while current_time < time_final:
  timestamp = time.time()
  for i in range(len(avenidas)):
    with open('routes_from_'+str(i)+'.json', 'a') as fileRoute:
      route = gmaps.directions(origens[i], destinos[i],
                            departure_time="now",
                            traffic_model="best_guess",
                            mode="driving",
                          )
      data = {}
      data["overview_polyline"] = route[0]["overview_polyline"]
      data["timestamp"] = timestamp
      data["warnings"] = route[0]["warnings"]
      data["summary"] = route[0]["summary"]
      data["legs"] = route[0]["legs"]
      json.dump(data, fileRoute, indent=2)
      time.sleep(14400)
      current_time = time.time()
