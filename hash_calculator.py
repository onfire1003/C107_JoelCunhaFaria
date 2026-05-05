import hashlib
import os


def hash_text(text):
    """Retourne le hash SHA-256 d'un texte."""
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    return sha256.hexdigest()


def hash_file(file_path):
    """Retourne le hash SHA-256 d'un fichier."""
    sha256 = hashlib.sha256()

    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        print("Erreur : fichier introuvable.")
    except PermissionError:
        print("Erreur : permission refusée.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

    return None


def save_hash_to_file(hash_value):
    """Sauvegarde le hash dans un fichier texte."""
    try:
        with open("hash_output.txt", "a") as f:
            f.write(hash_value + "\n")
        print("Hash sauvegardé dans hash_output.txt")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")


def main():
    while True:
        print("\nChoisissez une option :")
        print("[1] Hacher un texte")
        print("[2] Hacher un fichier")
        print("[0] Quitter")

        choice = input("Votre choix : ").strip()

        if choice == "1":
            text = input("Entrez le texte à hacher : ").strip()

            if not text:
                print("Erreur : le texte ne peut pas être vide.")
                continue

            result = hash_text(text)
            print(f"SHA-256 : {result}")

            save = input("Voulez-vous sauvegarder le résultat ? (o/n) : ").lower()
            if save == "o":
                save_hash_to_file(result)

        elif choice == "2":
            file_path = input("Entrez le chemin du fichier : ").strip()

            if not file_path:
                print("Erreur : chemin vide.")
                continue

            if not os.path.exists(file_path):
                print("Erreur : fichier introuvable.")
                continue

            result = hash_file(file_path)
            if result:
                print(f"SHA-256 : {result}")

                save = input("Voulez-vous sauvegarder le résultat ? (o/n) : ").lower()
                if save == "o":
                    save_hash_to_file(result)

        elif choice == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

try:
    main()
except KeyboardInterrupt:
    print("\nLe programme a été interrompu")