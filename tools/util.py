import constant

def get_block_reward(block):
    reward = 0
    coinbase_reward = 0
    for tx in block['transactions']:
        (fee, coinbase) = get_tx_fee(tx)
        if coinbase:
            coinbase_reward = fee

        reward += fee

    return (reward-coinbase_reward, coinbase_reward)



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

    return (output-input, coinbase)

