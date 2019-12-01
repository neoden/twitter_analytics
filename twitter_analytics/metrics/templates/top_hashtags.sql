SELECT
    t2.hashtag,
    t2.query_phrase,
    t2.num_tweets
FROM
    (SELECT
        t1.hashtag,
        t1.query_phrase,
        t1.num_tweets,
        ROW_NUMBER() OVER (
            PARTITION BY query_phrase
            ORDER BY num_tweets desc
        ) AS row
    FROM
        (SELECT
            LOWER(h.hashtag) AS hashtag,
            q.query_phrase,
            COUNT(t.id) AS num_tweets
        FROM
            collector_tweet t
            INNER JOIN collector_tweethashtag h ON h.tweet_id = t.id
            INNER JOIN collector_tweetqueryphrase q ON q.tweet_id = t.id
        WHERE
            1 = 1
            {{ filters|safe }}
        GROUP BY
            LOWER(h.hashtag),
            q.query_phrase
        ) t1
    ) t2
WHERE
    t2.row <= %(num_top_rows)s
