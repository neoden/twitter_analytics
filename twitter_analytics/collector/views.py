from django_filters import rest_framework as filters
from rest_framework import generics

from .models import Tweet
from .serializers import TweetSerializer


class TweetFilter(filters.FilterSet):
    start_dt = filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    end_dt = filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')
    query_phrase = filters.CharFilter(
        field_name='query_phrases__query_phrase', lookup_expr='icontains'
    )

    class Meta:
        model = Tweet
        fields = ['start_dt', 'end_dt', 'query_phrase']


class TweetsView(generics.ListAPIView):
    queryset = Tweet.objects.all().prefetch_related('query_phrases')
    serializer_class = TweetSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TweetFilter
