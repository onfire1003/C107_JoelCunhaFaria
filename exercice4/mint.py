from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv(dotenv_path="../.env")

RPC_URL = "http://10.229.43.182:8545"
SENDER_ADDRESS = "0x52E890381d7D41D274FA2bA7673122cB5807b6DF"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = 32383
CONTRACT_ADDRESS = "0x9A8C8E2EB8F6fA1Bd7EF9161417F64E48bf54225"

METADATA_URI = "https://raw.githubusercontent.com/onfire1003/C107_JoelCunhaFaria/main/exercice4/metadata.json"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("✅ Connecté à la blockchain")
else:
    print("❌ Connexion échouée")
    exit()

code = w3.eth.get_code(w3.to_checksum_address(CONTRACT_ADDRESS))
if code in (b'', b'0x'):
    print(f"❌ Aucun contrat trouvé à {CONTRACT_ADDRESS}")
    exit()
print(f"✅ Contrat trouvé")

with open("SimpleMintContract.abi", "r") as f:
    abi = json.load(f)

sender = w3.to_checksum_address(SENDER_ADDRESS)
contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# Mint du NFT
nonce_latest  = w3.eth.get_transaction_count(sender, 'latest')
nonce_pending = w3.eth.get_transaction_count(sender, 'pending')
print(f"Nonce confirmé: {nonce_latest} | Nonce pending: {nonce_pending}")

# Utilise le nonce pending pour remplacer la tx bloquée
nonce = nonce_pending - 1 if nonce_pending > nonce_latest else nonce_latest
print(f"Nonce utilisé: {nonce}")

mint_txn = contract.functions.mint(METADATA_URI).build_transaction({
    "chainId": CHAIN_ID,
    "gas": 300000,
    "gasPrice": w3.to_wei("200", "gwei"),
    "nonce": nonce,
    "value": w3.to_wei(0.05, "ether"),
})
signed = w3.eth.account.sign_transaction(mint_txn, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"Mint en cours... TX: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
token_id = contract.functions.totalSupply().call()
print(f"✅ NFT minté ! Token ID: {token_id} | Bloc: {receipt.blockNumber}")

balance = contract.functions.balanceOf(sender).call()
print(f"NFTs dans ce wallet : {balance}")
