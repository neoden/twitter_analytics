SELECT
    q.query_phrase,
    COUNT(tweet_id) num_tweets
FROM
    collector_tweet t
    INNER JOIN collector_tweetqueryphrase q ON q.tweet_id = t.id
WHERE
    1 = 1
    {{ filters|safe }}
GROUP BY
    q.query_phrase
