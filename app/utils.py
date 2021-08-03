from web3 import Web3


def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/5e7d471342c840d49675ff3e5d9f0dfd"))
    address = "0x532648Ab57E9c2e20F414115eB1Daa77d7bcC8Bb"
    privateKey = "0x7d9e1cf7cee3cb8d8012d12e7c2f23b77640a752e7c3c098fec4b4c8c7f0c2a3"
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, "ether")
    signedTx = w3.eth.account.signTransaction(
        dict(
            nonce=nonce,
            gasPrice=gasPrice,
            gas=100000,
            to="0x0000000000000000000000000000000000000000",
            value=value,
            data=message.encode("utf-8"),
        ),
        privateKey,
    )

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId


