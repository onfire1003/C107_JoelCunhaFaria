from dotenv import load_dotenv
from web3 import Web3
import os
import json

load_dotenv(dotenv_path="../.env")

RPC_URL = "http://10.229.43.182:8545"
SENDER_ADDRESS = "0x52E890381d7D41D274FA2bA7673122cB5807b6DF"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = 32383
CONTRACT_ADDRESS = "0x29e8F2e31805DEF4f5CE435B5cfd4afda37568a3"

IMAGE_URL_1 = "https://raw.githubusercontent.com/onfire1003/C107_JoelCunhaFaria/main/exercice5/metadata_super.json"
IMAGE_URL_2 = "https://raw.githubusercontent.com/onfire1003/C107_JoelCunhaFaria/main/exercice5/metadata_walter.json"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("✅ Connecté à la blockchain")
else:
    print("❌ Connexion échouée")
    exit()

with open("CunhaFariaJoelNFT.abi", "r") as f:
    abi = json.load(f)

sender = w3.to_checksum_address(SENDER_ADDRESS)
contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# Activer le mint seulement si nécessaire
is_enabled = contract.functions.isMintEnabled().call()
print(f"Mint activé : {is_enabled}")

if not is_enabled:
    print("Activation du mint...")
    nonce_l = w3.eth.get_transaction_count(sender, 'latest')
    nonce_p = w3.eth.get_transaction_count(sender, 'pending')
    nonce = nonce_p - 1 if nonce_p > nonce_l else nonce_l
    toggle_txn = contract.functions.toggleIsMintEnabled().build_transaction({
        "chainId": CHAIN_ID,
        "gas": 100000,
        "gasPrice": w3.to_wei("200", "gwei"),
        "nonce": nonce,
    })
    signed = w3.eth.account.sign_transaction(toggle_txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
    print(f"✅ Mint activé (TX: {tx_hash.hex()})")


def mint_nft(image_url, label):
    nonce_l = w3.eth.get_transaction_count(sender, 'latest')
    nonce_p = w3.eth.get_transaction_count(sender, 'pending')
    nonce = nonce_p - 1 if nonce_p > nonce_l else nonce_l
    mint_txn = contract.functions.mint(image_url).build_transaction({
        "chainId": CHAIN_ID,
        "gas": 300000,
        "gasPrice": w3.to_wei("200", "gwei"),
        "nonce": nonce,
        "value": w3.to_wei(0.05, "ether"),
    })
    signed = w3.eth.account.sign_transaction(mint_txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Mint {label} en cours... TX: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
    token_id = contract.functions.totalSupply().call()
    print(f"✅ NFT {label} minté ! Token ID: {token_id} | Block: {receipt.blockNumber}")
    return receipt


print("\n--- Mint NFT #1 ---")
mint_nft(IMAGE_URL_1, "#1")

print("\n--- Mint NFT #2 ---")
mint_nft(IMAGE_URL_2, "#2")

balance = contract.functions.balanceOf(sender).call()
print(f"\nNFTs possédés dans ce wallet : {balance}")
