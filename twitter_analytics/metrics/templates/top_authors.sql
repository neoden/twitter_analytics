SELECT
    t2.author_name,
    t2.query_phrase,
    t2.num_tweets
FROM
    (SELECT
        t1.author_name,
        t1.query_phrase,
        t1.num_tweets,
        ROW_NUMBER() OVER (
            PARTITION BY query_phrase
            ORDER BY num_tweets desc
        ) AS row
    FROM
        (SELECT
            t.author_name,
            q.query_phrase,
            COUNT(t.id) AS num_tweets
        FROM
            collector_tweet t
            INNER JOIN collector_tweetqueryphrase q ON q.tweet_id = t.id
        WHERE
            1 = 1
            {{ filters|safe }}
        GROUP BY
            t.author_name,
            q.query_phrase
        ) t1
    ) t2
WHERE
    t2.row <= %(num_top_rows)s
