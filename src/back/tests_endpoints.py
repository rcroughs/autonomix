from endpoints import app

url= "http://127.0.0.1:5000" # Adresse locale du serveur flask

# ----------Authentification----------
with app.test_client() as client:
    """
    Test de register : Success
    """
    new_user = {
        "name": "pepe",
        "mail": "pepe@musafiri.it",
        "password": "veronicaAI"
    }

    response = client.post(url + "/auth/register", json=new_user)

    if response.status_code == 201:
        print(f"User créé avec succès : code {response.status_code}")
    else:
        print(f"Erreur lors de la création de l'user : code {response.status_code}")

    response = client.post(url + "/auth/register", json=new_user)

    """
    Test de register : Fail, duplicata
    """

    if response.status_code == 201:
        print(f"User créé avec succès : code {response.status_code}")
    else:
        print(f"Erreur lors de la création de l'user : code {response.status_code}")

    """
    Test de connexion : Success
    """
    user_data = {
        "name": "pepe",
        "mail": "pepe@musafiri.it",
        "password": "veronicaAI"
    }

    response = client.post(url + "/auth/login", json=user_data)

    if response.status_code == 200:
        print(f"Connexion réussie : code {response.status_code}")
    else:
        print(f"Erreur lors de la connexion : code {response.status_code}")

    """
    Test de connexion : Fail, user does not exist
    """
    user_data = {
        "name": "Cool guy",
        "mail": "coolguy@ulb.be",
        "password": "coca-cola"
    }

    response = client.post(url + "/auth/login", json=user_data)

    if response.status_code == 200:
        print(f"Connexion réussie : code {response.status_code}")
    else:
        print(f"Erreur lors de la connexion : code {response.status_code}")

