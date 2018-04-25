# -*- coding: utf-8 -*-

import requests
import json

def test_block():
    data_dict = {'block_height': 8}
    url_rpc = 'http://localhost:9888' + '/' + 'get-block'

    r = requests.post(url_rpc, json.dumps(data_dict))
    block_info = r.json()
    print block_info
    print "=========================>>"
    assert block_info["status"], "success"
    print "end"


if __name__ == '__main__':
    test_block()
