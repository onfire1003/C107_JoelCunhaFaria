from web3 import Web3
import json
import config

# Adresse et clé privée de l'expéditeur
private_key = "6564afasdfa798sdfas64dfas68fa6s1fas6dfa6s48dfa6s1dfas31fa6sdfas7fdasfs"

# Connexion au nœud Ethereum
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))  # Remplacez par l'URL de votre nœud
assert w3.is_connected(), "Échec de la connexion au nœud Ethereum"

URI =  "https://www.cpnv.me/9c21b7718f9214bce2053b41a48584627cbfabe445d5863d6f322c3b8359fff5/metadata.json"

# Adresse et ABI du contrat déployé
contract_address = "0x28eE64601A58EDC21BC2Da9e33448c2822371dED"
deployer_address = "0x13cacedfb1b86e047cb21a5fa1c6d53417c3d69d"
recipient_address = "0x13cacedfb1b86e047cb21a5fa1c6d53417c3d69d"

sender_address = w3.to_checksum_address(deployer_address)


# Charger l'ABI du contrat
with open("SimpleMintContract.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Charger le contrat
nft_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Étape 1 : Mint du token
nonce = w3.eth.get_transaction_count(sender_address)
valueEth = 0.05
mint_txn = nft_contract.functions.mint(URI).build_transaction({
    "chainId": 32383,  # ID de votre blockchain privée ou testnet
    "gas": 2000000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "value": w3.to_wei(valueEth, "ether"),  # Prix du mint défini dans le contrat
    "nonce": nonce
})

signed_mint_txn = w3.eth.account.sign_transaction(mint_txn, private_key)

try:
    # Fait un test avant pour savoir si tout est en ordre, si c'est bon ça passe sinon 
    # ça leve l'exception
    mint_check = nft_contract.functions.mint(metadata_json).call({
        "from": sender_address,
        "value": w3.to_wei(valueEth, "ether")  # Prix du mint défini dans le contrat
    })


    mint_tx_hash = w3.eth.send_raw_transaction(signed_mint_txn.raw_transaction)
    print(f"Transaction de mint envoyée : {mint_tx_hash.hex()}")

    # Attendre la confirmation
    mint_receipt = w3.eth.wait_for_transaction_receipt(mint_tx_hash)
    print(f"Transaction de mint confirmée dans le bloc {mint_receipt.blockNumber}")
except Exception as e:
    print(f"Une erreur est survenue : {str(e)}")

# Récupérer le tokenId (assume que c'est totalSupply après mint)
token_id = nft_contract.functions.totalSupply().call()
print(f"Token ID minté (c'est totalSupply) : {token_id}")

