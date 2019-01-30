import couchbase
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
import logging
import sys
import random
import string
import time

def cblogging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    couchbase.enable_logging()
    return


def cbclustersetup(serveraddress,password):
    cluster = Cluster(serveraddress)
    authenticator = PasswordAuthenticator('Administrator', password)
    cluster.authenticate(authenticator)
    return cluster


def upsertrepeater(bucket):
    keys = list(range(0, 10000))
    count = 0
    while True:
        start = time.time()
        for key in keys:
            value = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=64)))
            bucket.upsert(str(key), {'value': value})
            bucket.remove(str(key))
            # print('\r >>> Current key: {}   '.format(str(key)), ' Loop count', count, end='', flush=True)
        #print('Time taken to do', len(keys), 'key upserts:', time.time()-start, '-- iteration', count)
        print(time.time()-start)
        count += 1

def main():
    ip = 'http://127.0.0.1:8091/'
    password = 'asdfasdf'
    cluster = cbclustersetup(ip, password)
    bucket = cluster.open_bucket('test')

    try:
        upsertrepeater(bucket)
    except KeyboardInterrupt:
        print('upsert repeater interrupted')
        pass
    print('program exit normally')
    return


# cblogging()
main()