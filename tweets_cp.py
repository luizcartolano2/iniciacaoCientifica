from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import urllib2, json

#Set credentials
CONSUMER_KEY = 'oi2mjNdG7A7rrrVNGJTlNFmq1'
CONSUMER_SECRET = 'aBE1n0WgDNrej0nxGS9ov6fWFuhNtBlJBdg0iY9fMHQaz7zF4V'
ACCESS_TOKEN_KEY = '59915904-l5jnitYxrqZkXcltAplIRS7sGLQvRKGUduutToCZl'
ACCESS_TOKEN_SECRET = 'Jhwe2uPrpZG7Jk984LG9zgjXirzwERLn5h4u7s42k2BlH'
path = '/local1/luiz/tweets/'
filename= 'tweets_campinas.json'

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
