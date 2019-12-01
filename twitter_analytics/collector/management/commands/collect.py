import os

from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured

from twitter_analytics.collector.services import TweetCollectorService


class Command(BaseCommand):
    help = 'Fetch latest tweets'

    MAX_SEARCH_QUERY_LENGTH = 500
    REQUIRED_SETTINGS = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET_KEY',
        'QUERY_PHRASE',
        'NUM_TWEETS_TO_FETCH'
    ]

    def __init__(self):
        self.config = {}
        self.configure()

    def configure(self):
        missing_settings = []

        for setting_name in self.REQUIRED_SETTINGS:
            setting_value = os.getenv(setting_name)
            if setting_value:
                self.config[setting_name] = setting_value
            else:
                missing_settings.append(setting_name)

        if missing_settings:
            raise ImproperlyConfigured(
                f'Required settings not configured: {missing_settings.join(", ")}'
            )

        # check QUERY_PHRASE length
        if len(self.config['QUERY_PHRASE']) > self.MAX_SEARCH_QUERY_LENGTH:
            raise ImproperlyConfigured(
                f'QUERY_PHRASE exceeds limit ({self.MAX_SEARCH_QUERY_LENGTH})'
            )

        # convert NUM_TWEETS_TO_FETCH to number
        try:
            self.config['NUM_TWEETS_TO_FETCH'] = int(self.config['NUM_TWEETS_TO_FETCH'])
        except ValueError:
            raise ImproperlyConfigured(
                f'NUM_TWEETS_TO_FETCH value is invalid: {self.config["NUM_TWEETS_TO_FETCH"]}'
            )

    def handle(self, **options):
        service = TweetCollectorService(
            api_key=self.config['TWITTER_API_KEY'],
            api_secret_key=self.config['TWITTER_API_SECRET_KEY'],
            query_phrase=self.config['QUERY_PHRASE'],
            num_tweets_to_fetch=self.config['NUM_TWEETS_TO_FETCH']
        )
        service.collect()
