from web3 import Web3


def connect(url):
	return Web3(Web3.HTTPProvider(url))

# url = "https://rinkeby.infura.io/v3/6e9f1a0bf9234d53ae42dbc976114388"
# account = "0xb89A963D1A0C5Fe66EFC921E8733808A659A29B3"

# url = "http://127.0.0.1:7545"
# account = "0xa9420d0AfA5c47D39d37996443Cbe204f019a98A"

# connector = Web3Connector(url)

# print(connector.web3.isConnected())
# print(connector.get_account_balance(account))