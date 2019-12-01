from rest_framework.views import APIView

from .mixins import MetricViewMixin


class HashtagStatsView(MetricViewMixin, APIView):
    paginator = None

    NUM_TOP_ROWS = 3

    def get(self, request, *args, **kwargs):
        return self.get_response(
            request,
            'top_hashtags.sql',
            {'num_top_rows': self.NUM_TOP_ROWS}
        )


class AuthorStatsView(MetricViewMixin, APIView):
    paginator = None

    NUM_TOP_ROWS = 3

    def get(self, request, *args, **kwargs):
        return self.get_response(
            request,
            'top_authors.sql',
            {'num_top_rows': self.NUM_TOP_ROWS}
        )


class AmountStatsView(MetricViewMixin, APIView):
    paginator = None

    def get(self, request, *args, **kwargs):
        return self.get_response(request, 'amount.sql')
