import json
import time
import os
import settings
from py2neo import Graph, authenticate
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


query = """
UNWIND {json} AS t
MERGE (tweet:Tweet {id:t.id}) ON CREATE
SET tweet.created_at = t.created_at,
tweet.text = t.text,
tweet.truncated = t.truncated,
tweet.retweet_count = t.retweet_count,
tweet.favorite_count = t.favorite_count,
tweet.favorited = t.favorited,
tweet.retweeted = t.retweeted,
tweet.filter_level = t.filter_level,
tweet.lang = t.lang,
tweet.possibly_sensitive = t.possibly_sensitive

MERGE (user:User {id:t.user.id}) ON CREATE
SET user.name = t.user.name,
user.screen_name = t.user.screen_name,
user.location = t.user.location,
user.url = t.user.url,
user.description = t.user.description,
user.protected = t.user.protected,
user.verified = t.user.verified,
user.followers_count = t.user.followers_count,
user.friends_count = t.user.friends_count,
user.listed_count = t.user.listed_count,
user.favourites_count = t.user.favourites_count,
user.statuses_count = t.user.statuses_count,
user.created_at = t.user.created_at,
user.utc_offset = t.user.utc_offset,
user.time_zone = t.user.time_zone,
user.geo_enabled = t.user.geo_enabled,
user.lang = t.user.lang,
user.contributors_enabled = t.user.contributors_enabled,
user.is_translator = t.user.is_translator,
user.profile_background_color = t.user.profile_background_color,
user.profile_background_image_url = t.user.profile_background_image_url,
user.profile_background_image_url_https = t.user.profile_background_image_url_https,
user.profile_background_tile = t.user.profile_background_tile,
user.profile_link_color = t.user.profile_link_color,
user.profile_sidebar_border_color = t.user.profile_sidebar_border_color,
user.profile_sidebar_fill_color = t.user.profile_sidebar_fill_color,
user.profile_text_color = t.user.profile_text_color,
user.profile_use_background_image = t.user.profile_use_background_image,
user.profile_image_url = t.user.profile_image_url,
user.profile_image_url_https = t.user.profile_image_url_https,
user.profile_banner_url = t.user.profile_banner_url,
user.default_profile = t.user.default_profile,
user.default_profile_image = t.user.default_profile_image,
user.following = t.user.following,
user.follow_request_sent = t.user.follow_request_sent,
user.notifications = t.user.notifications
MERGE (user)-[:POSTS]->(tweet)



FOREACH (s IN (CASE WHEN t.source_name = '' THEN [] ELSE [t.source_name] END ) |
    MERGE (source:Source {name:s}) ON CREATE
    SET source.url = t.source_url
    MERGE (tweet)-[:USING]->(source)
)


FOREACH (p IN t.place |
    MERGE (place:Place {id:p.id}) ON CREATE
    SET place.url = p.url,
    place.place_type = p.place_type,
    place.name = p.name,
    place.full_name = p.full_name,
    place.country_code = p.country_code,
    place.country = p.country
    MERGE (place)-[:PLACES]->(tweet)
)


FOREACH (h IN t.entities.hashtags |
    MERGE (tag:Hashtag {name:LOWER(h.text)})
    MERGE (tag)-[:TAGS]->(tweet)
)


FOREACH (l IN t.entities.urls |
    FOREACH(value IN (CASE WHEN l.url = '' THEN [] ELSE [l.url] END) |
        MERGE (link:Link {url:l.url}) ON CREATE 
        SET link.expanded_url = l.expanded_url,
        link.display_url = l.display_url
        MERGE (tweet)-[:CONTAINS]->(link)
    )
)



FOREACH (qt IN t.quoted_status |
    MERGE (qtweet:Tweet {id:qt.id}) ON CREATE
    SET qtweet.created_at = qt.created_at,
    qtweet.text = qt.text,
    qtweet.truncated = qt.truncated,
    qtweet.retweet_count = qt.retweet_count,
    qtweet.favorite_count = qt.favorite_count,
    qtweet.favorited = qt.favorited,
    qtweet.retweeted = qt.retweeted,
    qtweet.filter_level = qt.filter_level,
    qtweet.lang = qt.lang,
    qtweet.possibly_sensitive = qt.possibly_sensitive
    MERGE (tweet)-[:QUOTES]->(qtweet)

    MERGE (quser:User {id:qt.user.id}) ON CREATE
    SET quser.name = qt.user.name,
    quser.screen_name = qt.user.screen_name,
    quser.location = qt.user.location,
    quser.url = qt.user.url,
    quser.description = qt.user.description,
    quser.protected = qt.user.protected,
    quser.verified = qt.user.verified,
    quser.followers_count = qt.user.followers_count,
    quser.friends_count = qt.user.friends_count,
    quser.listed_count = qt.user.listed_count,
    quser.favourites_count = qt.user.favourites_count,
    quser.statuses_count = qt.user.statuses_count,
    quser.created_at = qt.user.created_at,
    quser.utc_offset = qt.user.utc_offset,
    quser.time_zone = qt.user.time_zone,
    quser.geo_enabled = qt.user.geo_enabled,
    quser.lang = qt.user.lang,
    quser.contributors_enabled = qt.user.contributors_enabled,
    quser.is_translator = qt.user.is_translator,
    quser.profile_background_color = qt.user.profile_background_color,
    quser.profile_background_image_url = qt.user.profile_background_image_url,
    quser.profile_background_image_url_https = qt.user.profile_background_image_url_https,
    quser.profile_background_tile = qt.user.profile_background_tile,
    quser.profile_link_color = qt.user.profile_link_color,
    quser.profile_sidebar_border_color = qt.user.profile_sidebar_border_color,
    quser.profile_sidebar_fill_color = qt.user.profile_sidebar_fill_color,
    quser.profile_text_color = qt.user.profile_text_color,
    quser.profile_use_background_image = qt.user.profile_use_background_image,
    quser.profile_image_url = qt.user.profile_image_url,
    quser.profile_image_url_https = qt.user.profile_image_url_https,
    quser.profile_banner_url = qt.user.profile_banner_url,
    quser.default_profile = qt.user.default_profile,
    quser.default_profile_image = qt.user.default_profile_image,
    quser.following = qt.user.following,
    quser.follow_request_sent = qt.user.follow_request_sent,
    quser.notifications = qt.user.notifications
    MERGE (quser)-[:POSTS]->(qtweet)



    FOREACH (s IN (CASE WHEN qt.source_name = '' THEN [] ELSE [qt.source_name] END ) |
        MERGE (qsource:Source {name:s}) ON CREATE
        SET qsource.url = qt.source_url
        MERGE (tweet)-[:USING]->(qsource)
    )


    FOREACH (p IN qt.place |
        MERGE (qplace:Place {id:p.id}) ON CREATE
        SET qplace.url = p.url,
        qplace.place_type = p.place_type,
        qplace.name = p.name,
        qplace.full_name = p.full_name,
        qplace.country_code = p.country_code,
        qplace.country = p.country
        MERGE (qplace)-[:PLACES]->(tweet)
    )


    FOREACH (h IN qt.entities.hashtags |
        MERGE (qtag:Hashtag {name:LOWER(h.text)})
        MERGE (qtag)-[:TAGS]->(tweet)
    )


    FOREACH (l IN qt.entities.urls |
        FOREACH(value IN (CASE WHEN l.url = '' THEN [] ELSE [l.url] END) |
            MERGE (qlink:Link {url:l.url}) ON CREATE 
            SET qlink.expanded_url = l.expanded_url,
            qlink.display_url = l.display_url
            MERGE (tweet)-[:CONTAINS]->(qlink)
        )
    )


)




FOREACH (rt IN t.retweeted_status |
    MERGE (rtweet:Tweet {id:rt.id}) ON CREATE
    SET rtweet.created_at = rt.created_at,
    rtweet.text = rt.text,
    rtweet.truncated = rt.truncated,
    rtweet.retweet_count = rt.retweet_count,
    rtweet.favorite_count = rt.favorite_count,
    rtweet.favorited = rt.favorited,
    rtweet.retweeted = rt.retweeted,
    rtweet.filter_level = rt.filter_level,
    rtweet.lang = rt.lang,
    rtweet.possibly_sensitive = rt.possibly_sensitive
    MERGE (tweet)-[:RETWEETS]->(rtweet)

    MERGE (ruser:User {id:rt.user.id}) ON CREATE
    SET ruser.name = rt.user.name,
    ruser.screen_name = rt.user.screen_name,
    ruser.location = rt.user.location,
    ruser.url = rt.user.url,
    ruser.description = rt.user.description,
    ruser.protected = rt.user.protected,
    ruser.verified = rt.user.verified,
    ruser.followers_count = rt.user.followers_count,
    ruser.friends_count = rt.user.friends_count,
    ruser.listed_count = rt.user.listed_count,
    ruser.favourites_count = rt.user.favourites_count,
    ruser.statuses_count = rt.user.statuses_count,
    ruser.created_at = rt.user.created_at,
    ruser.utc_offset = rt.user.utc_offset,
    ruser.time_zone = rt.user.time_zone,
    ruser.geo_enabled = rt.user.geo_enabled,
    ruser.lang = rt.user.lang,
    ruser.contributors_enabled = rt.user.contributors_enabled,
    ruser.is_translator = rt.user.is_translator,
    ruser.profile_background_color = rt.user.profile_background_color,
    ruser.profile_background_image_url = rt.user.profile_background_image_url,
    ruser.profile_background_image_url_https = rt.user.profile_background_image_url_https,
    ruser.profile_background_tile = rt.user.profile_background_tile,
    ruser.profile_link_color = rt.user.profile_link_color,
    ruser.profile_sidebar_border_color = rt.user.profile_sidebar_border_color,
    ruser.profile_sidebar_fill_color = rt.user.profile_sidebar_fill_color,
    ruser.profile_text_color = rt.user.profile_text_color,
    ruser.profile_use_background_image = rt.user.profile_use_background_image,
    ruser.profile_image_url = rt.user.profile_image_url,
    ruser.profile_image_url_https = rt.user.profile_image_url_https,
    ruser.profile_banner_url = rt.user.profile_banner_url,
    ruser.default_profile = rt.user.default_profile,
    ruser.default_profile_image = rt.user.default_profile_image,
    ruser.following = rt.user.following,
    ruser.follow_request_sent = rt.user.follow_request_sent,
    ruser.notifications = rt.user.notifications
    MERGE (ruser)-[:POSTS]->(rtweet)


    FOREACH (s IN (CASE WHEN rt.source_name = '' THEN [] ELSE [rt.source_name] END ) |
        MERGE (rsource:Source {name:s}) ON CREATE
        SET rsource.url = rt.source_url
        MERGE (tweet)-[:USING]->(rsource)
    )



    FOREACH (p IN rt.place |
        MERGE (rplace:Place {id:p.id}) ON CREATE
        SET rplace.url = p.url,
        rplace.place_type = p.place_type,
        rplace.name = p.name,
        rplace.full_name = p.full_name,
        rplace.country_code = p.country_code,
        rplace.country = p.country
        MERGE (rplace)-[:PLACES]->(tweet)
    )


    FOREACH (h IN rt.entities.hashtags |
        MERGE (rtag:Hashtag {name:LOWER(h.text)})
        MERGE (rtag)-[:TAGS]->(tweet)
    )


    FOREACH (l IN rt.entities.urls |
        FOREACH(value IN (CASE WHEN l.url = '' THEN [] ELSE [l.url] END) |
            MERGE (rlink:Link {url:l.url}) ON CREATE 
            SET rlink.expanded_url = l.expanded_url,
            rlink.display_url = l.display_url
            MERGE (tweet)-[:CONTAINS]->(rlink)
        )
    )
)


WITH t, tweet
MATCH (muser:User)
WHERE muser.id IN t.entities.user_mentions_ids
MERGE (tweet)-[:MENTIONS]->(muser)

WITH t, tweet
MATCH (rptweet:Tweet {id:t.in_reply_to_status_id})
MERGE (tweet)-[:PRPLYTO]->(rptweet)

"""




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

			if total_count <= self.neo4j_num:
				#save data to neo4j
				graph.run(query, json = tweet)

			if total_count > self.extract_num:
				return False

			# format json
			if total_count == 1:
			       self.format_json(file_name, '[')

			       self.save_file_name(file_name)
			       
			

			# if it is the last record, no comma at the end
			if_last_record = divmod(total_count, self.limit_num)[1] == 0


			#print (json.dumps(tweet))


			with open(os.path.join(settings.DATA_DIR, 'twitter'+file_name+'.json'), 'a') as f:
				f.write(json.dumps(tweet))
				if if_last_record == False:
					f.write(',')
					f.write('\n')


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

'''
# number of records per file
limit_num = 20000
# number of records that save to neo4j
neo4j_num = 1000000
# extract number
extract_num = 2000000
'''

file_name = str(time.time())

#connect neo4j
graph = Graph("http://neo4j:123456@"+settings.NEO4J_IP+":7474")

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


	
