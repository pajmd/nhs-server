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
        pass
    else:
        field_value = []
        for k,v in req['fieldValues'].items():
            if v:
                field_value.append("{field}:{value}".format(field=k, value=v))
        req_str = "%20AND%20".join(field_value)
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