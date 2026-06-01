from dotenv import load_dotenv
from web3 import Web3
import os
import json

# ==========================================================

# CONFIGURATION

# ==========================================================

load_dotenv()

# URL RPC de la blockchain privée CPNV

RPC_URL = "http://10.229.43.182:8545"

# Adresse du compte expéditeur

SENDER_ADDRESS = "0x52E890381d7D41D274FA2bA7673122cB5807b6DF"

# Clé privée

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

contract_address = "0x9A8C8E2EB8F6fA1Bd7EF9161417F64E48bf54225"

# ==========================================================

# CONNEXION À LA BLOCKCHAIN

# ==========================================================


w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():

    print("✅ Connecté à la blockchain")

else:

    print("❌ Connexion échouée")

    exit()


# Charger ABI
with open("SimpleMintContract.abi", "r") as abi_file:
    abi = json.load(abi_file)

# Créer instance du contrat
contract = w3.eth.contract(
    address=contract_address,
    abi=abi
)

# URL de votre image
metadata_url = "https://github.com/onfire1003/C107_JoelCunhaFaria/blob/main/exercice4/image.jpg"

# Nonce
nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)

# Construction transaction mint
transaction = contract.functions.mint(
    metadata_url
).build_transaction({
    "chainId": 32383,
    "gas": 300000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce,
    "value": w3.to_wei(0.05, "ether")
})

# Signature
signed_tx = w3.eth.account.sign_transaction(
    transaction,
    PRIVATE_KEY
)

# Envoi
tx_hash = w3.eth.send_raw_transaction(
    signed_tx.raw_transaction
)

print("Transaction envoyée :", tx_hash.hex())

# Attente confirmation
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("NFT minté avec succès !")
print("Transaction :", receipt.transactionHash.hex())


#récupérer le nombre nft
balance = contract.functions.balanceOf(
    SENDER_ADDRESS
).call()

print("NFT possédés :", balance)

"""
#vérif mint
status = contract.functions.isMintEnabled().call()

print("Mint activé :", status)

status = contract.functions.maxSupply().call()

print("Max supply :", status)
"""