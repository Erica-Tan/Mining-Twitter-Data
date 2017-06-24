import json
import time
import os
import settings
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

class MyStreamListener (StreamListener):
	def __init__(self, limit_num=100, neo4j_num=200, extract_num=1000):
		self.limit_num = limit_num
		self.neo4j_num = neo4j_num
		self.extract_num = extract_num

	def on_data(self, raw_data):
		global total_count
		global file_name
		global query
					 
		try:
			tweet = json.loads(raw_data)
			
			#ignore delete record
			if 'delete' in tweet:
				return True

			# format data
			tweet = self.format_data(tweet)

			#if total_count <= self.neo4j_num:
				#save data to neo4j
				#graph.run(query, json = tweet)

			if total_count > self.extract_num:
				return False

			# format Json file
			if total_count == 1:
			       self.format_json(file_name, '[')
			       self.save_file_name(file_name)

			# if it is the last record, no comma at the end
			if_last_record = divmod(total_count, self.limit_num)[1] == 0

			#print (json.dumps(tweet))

            # save the data into Json file
			with open(os.path.join(settings.DATA_DIR, 'twitter'+file_name+'.json'), 'a') as f:
				f.write(json.dumps(tweet))
				if if_last_record == False:
					f.write(',')
					f.write('\n')

            # format Json file
			if if_last_record == True:
				self.format_json(file_name, ']')
				file_name = str(time.time())
				self.format_json(file_name, '[')
				self.save_file_name(file_name)

			# increase total_count
			total_count += 1

			return True

		except BaseException as e:
			save_error(self, 'failed ondata-'+ str(e))
			time.sleep(5)
			return True


	def on_error (self, status) :
		'''
		print(status)

		#returning False in on_data disconnects the stream
		if status == 420:
		    return False
		'''

		save_error(self, status)
		return False

	def save_error(self, error):
		with open(os.path.join(settings.DATA_DIR, 'Listen_error.txt'), 'a') as f:
		    f.write(error)
		    f.write('\n')

	def save_file_name(self, file_name):
		with open(os.path.join(settings.DATA_DIR, 'filename.txt'), 'a') as f:
			f.write('"'+file_name+'"')
			f.write(',')


	def format_json(self, file_name, symbol):
		with open(os.path.join(settings.DATA_DIR, 'twitter'+file_name+'.json'), 'a') as f:
			f.write(symbol)

	def format_data(self, tweet):
		# format source
		if 'source' in tweet :
			source_url = source_name = ''
			source_info = tweet['source'].replace('<a href="', '')
			source_info = source_info.replace('" rel="nofollow"', '')
			source_info = source_info.replace('</a>', '')
			source_info = source_info.split('>')
			source_url, source_name = source_info[0], source_info[1]

			tweet['source_url'] = source_url
			tweet['source_name'] = source_name

		if ('extended_tweet' in tweet):
			del tweet['extended_tweet']

		if ('extended_entities' in tweet):
			del tweet['extended_entities']

		# format urls & user_mentions
		if ('entities' in tweet):
			if ('urls' in tweet['entities']):
				urls = []
				for url in  tweet['entities']['urls']:
					if url['url'] != '':
						urls.append(url)

			tweet['entities']['urls'] = urls

		if ('user_mentions' in tweet['entities']):
			user_ids = []
			for user in  tweet['entities']['user_mentions']:
				user_ids.append(user['id'])

			tweet['entities']['user_mentions_ids'] = user_ids


		if ('retweeted_status' in tweet):
			retweeted_status = tweet['retweeted_status']

			# format source
			if 'source' in retweeted_status :
				source_url = source_name = ''
				source_info = retweeted_status['source'].replace('<a href="', '')
				source_info = source_info.replace('" rel="nofollow"', '')
				source_info = source_info.replace('</a>', '')
				source_info = source_info.split('>')
				source_url, source_name = source_info[0], source_info[1]
				tweet['retweeted_status']['source_url'] = source_url
				tweet['retweeted_status']['source_name'] = source_name
		
			if ('extended_tweet' in retweeted_status):
				del tweet['retweeted_status']['extended_tweet']

			if ('extended_entities' in retweeted_status):
				del tweet['retweeted_status']['extended_entities']

			# format urls & user_mentions        
			if ('entities' in retweeted_status):
				entities = retweeted_status['entities']

				if ('urls' in entities):
					urls = []
					for url in  entities['urls']:
						if url['url'] != '':
							urls.append(url)

					tweet['retweeted_status']['entities']['urls'] = urls


				if ('user_mentions' in entities):
					user_ids = []
					for user in  entities['user_mentions']:
						user_ids.append(user['id'])

					tweet['retweeted_status']['entities']['user_mentions_ids'] = user_ids


		if ('quoted_status' in tweet):
			quoted_status = tweet['quoted_status']
			# format source
			if 'source' in quoted_status :
				source_url = source_name = ''
				source_info = quoted_status['source'].replace('<a href="', '')
				source_info = source_info.replace('" rel="nofollow"', '')
				source_info = source_info.replace('</a>', '')
				source_info = source_info.split('>')
				source_url, source_name = source_info[0], source_info[1]

				tweet['quoted_status']['source_url'] = source_url
				tweet['quoted_status']['source_name'] = source_name

			if ('extended_tweet' in quoted_status):
				del tweet['quoted_status']['extended_tweet']

			if ('extended_entities' in quoted_status):
				del tweet['quoted_status']['extended_entities']

			# format urls & user_mentions
			if ('entities' in quoted_status):
				entities = quoted_status['entities']

				if ('urls' in entities):
					urls = []
					for url in  entities['urls']:
						if url['url'] != '':
							urls.append(url)

					tweet['quoted_status']['entities']['urls'] = urls

				if ('user_mentions' in entities):
					user_ids = []
					for user in  entities['user_mentions']:
						user_ids.append(user['id'])

					tweet['quoted_status']['entities']['user_mentions_ids'] = user_ids

		return tweet


total_count = 1


# number of records per file
limit_num = 50000
# number of records that save to neo4j
#neo4j_num = 1000000
# extract number
extract_num = 1000000


file_name = str(time.time())

#connect neo4j
#graph = Graph("http://neo4j:123456@"+settings.NEO4J_IP+":7474")

#connect twitter api
auth = OAuthHandler(settings.CUSTOMER_KEY, settings.CUSTOMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

def save_message(message):
    with open(os.path.join(settings.DATA_DIR, 'Loop_message.txt'), 'a') as f:
        f.write(message)
        f.write('\n')

while True:
	save_message('Loop')

	if total_count > extract_num:
		break
	
	try:
		twitterStream = Stream(auth, MyStreamListener(limit_num, neo4j_num, extract_num))
		twitterStream.sample()
	except KeyboardInterrupt:
		save_message('Interrupt')
		# Or however you want to exit this loop
		twitterStream.disconnect()
		break
	except:
		save_message('disconnect')
		continue
