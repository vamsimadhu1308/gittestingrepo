import automaton.utility.elasticsearch.Util as util

# elb target GROUP DATA
query = {
    "size": 9000,

    "_source": {
        "excludes": ["vpc_id"]
    },
    "query": {
        "match_all": {}
    }
}
data = util.getESObject().getQueryResult(util.getESClient(), "esi_aws_service_synchronizer",
                                         "esm_elbv2_targetgroup_synchronizer", query)
hits = data['hits']['hits']
for hit in hits:
    hit['_index'] = "esi_elbv2_targetgroup_data"
    del hit["_id"]
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers

esClient = Elasticsearch(hosts=['http://18.208.92.240:9200'],
                         connection_class=RequestsHttpConnection)
response = helpers.bulk(esClient, hits)
print response
