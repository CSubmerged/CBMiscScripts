# Server and Bucket creation script for Couchbase Server
# Written in the first few weeks, by Chris F

import csv
import random
import string
import requests
import json
import time
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase import exceptions
from couchbase.admin import Admin
import couchbase.subdocument as SD

def main():
    # >>> Variables to define server details <<<
    url = 'http://127.0.0.1:9000/'
    port = 0
    if url.find('8091') != -1:
        port += 8091
    elif url.find('9000') != -1:
        port += 9000
    else:
        print("Could not find port in url, setting as 0")
    username = 'Administrator'
    password = 'password'
    target_bucket = 'test'

    # >>> Server setup functions <<<
    selection = input_looper("Would you like to initiate a new server? y/n: ", ['y', 'n'])
    if selection == 'y':
        init_new_server(url, target_bucket, username, password, port)

    # >>> Initiate cluster, authenticate and open bucket <<<
    cluster = Cluster(url)
    authenticator = PasswordAuthenticator(username, password)
    cluster.authenticate(authenticator)
    bucket1 = cluster.open_bucket(target_bucket)

    # >>> Choose fill method <<<
    choice = input_looper("Please choose a fill option: "
                          "1) Pokedex, 2) Random, 3) Forever, 4) Reset/Clear, 5) Read, 6) xattr test : ",
                          ['1', '2', '3', '4', '5', '6'])
    if choice == '1':
        pokedex_fill(bucket1)
    elif choice == '2':
        random_fill(bucket1)
    elif choice == '3':
        forever_fill(bucket1)
    elif choice == '4':
        reset_bucket(bucket1)
    elif choice == '5':
        read_me(bucket1)
    elif choice == '6':
        xattr_add(bucket1)
    else:
        print('Bucket not filled')

    print("Cluster created, Bucket Booted and we're ready to rumble! :)")
    return


def pokedex_fill(input_bucket):
    # Simple pokedex with ID, name and type(s)
    poke_table = open('/Users/christopherfarman/dev/PokemonListByNumber.csv')
    csv_poke_table = csv.reader(poke_table)

    for row in csv_poke_table:
        if row[0] != ' Ndex':
            ndex = row[0].replace('#', '').strip()
            ndex = ndex.lstrip('0')
            if row[3] == '':
                type_entry = row[2]
            else:
                type_entry = [row[2], row[3]]
            input_bucket.upsert(ndex,
                                {'NDex': row[0].strip(),
                                 'Name': row[1],
                                 'Type': type_entry
                                 },
                                0,   # cas
                                10)  # TTL

    print("Completed Pokedex fill")
    return


def random_fill(input_bucket):
    number_of_elements = 100000
    start_time = time.time()
    for i in range(1, number_of_elements + 1):
        a = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=100)))
        b = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=100)))
        c = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=100)))
        input_bucket.upsert(str(i), {'a': a, 'b': b, 'c': c})
        print('\r >>> Current progress: {}   '.format(str(i)), end='', flush=True)
    print('\r Completed Random fill in', (time.time() - start_time), 's')
    return


def forever_fill(input_bucket):
    i = 0
    output = ""
    output.zfill(100000)
    while True:
        try:
            input_bucket.upsert(("item" + str(i)), output, 0, 2)
            i = i + 1
        except KeyboardInterrupt:
            return
        except:
            continue
    return


def reset_bucket(input_bucket):
    for i in range(100001):
        print('\r >>> Current progress: {}   '.format(str(i)), end='', flush=True)
        try:
            input_bucket.remove(str(i))
        except exceptions.NotFoundError:
            continue
    print('\r Completed Remove')
    return


def read_me(input_bucket):
    read_list = []
    i = 0
    while True:
        i += 1
        print('\r >>> Current progress: {}   '.format(str(i)), end='', flush=True)
        try:
            read_list.append(input_bucket.get("item" + str(i)))
        except exceptions.NotFoundError:
            continue
        except KeyboardInterrupt:
            break
    print('\r Completed read:', read_list)
    return


def xattr_add(cb):
    ogkey = 'test_doc'
    docBody = '{"a":3434}'
    xattrPath = '_sync'
    xattrBody = [0, 1, 2, 3]
    numItems = 100000

    for i in range(numItems):
        key = ogkey + str(i+520)
        cb.upsert(key, docBody)
        # cb.mutate_in(key, SD.upsert(xattrPath, xattrBody, xattr=True), SD.upsert_fulldoc(docBody))
        cb.mutate_in(key, SD.upsert(xattrPath, xattrBody, xattr=True))
        cb.touch(key, 1)

    time.sleep(10)
    for i in range(numItems):
        key = ogkey + str(i+520)
        # cb.upsert(key, {"new": 5656876543})
        try:
            res = cb.lookup_in(key, SD.get(xattrPath, xattr=True))
        except exceptions.NotFoundError:
            print("key not found")

        # cb.delete(key)
    total = 0
    # for key, value in cb.stats()['total_items'].items():
    #     total += value
    print("expired", cb.stats()['vb_active_expired'])
    return


def cluster_setup(url: str, username: str, password: str, port: int):
    setup_url = str(url + 'node/controller/setupServices/')
    r = requests.post(setup_url, data={'services': 'kv', 'ramQuotaMB': '100'}, auth=(username, password))
    print('setup: ', r)

    pass_url = str(url + 'settings/web/')
    p = requests.post(pass_url, data={'password': password, 'username': username, 'port': str(port)},
                      auth=(username, password))
    print('pass', p)

    return


def bucket_setup(url: str, bucket_name: str, username: str, password: str, port: int):
    get_url = str(url + 'pools/default/buckets/')
    r = requests.get(get_url, auth=(username, password))
    json_read = json.loads(r.text)
    bucket_list = []
    for a in range(len(json_read)):
        bucket_list.append(json_read[a]['name'])

    if bucket_name in bucket_list:
        return

    else:
        url_split = url.split(':')
        no_port = url_split[1].replace('/', '')
        adm = Admin(username, password, host=no_port, port=port)

        adm.bucket_create(bucket_name, bucket_type='couchbase', ram_quota=100, replicas=1)
        adm.wait_ready(bucket_name, timeout=30)

    # bucket_url = str(url + 'pools/default/buckets/')
    # b = requests.post(bucket_url, data={'flushEnabled': '1', 'threadsNumber': '3',
    #                                     'replicaIndex': '0', 'evictionPolicy': 'valueOnly',
    #                                     'ramQuotaMB': '512', 'bucketType': 'couchbase',
    #                                     'name': bucket_name},
    #                   auth=('Administrator', 'password'))
    # print('bucket', b)

    return


def server_add_setup_vagrants(url: str, username: str, password: str):
    add_url = str(url + 'controller/addNode/')
    url_split = url.split(':')
    no_port = url_split[1].replace('/', '')
    n2_addr = str(no_port[:-1] + '2')
    n2 = requests.post(add_url, data={'hostname': n2_addr,
                                      'user': username, 'password': password,
                                      'services': 'kv'}, auth=(username, password))
    n3_addr = str(no_port[:-1] + '3')
    n3 = requests.post(add_url, data={'hostname': n3_addr,
                                      'user': username, 'password': password,
                                      'services': 'kv'}, auth=(username, password))
    n4_addr = str(no_port[:-1] + '4')
    n4 = requests.post(add_url, data={'hostname': n4_addr,
                                      'user': username, 'password': password,
                                      'services': 'n1ql,index,fts'}, auth=(username, password))

    print('nodeadding', n2, n3, n4)

    rebalance_url = str(url + 'controller/rebalance/')
    server_list_string = 'ns_1@' + no_port + ',ns_1@' + n2_addr + ',ns_1@' + n3_addr + ',ns_1@' + n4_addr
    r = requests.post(rebalance_url,
                      data={
                          'knownNodes': server_list_string},
                      auth=(username, password))

    print('rebal', r)

    return

def server_add_setup_cluster_run(url: str, username: str, password: str, port: int):
    print("currently broken don't expect it to work")
    url_split = url.split(':')
    new_node_url = url_split[0] + ':' + url_split[1] + ':9001/'
    cluster_setup(new_node_url, username, password, 9001)

    add_url = str(url + 'node/controller/doJoinCluster/')
    no_port = url_split[1].strip('/')
    print(no_port)
    n2 = requests.post(add_url,
                       data={'clusterMemberHostIp': no_port, 'clusterMemberPort': '9001',
                             'user': username, 'password': password},
                       auth=(username, password))

    print('nodeadding', n2)

    rebalance_url = str(url + 'controller/rebalance/')
    server_list_string = 'ns_1@' + no_port + ':9000/,ns_1@' + no_port + ':9001'
    r = requests.post(rebalance_url,
                      data={'knownNodes': server_list_string},
                      auth=(username, password))

    print('rebal', r)


def init_new_server(url: str, target_bucket: str, username: str, password: str, port: int):
    cluster_setup(url, username, password, port)
    # server_add_setup_vagrants(url, username, password)
    # server_add_setup_cluster_run(url, username, password, port)
    time.sleep(5)  # needed to ensure that rebalance and bucket creation don't overlap and error
    bucket_setup(url, target_bucket, username, password, port)
    time.sleep(5) # Wait for bucket to setup
    return


def input_looper(message: str, in_list: list) -> str:
    loop = True
    while loop:
        choice = str(input(message))
        if choice in in_list:
            loop = False
        else:
            print('Invalid entry, please try again')
    return choice


main()
