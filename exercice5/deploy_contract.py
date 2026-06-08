from dotenv import load_dotenv
from web3 import Web3
import os
import json

load_dotenv(dotenv_path="../.env")

RPC_URL = "http://10.229.43.182:8545"
SENDER_ADDRESS = "0x52E890381d7D41D274FA2bA7673122cB5807b6DF"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = 32383

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("✅ Connecté à la blockchain")
else:
    print("❌ Connexion échouée")
    exit()

with open("CunhaFariaJoelNFT.abi", "r") as f:
    abi = json.load(f)

with open("CunhaFariaJoelNFT.bin", "r") as f:
    bytecode = f.read().strip()

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

sender = w3.to_checksum_address(SENDER_ADDRESS)
nonce = w3.eth.get_transaction_count(sender)

deploy_txn = contract.constructor(sender).build_transaction({
    "chainId": CHAIN_ID,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce,
})

signed_txn = w3.eth.account.sign_transaction(deploy_txn, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

print(f"Déploiement en cours... TX: {tx_hash.hex()}")

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = receipt.contractAddress

print(f"✅ Contrat déployé à l'adresse : {contract_address}")
print(f"   Block : {receipt.blockNumber}")
