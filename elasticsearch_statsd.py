from elasticsearch import Elasticsearch
from datadog import statsd, initialize
from functools import wraps
import inspect


class ElasticsearchStatsD:
    def __init__(self, namespace, *args, **kwargs):
        if 'statsd_host' not in kwargs:
            raise ValueError('statsd_host must be set')

        if 'statsd_port' not in kwargs:
            raise ValueError('statsd_port must be set')

        initialize(
            statsd_host=kwargs['statsd_host'],
            statsd_port=kwargs['statsd_port']
        )
        statsd.namespace = namespace

        del kwargs['statsd_host'], kwargs['statsd_port']

        self.__es = Elasticsearch(*args, **kwargs)

    def __getattr__(self, attr):
        es_attr = getattr(self.__es, attr)

        if not inspect.ismethod(es_attr):
            return es_attr

        @wraps(es_attr)
        def wrapper(*args, **kwargs):

            tags = {'operation': attr}
            if 'index' in kwargs:
                tags['index'] = kwargs['index']

            with statsd.timed(
                    'elasticsearch',
                    tags=self.__prepare_tags(tags),
                    use_ms=True
            ):
                return es_attr(*args, **kwargs)

        return wrapper

    @staticmethod
    def __prepare_tags(tags):
        return ['{}:{}'.format(k, v) for k, v in tags.items()]
