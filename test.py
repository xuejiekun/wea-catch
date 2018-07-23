# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# baseurl = '192.168.1.109'
baseurl = 'localhost'

def crack_csrf():
    s = requests.Session()
    r = s.get(r'http://{}:5000/query_loc'.format(baseurl))

    bsobj = BeautifulSoup(r.content, 'lxml')
    csrf = bsobj.find('input', {'name': 'csrf_token'})

    # dat = {'csrf_token': csrf['value'],
    #        'address_id': '1'}

    dat = {'address_id': '1'}
    r2 = s.post(r'http://{}:5000/query_loc'.format(baseurl), data=dat)
    print(r2.text)
    print(r2.url)


def test_api():
    s = requests.Session()
    r = s.get(r'http://{}:5000/api/1.0/address/1'.format(baseurl))
    print(r.json())

crack_csrf()
# test_api()
