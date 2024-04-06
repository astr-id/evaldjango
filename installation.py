import subprocess

def installation():
    try:

        # Commande 1 créé les migrations: python3 manage.py makemigrations projetmanagement
        subprocess.run(['python3', 'manage.py', 'makemigrations', 'projetmanagement'], check=True)

        # Commande 2, applique les migrations : python3 manage.py migrate
        subprocess.run(['python3', 'manage.py', 'migrate'], check=True)

        # Commande 3, créé les données : python3 GenererData.py
        subprocess.run(['python3', 'GenererData.py'], check=True)

        # Commande 4, lance le serveur: python3 manage.py runserver 0.0.0.0:8000
        subprocess.run(['python3', 'manage.py', 'runserver', '0.0.0.0:8000'])

    except subprocess.CalledProcessError as e:
        print(f"Erreur: Commande '{e.cmd}' n'a pas renvoyé la valeur 0 : {e.returncode}.")
    except FileNotFoundError:
        print("Erreur: 'python3'n'est pas installé ou n'existe pas.")
    except Exception as e:
        print(f"Une erreur inattendue est apparue: {e}")

if __name__ == "__main__":
    installation()
