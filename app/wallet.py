from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/5e7d471342c840d49675ff3e5d9f0dfd"))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address': {address},\n Your Private Key : {privateKey}")
