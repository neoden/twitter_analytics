from django.db import models


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    published_at = models.DateTimeField()
    phrase = models.TextField()
    author_id = models.BigIntegerField()
    author_name = models.TextField()

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['published_at'])
        ]


class TweetQueryPhrase(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='query_phrases')
    query_phrase = models.TextField()


class TweetHashtag(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='hashtags')
    hashtag = models.TextField()
