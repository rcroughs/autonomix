import requests
from typing import Optional

url = "http://127.0.0.1:5000"
token_file = ".token"


def register(name, mail, password):
    data = {"name": name, "mail": mail, "password": password}
    try:
        # Envoi de la requête POST
        response = requests.post(url + "/auth/register", json=data)

        # Affichage de la réponse
        if response.status_code == 200:
            print("Enregistrement réussi :", response.json())
        else:
            print(f"Erreur {response.status_code} :", response.text)

    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def login(mail, password) -> Optional[str]:
    data = {"mail": mail, "password": password}
    try:
        # Envoi de la requête POST
        response = requests.post(url + "/auth/login", json=data)
        # Affichage de la réponse
        if response.status_code == 200:
            print("Connexion réussie :", response.json())
            token = response.json()["token"]
            with open(token_file, "w") as f:
                f.write(token)
            return token
        else:
            print(f"Erreur {response.status_code} :", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)
        return None


def get_contacts(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Envoi de la requête GET
        response = requests.get(url + "/contacts", headers=headers)
        # Affichage de la réponse
        if response.status_code == 200:
            print("Liste des contacts :", response.json())
            return response.json()
        else:
            print(f"Erreur {response.status_code} :", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def add_contact(token, name, phone, image):
    try:
        # Envoi de la requête POST
        headers = {"Authorization": f"Bearer {token}"}
        data = {"name": name, "phone_number": phone, "image_url": image}
        response = requests.post(url + "/contacts", headers=headers, json=data)
        # Affichage de la réponse
        if response.status_code == 200:
            print("Contact ajouté :", response.json())
        else:
            print(f"Erreur {response.status_code} :", response.text)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def get_shopping_list(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Envoi de la requête GET
        response = requests.get(url + "/shopping", headers=headers)
        # Affichage de la réponse
        if response.status_code == 200:
            print("Liste de courses :", response.json())
            return response.json()
        else:
            print(f"Erreur {response.status_code} :", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def add_shopping_item(token, id, amount):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Envoi de la requête POST
        data = {"category_id": id, "amount": amount}
        response = requests.post(url + "/shopping", headers=headers, json=data)
        # Affichage de la réponse
        if response.status_code == 200:
            print("Article ajouté :", response.json())
        else:
            print(f"Erreur {response.status_code} :", response.text)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def remove_shopping_item(token, id):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        data = {"id": id}
        response = requests.delete(url + "/shopping", headers=headers, json=data)
        if response.status_code == 200:
            print("Article supprimé :", response.json())
        else:
            print(f"Erreur {response.status_code} :", response.text)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def increment_shopping_item(token, id):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        data = {"id": id}
        response = requests.post(
            url + "/shopping/increment", headers=headers, json=data
        )
        if response.status_code == 200:
            print("Article incrémenté :", response.json())
        else:
            print(f"Erreur {response.status_code} :", response.text)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def decrement_shopping_item(token, id):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        data = {"id": id}
        response = requests.post(
            url + "/shopping/decrement", headers=headers, json=data
        )
        if response.status_code == 200:
            print("Article décrémenté :", response.json())
        else:
            print(f"Erreur {response.status_code} :", response.text)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)
