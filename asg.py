import automaton.utility.elasticsearch.Util as util

# AUTO SCALING GROUP DATA
query = {
    "size": 9000,
    "_source": {
        "excludes": ["vpc_id", "autoscaling_group_vpc_zone_identifier"]
    },
    "query": {
        "match_all": {}
    }
}
data = util.getESObject().getQueryResult(util.getESClient(), "esi_aws_service_synchronizer",
                                         "esm_autoscaling_synchronizer", query)
hits = data['hits']['hits']
for hit in hits:
    hit['_index'] = "esi_asg_data"
    del hit["_id"]
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers

esClient = Elasticsearch(hosts=['http://18.208.92.240:9200'],
                         connection_class=RequestsHttpConnection)
response = helpers.bulk(esClient, hits)
print response
