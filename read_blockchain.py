from web3 import Web3
import json

RPC_URL = "http://10.229.43.182:8545"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("Connexion échouée")
    exit()

print("Connecté")

# ==========================================================
# HASH DE TRANSACTION À LIRE
# ==========================================================

tx_hash = input("Entrer le hash de transaction : ")

# ==========================================================
# RÉCUPÉRATION TRANSACTION
# ==========================================================

tx = w3.eth.get_transaction(tx_hash)

# ==========================================================
# LECTURE DU DATA
# ==========================================================

data_hex = tx["input"]

# HEX -> TEXTE
data_text = w3.to_text(hexstr=data_hex)

# TEXTE -> JSON
metadata = json.loads(data_text)

print("\n=== Données récupérées ===")

print("PDF :", metadata["pdf"])
print("Hash :", metadata["hash"])