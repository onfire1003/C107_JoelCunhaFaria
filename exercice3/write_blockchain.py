from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv(dotenv_path="../.env")

# Connexion au nœud Ethereum
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))
assert w3.is_connected(), "Échec de la connexion au nœud Ethereum"

sender_address = w3.to_checksum_address("0x52E890381d7D41D274FA2bA7673122cB5807b6DF")
private_key = os.getenv("PRIVATE_KEY")
recipient_address = w3.to_checksum_address("0x0000000000000000000000000000000000000000")

pdf_path = "https://github.com/onfire1003/C107/blob/main/exercice3/joelcunhafaria.pdf"
pdf_hash = "df42bb16603338d43437d7604b4b7c95dd8fdc20499bdca9094f9f69539b5fdd"

metadata = {
    "student": "Joel Cunha Faria",
    "file_path": pdf_path,
    "sha256": pdf_hash
}

metadata_hex = w3.to_hex(text=json.dumps(metadata))

nonce = w3.eth.get_transaction_count(sender_address)

transaction = {
    'from': sender_address,
    'to': recipient_address,
    'value': 0,
    'gas': 200000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce,
    'chainId': 32383,
    'data': metadata_hex
}

signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

try:
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Transaction envoyée : {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    final_hash = receipt.transactionHash.hex()
    print(f"Confirmée dans le bloc {receipt.blockNumber}")
    print(f"Hash de transaction : {final_hash}")

    with open("tx_result.txt", "w") as f:
        f.write(f"tx_hash: {final_hash}\n")
        f.write(f"block: {receipt.blockNumber}\n")
        f.write(f"metadata: {json.dumps(metadata)}\n")
    print("Résultat sauvegardé dans tx_result.txt")
except Exception as e:
    print(f"Erreur : {e}")
