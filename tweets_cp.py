from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import urllib2, json

#Set credentials
CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
ACCESS_TOKEN_KEY = 'YOUR_ACCESS_TOKEN_KEY'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'
path = 'YOUR_PATH'
filename= 'YOUR_FILENAME'

#Autentica a API com as credenciais
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

class StdOutListener(StreamListener):
    def on_data(self, data):
        with open(path+filename, 'a') as file:
            parsed_data = json.loads(data)
            json.dump(parsed_data, file, indent=2)
        return True
    def on_error(self, status):
        print status
        if status == 420:
                #Clients exceed limited number of attempts to connect to stream API.
                #The amount time a client has to wait increase exponentially
                return False
        else:
                return True

if __name__ == '__main__':
    # Set bound box of the city
    coord = [-47.2461,-23.0612,-46.8152,-22.7290]
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)
    stream.filter(locations= coord)
