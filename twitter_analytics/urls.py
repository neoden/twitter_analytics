from django.urls import path

import twitter_analytics.collector.views
import twitter_analytics.metrics.views


urlpatterns = [
    path(
        'api/tweets/',
        twitter_analytics.collector.views.TweetsView.as_view(),
        name='tweets'
    ),
    path(
        'api/analytics/top_hashtags/',
        twitter_analytics.metrics.views.HashtagStatsView.as_view(),
        name='top_hashtags'
    ),
    path(
        'api/analytics/top_authors/',
        twitter_analytics.metrics.views.AuthorStatsView.as_view(),
        name='top_authors'
    ),
    path(
        'api/analytics/amount/',
        twitter_analytics.metrics.views.AmountStatsView.as_view(),
        name='amount'
    )
]
