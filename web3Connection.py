from web3 import Web3


def connect(url):
	return Web3(Web3.HTTPProvider(url))

# url = "https://rinkeby.infura.io/v3/6e9f1a0bf9234d53ae42dbc976114388"
# account = "0xb89A963D1A0C5Fe66EFC921E8733808A659A29B3"

url = "http://127.0.0.1:8545"
account = "0xfa915e49980571b3163e01caddc90dc742c58132"

connector = connect(url)

print(connector.isConnected())
