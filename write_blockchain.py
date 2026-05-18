from web3 import Web3
from dotenv import load_dotenv
import hashlib
import json
import os

# ==========================================================
# CONFIGURATION
# ==========================================================

load_dotenv()

RPC_URL = "http://10.229.43.182:8545"

SENDER_ADDRESS = "0x52E890381d7D41D274FA2bA7673122cB5807b6DF"

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

CHAIN_ID = 32383

PDF_FILE = "blockchain.pdf"

# Adresse nulle demandée dans l'exercice
NULL_ADDRESS = "0x0000000000000000000000000000000000000000"

# URL Github du PDF
PDF_URL = "https://github.com/onfire1003/C107_JoelCunhaFaria/blob/main/blockchain.pdf"

# ==========================================================
# CONNEXION
# ==========================================================

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("Connecté à la blockchain")
else:
    print("Connexion échouée")
    exit()

# ==========================================================
# HASH SHA-256 DU PDF
# ==========================================================

def calculer_hash_pdf(fichier):
    sha256 = hashlib.sha256()

    with open(fichier, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

# ==========================================================
# CRÉATION DES MÉTADONNÉES
# ==========================================================

pdf_hash = calculer_hash_pdf(PDF_FILE)

metadata = {
    "pdf": PDF_URL,
    "hash": pdf_hash
}

print("\n=== Métadonnées ===")
print(metadata)

# Conversion JSON -> HEX
metadata_json = json.dumps(metadata)

metadata_hex = w3.to_hex(text=metadata_json)

# ==========================================================
# NONCE
# ==========================================================

nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)

# ==========================================================
# TRANSACTION
# ==========================================================

transaction = {
    'from': SENDER_ADDRESS,
    'to': NULL_ADDRESS,
    'value': 0,
    'gas': 200000,
    'gasPrice': w3.to_wei('20', 'gwei'),
    'nonce': nonce,
    'chainId': CHAIN_ID,
    'data': metadata_hex
}

# ==========================================================
# SIGNATURE
# ==========================================================

signed_tx = w3.eth.account.sign_transaction(
    transaction,
    PRIVATE_KEY
)

# ==========================================================
# ENVOI
# ==========================================================

tx_hash = w3.eth.send_raw_transaction(
    signed_tx.raw_transaction
)

print("\n✅ Transaction envoyée")
print("Hash transaction :", tx_hash.hex())

print("\nSHA-256 du PDF :")
print(pdf_hash)