import requests
from app.solr.solrconfig import get_solr_query, get_url


# wild request to return everything in the collection
# http://localhost:8983/solr/nhsCollection/select?q=*:*&rows=100
# same as above but we only want returned the "medicine" field:
#   http://localhost:8983/solr/nhsCollection/select?fl=Medicine&q=*:*&rows=100
# search for which the value contains spaces
# http://localhost:8983/solr/nhsCollection/select?q=Medicine:Acetylcysteine+10%25+eye+drops
# Search on full word (token)
# http://localhost:8983/solr/nhsCollection/select?q=Medicine:Acetylcysteine
# Search field are key sensitive
# Here field contains spaces
# http://localhost:8983/solr/nhsCollection/select?q=Pack\%20Size:5
# http://localhost:8983/solr/nhsCollection/select?q=Medicine:Acetylcysteine&period:December
#
# "5%  drops"~10  - 5% and drop less than 10 words away
# http://localhost:8983/solr/nhsCollection/select?q=%225%25%20%20drops%22~10
#
# search something containing ser and op
# http://localhost:8983/solr/nhsCollection/select?q=%2Aser%2A%20AND%20%2Aop%2A&rows=10000
# http://localhost:8983/solr/nhsCollection/select?q=*ser*%20AND%20*op*&rows=10

def build_free_text_search_payload(free_search_text):
    tokens = free_search_text.split(' ')
    star_tokens = ["*%s*" % token for token in tokens]
    return "%20AND%20".join(star_tokens)


def build_field_search_payload(field_values):
    field_value_list = []
    for k, v in field_values.items():
        if v:
            field_value_list.append("{field}:{value}".format(field=k, value=v))
    return "%20AND%20".join(field_value_list)

def solr_search(req):
    # fieldValues: {
    #     name: "",
    #     price: "",
    #     category: "",
    #     code: "",
    #     period: "",
    #     quantity: "",
    #     unit: "",
    #     [free_search]: ""
    # }
    if req['fieldValues']["Free Search"]:
        req_str = build_free_text_search_payload(req['fieldValues']["Free Search"])
    else:
        req_str = build_field_search_payload(req['fieldValues'])

    solr_request = get_solr_query(req_str)
    r = requests.get(solr_request)
    # params = dict()
    # for k,v in req['fieldValues'].items():
    #     if v:
    #         params[k] = v
    # r = requests.get(url=get_url(), params=params)
    print("requesting solr: %s" % r.url)
    r.raise_for_status()
    return r.json()