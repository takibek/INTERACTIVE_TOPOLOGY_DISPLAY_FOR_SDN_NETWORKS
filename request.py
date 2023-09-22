# REST API for switch configuration
#
# get all the switches
# GET /v1.0/topology/switches
#
# get the switch
# GET /v1.0/topology/switches/<dpid>
#
# get all the links
# GET /v1.0/topology/links
#
# get the links of a switch
# GET /v1.0/topology/links/<dpid>
#
# get all the hosts
# GET /v1.0/topology/hosts
#
# get the hosts of a switch
# GET /v1.0/topology/hosts/<dpid>
#
# where
# <dpid>: datapath id in 16 hex

import requests

SERVER = 'http://localhost:8080/'

def get_switches():
    r = requests.get(SERVER + 'v1.0/topology/switches')
    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_hosts():
    r = requests.get(SERVER + 'v1.0/topology/hosts')
    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_hosts_by_switch(switch):
    r = requests.get(SERVER + 'v1.0/topology/hosts/' + switch)
    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_links():
    r = requests.get(SERVER + 'v1.0/topology/links')
    if r.status_code == 200:
        return r.json()
    else:
        return None


if __name__ == '__main__':
    switches = get_switches()
    if switches != None:
        for i in switches:
            print(i['dpid'])
            hosts = get_hosts_by_switch(i['dpid'])
            if hosts != None:
                [print(k['mac']) for k in hosts]
