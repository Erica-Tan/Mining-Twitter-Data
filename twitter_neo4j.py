import json
import ast
import os
import settings
from py2neo import Graph, authenticate
 
#Property values can only be of primitive types or arrays thereof
 
 
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

# connect neo4j
graph = Graph("http://neo4j:123456@"+settings.NEO4J_IP+":7474")

with open('filename.txt') as data_file:
    filenames = ast.literal_eval(data_file.readline())
    
for filename in filenames:
    with open(os.path.join(settings.DATA_DIR, 'twitter'+filename+'.json')) as data_file:
        tweet = json.load(data_file)


    # Send Cypher query.
    graph.run(query, json = tweet)
    #graph.run(query, json = tweet).dump()





query1 = """
UNWIND {json} AS t


WITH t
MATCH (tweet1:Tweet {id:t.quoted_status.id})
WITH t, tweet1
MATCH (user1:User)
WHERE user1.id IN t.quoted_status.entities.user_mentions_ids
MERGE (tweet1)-[:MENTIONS]->(user1)
"""


query2="""
UNWIND {json} AS t

WITH t
MATCH (tweet1:Tweet {id:t.quoted_status.id})
WITH t, tweet1
MATCH (rtweet1:Tweet {id:t.quoted_status.in_reply_to_status_id})
MERGE (tweet1)-[:PRPLYTO]->(rtweet1)
"""
query3="""
UNWIND {json} AS t

WITH t
MATCH (tweet:Tweet {id:t.retweeted_status.id})
WITH t, tweet
MATCH (user:User)
WHERE user.id IN t.retweeted_status.entities.user_mentions_ids
MERGE (tweet)-[:MENTIONS]->(user)
"""

query4="""
UNWIND {json} AS t

WITH t
MATCH (tweet:Tweet {id:t.retweeted_status.id})
WITH t, tweet
MATCH (rtweet:Tweet {id:t.retweeted_status.in_reply_to_status_id})
MERGE (tweet)-[:PRPLYTO]->(rtweet)
"""

'''
with open('data/twitter6.json') as data_file:
    tweet = json.load(data_file)


# Send Cypher query.
graph.run(query, json = tweet)
graph.run(query1, json = tweet)
graph.run(query2, json = tweet)
graph.run(query3, json = tweet)
graph.run(query4, json = tweet)
'''









