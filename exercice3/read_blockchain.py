from web3 import Web3
import json
import hashlib
import sys

w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))
assert w3.is_connected(), "Échec de la connexion au nœud Ethereum"


def get_metadata_from_tx(tx_hash):
    tx = w3.eth.get_transaction(tx_hash)
    raw_data = tx['input']
    text = w3.to_text(raw_data)
    return json.loads(text)


def verify_pdf(file_path, expected_hash):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    computed = sha256.hexdigest()
    match = computed == expected_hash
    print(f"Hash attendu  : {expected_hash}")
    print(f"Hash calculé  : {computed}")
    print(f"Vérification  : {'OK' if match else 'ECHEC'}")
    return match


if __name__ == "__main__":
    tx_hash = input("Entrez le hash de transaction : ").strip()
    metadata = get_metadata_from_tx(tx_hash)
    print(f"\nMétadonnées récupérées :")
    print(json.dumps(metadata, indent=2))

    local_pdf = input("\nEntrez le chemin local du PDF à vérifier (laisser vide pour ignorer) : ").strip()
    if local_pdf:
        verify_pdf(local_pdf, metadata["sha256"])
