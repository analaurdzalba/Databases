
-- Queries Jesús Lopez 
--1
SELECT COUNT(u.id)
FROM USERS u, HASHTAGS h 
WHERE h.hashtag = 'LoL'
AND u.followers_count > 100000
--2
SELECT COUNT(*) as Hashtags
FROM HASHTAGS h, TWEETS t, PLACES p 
WHERE t.id = h.tweet_id
AND p.id = t.place_id
AND h.hashtag = 'LoL'
--3
SELECT u.id
FROM MENTIONS m, USERS u, HASHTAGS h
WHERE m.mention = 'Youtube'
AND h.hashtag = 'LoL'

-- Queries Rafael Aguirre
--1
SELECT t.tweet_text
FROM TWEETS t, HASHTAGS h 
WHERE h.tweet_id = t.id
AND h.hashtag = 'NBA'
AND t.retweet_count = 0
--2 
SELECT COUNT(*) as Hashtags
FROM HASHTAGS h, TWEETS t, PLACES p 
WHERE t.id = h.tweet_id
AND p.id = t.place_id
AND p.country_code = 'US'
AND h.hashtag = 'NBA'
--3
SELECT COUNT(u.id) as IDs
FROM USERS u, HASHTAGS h 
WHERE h.hashtag = 'nba'
AND u.followers_count > 100000

-- Queries Ana Laura Rodríguez
--1
SELECT COUNT(u.id) AS [Cantidad de Usuarios]
FROM USERS u, TWEETS t, HASHTAGS h 
WHERE t.id = h.tweet_id
AND u.verified = 0
AND h.hashtag = 'HarryStyles'
--2
SELECT u.id
FROM USERS u, TWEETS t, PLACES p 
WHERE u.id = t.[user] 
AND t.place_id = p.id
AND p.country_code != 'US' 
--3
SELECT p.name
FROM PLACES p, TWEETS t, HASHTAGS h 
WHERE p.id = t.place_id
AND t.id = h.tweet_id
AND h.hashtag = null

-- Queries Diego Samano
--1
SELECT u.id
FROM USERS u, TWEETS t, HASHTAGS h 
WHERE t.id = h.tweet_id
AND u.verified = 0
AND h.hashtag = 'nflseason'
--2
SELECT t.id, t.tweet_text
FROM TWEETS t, HASHTAGS h 
WHERE h.tweet_id = t.id
AND t.retweet_count = 0
--3
SELECT DISTINCT( t.[user]) as [MOST MENTIONED USER ID], m.mention as USERNAME
FROM TWEETS t, MENTIONS m, USERS u
WHERE t.id = m.tweet_id
AND u.id = t.[user]
AND m.mention = (
    SELECT MAX(mention)
    FROM MENTIONS
)



