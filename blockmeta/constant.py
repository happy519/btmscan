#common
DEFAULT_START = 0
DEFAULT_OFFSET = 10
DEFAULT_MINER_OFFSET = 30
DEFAULT_LIST = 30
DEFAULT_PERIOD = 30
DEFAULT_RANK_LEN = 100

DISPLAY_LEN = 10
EXPIRE_TIME = 300

MAX_HANDLE = 5
MAX_ADDRESSES = 10
DISPLAY_UNCONFIRMED = 7

MAX_MONTH = 100 * 12
DAY_IN_SEC = 60 * 60 *24
ONE_DAY =  24
LOG_0 = 1e-5
TOP_N = 10

# address api
FILTERS = ['all', 'sent', 'recv', 'unspent', 'unconfirmed', 'confirmed']
# ethereum address part
#(1) addr
FILTERS = FILTERS + ['tx', 'holder', 'mine', 'internaltx', 'uncles', 'source']


FILTER_CONFIRMED ='confirmed'
FILTER_UNCONFIRMED = 'unconfirmed'
FILTER_DEFAULT = 'all'
FILTER_SENT = 'sent'
FILTER_RECEIVED = 'recv'
FILTER_UNSPENT = 'unspent'

SHARDING_SIZE = 1000
EXPIRE_ADDRESS =  30
BTC_IN_SATOSHIS = 100000000


#tx chart
TX_CHARTS = ['opreturn', 'coinbase', 'largetx', 'toprank']
TX_TYPE_DEFAULT = 'opreturn'
TX_TYPE_OPRETURN = 'opreturn'
TX_TYPE_COINBASE = 'coinbase'
TX_TYPE_LARGETX = 'largetx'
TX_TYPE_TOPRANK ='toprank'

PRIORITY_THRESHOLD = 57600000
#driver


#archives
ARCHIVES_FILTERS = ['all', 'bussiness', 'personal', 'miner', 'donation', 'hack', 'gambling', 'other']
DEFAULT_ARCHIVES_FILTER = 'all'
DEFAULT_ARCHIVES_DISPLAY = 30


#graph
EXPIRE_CAPTCHA =  60

#Bitcoin
BTC_IN_SATOSHIS = 10 ** 8
TX_HASH_LEN = 64
HASHRATE_PER_P = 1024 * 1024 * 1024 * 1024 * 1024

# ethereum reward
BLOCK_REWARD = 5
UNCLE_REWARD = 5 * 1.0 / 32
# token demicals

# chain type
BITCOIN="bitcoin"
ETHEREUM="ethereum"
ETHEREUMCLASSIC="ethereumclassic"
BYTOM="bytom"


METHOD_ETH_GET_BALANCE = "eth_getBalance"
METHOD_ETH_GET_NUMBER = "eth_blockNumber"




