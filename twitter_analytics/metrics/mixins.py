from django.db import connection
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

from .utils import dictfetchall


class MetricViewMixin:
    def get_response(self, request, template_name, additional_execute_params=None):
        params = request.query_params
        filters = []
        execute_params = {}

        if additional_execute_params:
            execute_params.update(additional_execute_params)

        if 'start_dt' in params:
            start_dt = parse_datetime(params['start_dt'])
            filters.append('AND published_at >= %(start_dt)s')
            execute_params['start_dt'] = start_dt

        if 'end_dt' in params:
            end_dt = parse_datetime(params['end_dt'])
            filters.append('AND published_at <= %(end_dt)s')
            execute_params['end_dt'] = end_dt

        if 'query_phrase' in params:
            query_phrase = params['query_phrase'].lower()
            filters.append('AND lower(query_phrase) = %(query_phrase)s')
            execute_params['query_phrase'] = query_phrase

        query = render_to_string(
            template_name,
            {'filters': '\n'.join(filters)}
        )

        with connection.cursor() as cursor:
            cursor.execute(query, execute_params)
            result = dictfetchall(cursor)

        return JsonResponse(result, safe=False)
