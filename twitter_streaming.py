import json
import time
import os
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import settings

total_count = 1
file_name = str(time.time())

class MyStreamListener (StreamListener):
        def __init__(self, limit=10000):
            self.limit = limit

        def on_data(self, raw_data):
            try:
                if 'delete' in raw_data:
                    return True

                global total_count
                global file_name
                
                if divmod(total_count, self.limit)[1] == 0:
                    file_name = str(time.time())

                total_count += 1

                #print (raw_data)

                with open(os.path.join(settings.DATA_DIR, 'twitter'+file_name+'.json'), 'a') as f:
                    f.write(raw_data)

                return True

            except BaseException as e:
                #print ('failed ondata', str(e))
                time.sleep(5)
                return True

        def on_error (self, status) :
            #returning False in on_data disconnects the stream
            if status == 420:
                return False

auth = OAuthHandler(settings.CUSTOMER_KEY, settings.CUSTOMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

while True:
    try:
        twitterStream = Stream(auth, MyStreamListener())
        twitterStream.sample()
    except KeyboardInterrupt:
        # Or however you want to exit this loop
        twitterStream.disconnect()
        break
    except:
        # Oh well, reconnect and keep trucking
        continue

        
