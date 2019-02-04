import automaton.utility.elasticsearch.Util as util
import copy

query = {
    "size": 9000,
    "query": {
        "match_all": {}
    }
}
data = util.getESObject().getQueryResult(util.getESClient(), "esi_aws_service_synchronizer", "esm_lambda_synchronizer",
                                         query)
# print data
hits = data['hits']['hits']
print "hits size"
print len(hits)
for item in hits:
    item['_source']['lambda_function_vpcconfig'] = {
        "subnetIds": [
            "subnet-0f99de6b",
            "subnet-866727cd"
        ],
        "securityGroupIds": [
            "sg-f114ee82"
        ]
    }
output = []
print hits[0]
for hit in hits:
    if "lambda_function_vpcconfig" in hit["_source"].keys():
        for entry in hit["_source"]["lambda_function_vpcconfig"]["securityGroupIds"]:
            innerjson = {}
            innerjson["_index"] = "esi_aws_service_synchronizer_relationship_sg_lambda"
            innerjson["_type"] = "esm_lambda_synchronizer"
            innerjson["_source"] = {}
            if "lambda_function_arn" in hit['_source']:
                innerjson["_source"]["lambda_function_arn"] = hit["_source"]["lambda_function_arn"]
            else:
                innerjson["_source"]["lambda_function_arn"] = hit["_source"]["lambda_function_name"]
            innerjson["_source"]["sg_id"] = entry
            output.append(innerjson)

from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers

esClient = Elasticsearch(hosts=['http://18.208.92.240:9200'],
                         connection_class=RequestsHttpConnection)
response = helpers.bulk(esClient, output)
print response
