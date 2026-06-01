from web3 import Web3
from dotenv import load_dotenv
import os

# ==========================================================
# CONFIGURATION
# ==========================================================

load_dotenv()


RPC_URL = "http://10.229.43.182:8545"

SENDER_ADDRESS = "0x52E890381d7D41D274FA2bA7673122cB5807b6DF"

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

AMOUNT_TO_SEND = 0.1  # en ETH

# ==========================================================
# CONNEXION À LA BLOCKCHAIN
# ==========================================================

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("✅ Connecté à la blockchain")
else:
    print("❌ Connexion échouée")
    exit()

# ==========================================================
# LECTURE DES ADRESSES
# ==========================================================

def lire_adresses(fichier):
    adresses = []

    with open(fichier, "r") as f:
        for ligne in f:
            adresse = ligne.strip()

            # Vérifier que l’adresse est valide
            if w3.is_address(adresse):
                adresses.append(adresse)

    return adresses

# ==========================================================
# AFFICHER LES SOLDES
# ==========================================================

def afficher_soldes(adresses):
    for adresse in adresses:
        balance_wei = w3.eth.get_balance(adresse)
        balance_eth = w3.from_wei(balance_wei, 'ether')

        print(f"{adresse} : {balance_eth} ETH")

# ==========================================================
# ENVOI DE TRANSACTION
# ==========================================================

def envoyer_eth(destinataire, montant_eth, nonce):
    transaction = {
        "nonce": nonce,
        "to": destinataire,
        "value": w3.to_wei(montant_eth, 'ether'),
        "gas": 21000,
        "gasPrice": w3.to_wei('20', 'gwei'),
        "chainId": w3.eth.chain_id
    }

    # Signature de la transaction
    signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    # Envoi sur le réseau
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()

# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================

def main():
    adresses = lire_adresses("adresses.txt")

    print("\n=== Soldes avant envoi ===")
    afficher_soldes(adresses)

    # Récupération du nonce initial
    nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)

    print("\n=== Envoi des transactions ===")

    for adresse in adresses:
        try:
            tx_hash = envoyer_eth(
                adresse,
                AMOUNT_TO_SEND,
                nonce
            )

            print(f"Transaction envoyée vers {adresse}")
            print(f"Hash : {tx_hash}")

            # Incrément du nonce
            nonce += 1

        except Exception as e:
            print(f"Erreur : {e}")

    print("\n=== Soldes après envoi ===")
    afficher_soldes(adresses)

main()