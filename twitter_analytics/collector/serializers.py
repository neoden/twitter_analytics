from rest_framework.serializers import ModelSerializer

from . import models


class QueryPhraseSerializer(ModelSerializer):
    class Meta:
        model = models.TweetQueryPhrase
        fields = [
            'query_phrase'
        ]

    def to_representation(self, instance):
        return instance.query_phrase


class HashtagSerializer(ModelSerializer):
    class Meta:
        model = models.TweetHashtag
        fields = [
            'hashtag'
        ]

    def to_representation(self, instance):
        return instance.hashtag


class TweetSerializer(ModelSerializer):
    query_phrases = QueryPhraseSerializer(many=True)
    hashtags = HashtagSerializer(many=True)

    class Meta:
        model = models.Tweet
        fields = [
            'id',
            'published_at',
            'phrase',
            'hashtags',
            'author_id',
            'author_name',
            'query_phrases'
        ]
