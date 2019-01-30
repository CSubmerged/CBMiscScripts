import random

print(random.randint(0, 100))
import couchbase
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.views.params import Query
from couchbase.n1ql import N1QLQuery
import json
import logging
import sys
import requests


def cblogging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    couchbase.enable_logging()
    return


# cblogging()

cluster = Cluster('http://127.0.0.1:8091/')
authenticator = PasswordAuthenticator('Administrator', 'asdfasdf')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('test')
beer = cluster.open_bucket('beer-sample')
cb.upsert('u:king_arthur',
          {'name': 'Arthur', 'email': 'kingarthur@couchbase.com', 'interests': ['Holy Grail', 'African Swallows']})


r = requests.get('http://127.0.0.1:8091/pools/default/buckets/', auth=('Administrator', 'asdfasdf'))
print(r, r.text)
res = json.loads(r.text)
for a in range(len(res)):
    print(res[a]['name'])

# OperationResult<RC=0x0, Key=u'u:king_arthur', CAS=0xb1da029b0000>

# print(cb.get('u:king_arthur').value)
# # {u'interests': [u'Holy Grail', u'African Swallows'], u'name': u'Arthur', u'email': u'kingarthur@couchbase.com'}
#
# cb.upsert('key1',
#           {'name': 'Chris', 'email': 'go.away@gmail.com'})
#
# rv = cb.get('key1')
# print(rv.value)
#
# cb.upsert('key1',
#           {'name': 'Chris', 'email': ['go.away@gmail.com', 'christopherfarman@couchbase.com']})
#
# rv = cb.get('key1')
# print(rv.value)

#  #Brewery names beginning with C query
# q = Query()
# q.limit = 100
# q.mapkey_range = ('C','C'+Query.STRING_RANGE_END)
#
# query_result = beer.query('beername', 'Brewery Name', query=q)
# for row in query_result:
#     print(row)

# namelist = []
# query_result2 = beer.query('beername', 'Beer Name')
# for row in query_result2:
#     namelist.append(row.key)
# print(namelist[(random.randint(0, len(namelist)))])

# beer.n1ql_query('CREATE PRIMARY INDEX ON `beer-sample`').execute()
#
# row_rand = beer.n1ql_query(N1QLQuery('SELECT * FROM `beer-sample`'))
# for row in row_rand: print(row)

# travelsample = cluster.open_bucket('travel-sample')
# print(travelsample.get('airline_10').value)
# query = N1QLQuery("SELECT airportname, city, country FROM 'travel-sample "
#                   "WHERE type=\"airport\" AND city=$my_city", my_city="Reno")
# res = travelsample.n1ql_query(query)
# print(res)
# for row in res:
#     print(row)

# cb.n1ql_query('CREATE PRIMARY INDEX ON `test`').execute()
#
# row_iter = cb.n1ql_query(N1QLQuery('SELECT name FROM `test` WHERE ' + \
#                                    '$1 IN interests', 'African Swallows'))
# for row in row_iter: print(row)
# # {u'name': u'Arthur'}
