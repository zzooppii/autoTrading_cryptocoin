from web3 import Web3

infuraA = 'https://kovan.infura.io/v3/34ed41c4cf28406885f032930d670036'
infuraB = 'https://ropsten.infura.io/v3/'
# Change this to use your own infura ID
web3 = Web3(
    Web3.HTTPProvider(
        infuraA))
# AggregatorV3Interface ABI
abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
# Price Feed address
addr = '0x6135b13325bfC4B00278B4abC5e20bbce2D6580e' #BTC-USD Kovan
addr2 = '0x9326BFA02ADD2366b30bacB125260Af641031331' #ETH-USD Kovan
addr3 = '0x8468b2bDCE073A157E560AA4D9CcF6dB1DB98507'
addr4 = '0xB830F888a287D2bc7AA2a42C7cED8ecEfcB8cb34'
addr5 = '0x777A68032a88E5A84678A77Af2CD65A7b3c0775a'    #DAI/USD Kovan


# Set up contract instance
contract = web3.eth.contract(address=addr, abi=abi)
contract2 = web3.eth.contract(address=addr2, abi=abi)
contract3 = web3.eth.contract(address=addr5, abi=abi)
# Make call to latestRoundData()
latestData = contract.functions.latestRoundData().call()
latestData2 = contract2.functions.latestRoundData().call()
latestData3 = contract3.functions.latestRoundData().call()

divide = 10 ** 8

btc_price = float(latestData[1]) / float(divide)
eth_price = latestData2[1] / divide
dai_price = latestData3[1] / divide
btc_price_krw = btc_price * 1100
eth_price_krw = eth_price * 1100
dai_price_krw = dai_price * 1100
# a = 1400000
# b = a / 1100

print(latestData)
print(latestData2)
print(latestData3)
print("BTC-USD : $" + str(btc_price))
print("ETH-USD : $" + str(eth_price))
print("DAI-USD : $" + str(dai_price))
print("BTC-KRW : " + str(btc_price_krw) + " 원")
print("ETH-KRW : " + str(eth_price_krw) + " 원")
print("DAI-KRW : " + str(dai_price_krw) + " 원")
# print("b : $" + str(b))

