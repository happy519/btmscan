import constant

BASE_SUBSIDY = 41250000000
SUBSIDY_REDUCTION_INTERVAL = 840000

def get_base_reward(hight):
    return BASE_SUBSIDY >> (hight/SUBSIDY_REDUCTION_INTERVAL)

def get_block_fee(block):
    for tx in block['transactions']:
        if is_coinbase(tx):
            for tx_out in tx['outputs']:
                    return tx_out['amount'] - get_base_reward(block['height'])

    raise Exception('No coinbase transaction in block %s', block['height'])

def is_coinbase(tx):
    for tx_in in tx['inputs']:
        if tx_in['type'] == 'coinbase':
            return True

    return False

def get_tx_fee(tx):
    coinbase = False
    input = 0
    output = 0
    for tx_in in tx['inputs']:
        if tx_in['type'] == 'coinbase':
            coinbase = True
        if tx_in['asset_id'] == constant.BTM_ID:
            input += tx_in['amount']

    for tx_out in tx['outputs']:
        if tx_out['asset_id'] == constant.BTM_ID:
            output += tx_out['amount']

    return (abs(input-output), coinbase)

# if __name__ == '__main__':
#     block = {u'nonce': 0, 'fee': 5000000000, u'hash': u'367402b6b2d6fe4f8d7dd0cd045c94034b6b0e989e87a9c409aa5ab362d361f2', u'transaction_status_hash': u'6978a65b4ee5b6f4914fe5c05000459a803ecf59132604e5d334d64249c5e50a', u'timestamp': 1525757250, u'transactions': [{u'inputs': [{u'asset_id': u'0000000000000000000000000000000000000000000000000000000000000000', u'asset_definition': {}, u'amount': 0, u'type': u'coinbase', u'arbitrary': u'7e'}], u'outputs': [{u'asset_id': u'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', u'control_program': u'00144c8d5ffb740bc0ccec5164b188f4346550f31072', u'asset_definition': {}, u'amount': 46250000000, u'address': u'sm1qfjx4l7m5p0qvemz3vjcc3ap5v4g0xyrjsamh2p', u'position': 0, u'type': u'control', u'id': u'37e2b88f22878da99bd69928c84b1dcf16d76ff2f2040c63c1d87848fd1457ce'}], u'status_fail': False, u'time_range': 0, 'block_hash': u'367402b6b2d6fe4f8d7dd0cd045c94034b6b0e989e87a9c409aa5ab362d361f2', u'version': 1, 'block_height': 126, u'id': u'ecccf1020acb992228ed3d13f172806c7fe381467c823aa7ae4ad1d9854f254d', u'size': 76}, {u'inputs': [{u'asset_id': u'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', u'spent_output_id': u'0c208212ff54dbaaa65ce991b636363cba5b42ab29779dd09b85ef0139ee7bec', u'control_program': u'00144c8d5ffb740bc0ccec5164b188f4346550f31072', u'asset_definition': {}, u'amount': 41250000000, u'address': u'sm1qfjx4l7m5p0qvemz3vjcc3ap5v4g0xyrjsamh2p', u'type': u'spend'}, {u'asset_id': u'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', u'spent_output_id': u'1067d521dc4ae5e9788fcac05b35fd7b09a16c794c2b2a2eaa5398af173d349f', u'control_program': u'00144c8d5ffb740bc0ccec5164b188f4346550f31072', u'asset_definition': {}, u'amount': 41250000000, u'address': u'sm1qfjx4l7m5p0qvemz3vjcc3ap5v4g0xyrjsamh2p', u'type': u'spend'}, {u'asset_id': u'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', u'spent_output_id': u'13b43836e8eeebedd009638d9c34b6a01515a396d6bcf94092b6b52ba9a3ae6d', u'control_program': u'00144c8d5ffb740bc0ccec5164b188f4346550f31072', u'asset_definition': {}, u'amount': 41250000000, u'address': u'sm1qfjx4l7m5p0qvemz3vjcc3ap5v4g0xyrjsamh2p', u'type': u'spend'}], u'outputs': [{u'asset_id': u'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', u'control_program': u'0014751447511776fbac500331721e6d13f46505b573', u'asset_definition': {}, u'amount': 18750000000, u'address': u'sm1qw52yw5ghwma6c5qrx9epumgn73jstdtn7fyv7c', u'position': 0, u'type': u'control', u'id': u'dce1111df360df7860ce559b53400ccccde34545b957ec3a088655a0e46846db'}, {u'asset_id': u'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', u'control_program': u'00144c8d5ffb740bc0ccec5164b188f4346550f31072', u'asset_definition': {}, u'amount': 100000000000, u'address': u'sm1qfjx4l7m5p0qvemz3vjcc3ap5v4g0xyrjsamh2p', u'position': 1, u'type': u'control', u'id': u'c08c4d9ab1bd161c41ba8522557987acefc2a41dcf0ab6a6d8168dbc89b7599d'}], u'status_fail': False, u'time_range': 0, 'block_hash': u'367402b6b2d6fe4f8d7dd0cd045c94034b6b0e989e87a9c409aa5ab362d361f2', u'version': 1, 'block_height': 126, u'id': u'81d48594df45d6ee135f7d7f1e9896333f493e7911d3853ccec8045613e47969', u'size': 731}], u'height': 126, u'difficulty': u'7640617385137161009307348744505657205600476961500639119722770042191872', u'version': 1, u'previous_block_hash': u'37f5dd743c170fc81572deb15d5368504158cab6b1ddaed1b69516c12b3880f7', 'coinbase': 46250000000, u'transaction_merkle_root': u'34b9149bcacfecba8e9669244ee8df884fdaba6a4ead18237e4282e6f3e2a9e8', u'bits': 2161727821137910632, u'size': 1846}
#     print get_block_fee(block)