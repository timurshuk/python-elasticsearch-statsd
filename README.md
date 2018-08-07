# python-elasticsearch-statsd

Wrapper for elasticsearch client that send metrics to StatsD

## Installation

1. Clone this repository
2. `pip3 install .`

## Example use

```
from elasticsearch_statsd import ElasticsearchStatsD
es = ElasticsearchStatsD()
es.search()
```


