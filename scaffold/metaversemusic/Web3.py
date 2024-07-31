from web3 import Web3
from django.conf import settings

# Initialize Web3 connection
w3 = Web3(Web3.HTTPProvider(settings.INFURA_URL))

def get_gas_price():
    """Fetch current gas price from the network"""
    return w3.eth.gas_price

def estimate_gas(transaction):
    """Estimate gas required for a transaction"""
    return w3.eth.estimate_gas(transaction)

def calculate_minting_cost(gas_limit=200000):
    """Calculate the estimated cost of minting an NFT"""
    gas_price = get_gas_price()
    estimated_cost = gas_price * gas_limit
    return w3.from_wei(estimated_cost, 'ether')

def send_transaction(transaction, private_key):
    """Sign and send a transaction"""
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def get_transaction_receipt(tx_hash):
    """Get the receipt of a transaction"""
    return w3.eth.get_transaction_receipt(tx_hash)
