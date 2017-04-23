import json
import os
import settings
import urllib.request


'''
#response = urllib.request.urlopen('http://52.88.147.108/Twitter1492300810.71.json')
#tweets_file = response.readlines()


#tweets_data_path = os.path.join(settings.DATA_DIR, 'Twitter.json')

tweets_data_path = 'Twitter.json'
tweets_file = open(tweets_data_path, "r")


for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
'''   

with open(os.path.join(settings.DATA_DIR, 'twitter1492925833.877711.json'), "r") as data_file:
    json = json.load(data_file)
