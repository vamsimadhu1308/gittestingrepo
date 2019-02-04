import automaton.utility.elasticsearch.Util as util

# ec2 DATA
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
                                         "esm_ec2_sg_synchronizer", query)
hits = data['hits']['hits']
for hit in hits:
    hit['_index'] = "esi_aws_service_synchronizer_basic_sg"
    hit["_source"]["sg_id"] = hit["_source"]["security_group_id"]
    del hit["_id"]
    del hit["_source"]["security_group_id"]
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers

esClient = Elasticsearch(hosts=['http://18.208.92.240:9200'],
                         connection_class=RequestsHttpConnection)
response = helpers.bulk(esClient, hits)
print response
