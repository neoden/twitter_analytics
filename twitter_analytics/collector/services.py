import logging

import tweepy
from django.db import transaction
from django.db.models import Max

from . import models

log = logging.getLogger(__name__)


class TweetCollectorService:
    def __init__(self, api_key, api_secret_key, query_phrase, num_tweets_to_fetch):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.query_phrase = query_phrase
        self.num_tweets_to_fetch = num_tweets_to_fetch

    def get_api(self):
        auth = tweepy.AppAuthHandler(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret_key
        )
        api = tweepy.API(auth)
        return api

    @transaction.atomic
    def collect(self):
        api = self.get_api()

        since_id = models.Tweet.objects.all().aggregate(Max('id'))['id__max']
        search_results = api.search(
            q=self.query_phrase,
            result_type='recent',
            count=self.num_tweets_to_fetch,
            since_id=since_id
        )

        for status in search_results:
            tweet, created = models.Tweet.objects.get_or_create(
                id=status.id,
                published_at=status.created_at,
                phrase=status.text,
                author_id=status.author.id,
                author_name=status.author.screen_name
            )
            if created:
                for entry in status.entities.get('hashtags', []):
                    hashtag = entry['text']
                    models.TweetHashtag.objects.get_or_create(
                        tweet=tweet,
                        hashtag=hashtag
                    )
                log.info(f'Created: {tweet}')

            models.TweetQueryPhrase.objects.get_or_create(
                tweet=tweet,
                query_phrase=self.query_phrase
            )
