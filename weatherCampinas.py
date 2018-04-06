import urllib2
import json
import time

path = 'YOUR_PATH'
filename= 'YOUR_FILENAME'

#Ultimo dia de coleta
time_final = 1577836799  #Tue, 31 Dec 2019 23:59:59 GMT
current_time = time.time()
while current_time<time_final:
    f = urllib2.urlopen('https://api.wunderground.com/api/cf3fccc704240ff5/conditions/q/YOUR_COORDINATES.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    temp_f = parsed_json['current_observation']['temp_f']
    fileCamp = open(path+filename, 'a')
    fileCamp.write(json_string)
    fileCamp.close()
    f.close()
    time.sleep(1210)
    current_time = time.time()
