from datetime import datetime, timedelta
from encodings.base64_codec import base64_encode
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from db import Database
from data import *
from typing import Optional
import os


def create_app(testing=False):
    app = Flask(__name__)
    # Token d'authentification
    app.config["SECRET_KEY"] = "autonomixmax"

    if testing:
        app.db = Database(":memory:", "ddl.sql")
    else:
        app.db = Database("database.db", "ddl.sql")
    return app


app = create_app()
db = app.db


def check_auth(token):
    token = token.split(" ")[1]
    print(token)
    try:
        jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    return True


def get_user_id(token) -> Optional[int]:
    token = token.split(" ")[1]
    try:
        return jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
            "user_id"
        ]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# -------------Authentification-------------
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json  # Extraction du Json

    # Vérification de l'intégrité des données
    if not data:
        return jsonify({"error": "Invalid Data"}), 400

    user_id = -1
    if db.get_user_by_email(data["mail"]):
        user_id = db.get_user_by_email(data["mail"]).id

    user = db.get_user(user_id)

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid password"}), 401

    token = jwt.encode(
        {"user_id": user.id},
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return jsonify({"message": "Login successful", "token": token}), 200


@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    existing_user = db.get_user_by_email(data["mail"])
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    secured_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(
        id=None, name=data["name"], mail=data["mail"], password=secured_password
    )
    db.add_user(new_user)
    db.commit()

    return jsonify({"message": "User registered successfully"}), 201


# -------------Ingredients---------
@app.route("/ingredient", methods=["GET"])
def get_ingredients():
    # Fetch les ingrédients
    ingredients = db.get_ingredients()

    # Formatage
    ingredients_list = [
        {"id": ingredient.id, "name": ingredient.name, "icon_id": ingredient.icon_id}
        for ingredient in ingredients
    ]
    return jsonify(ingredients_list), 200


@app.route("/ingredient", methods=["POST"])
def post_ingredient():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid Data"}), 400

    new_ingredient = Ingredient(id=None, name=data["name"], icon_id=data["icon_id"])
    db.add_ingredient(new_ingredient)
    db.commit()

    return jsonify({"message": "ingredient added successfully"}), 200


# -------------Recipes-------------
@app.route("/recipes", methods=["GET"])
def get_recipes():
    # Fetch les recettes
    recipes = db.get_recipes()

    # Formatage
    recipes_list = [
        {
            "id": recipe.id,
            "name": recipe.name,
            "difficulty": recipe.difficulty,
            "image_url": recipe.image_url,
        }
        for recipe in recipes
    ]
    return jsonify(recipes_list), 200


@app.route("/recipes", methods=["POST"])
def post_recipe():
    data = request.json

    if not check_auth(request.headers.get("Authorization")):
        return jsonify({"error": "Unauthorized"}), 401

    if not data:
        return jsonify({"error": "Invalid Data"}), 400

    new_recipe = Recipe(
        id=None,
        name=data["name"],
        difficulty=data["difficulty"],
        json=data["json"],
        image_url=data["image_url"],
    )
    recipe_id = NotImplemented  # db.add_recipe(new_recipe)

    return jsonify({"message": "Recipe added successfully", "id": recipe_id}), 201


# -------------Todo_-------------
@app.route("/todo", methods=["GET"])
def get_todo_list():
    # Récupération du user_id
    if not check_auth(request.headers.get("Authorization")):
        return jsonify({"error": "Unauthorized"}), 401
    jwt = request.headers.get("Authorization")
    user_id = jwt.decode(jwt, app.config["SECRET_KEY"], algorithms=["HS256"])["user_id"]

    # Fetch des todo_
    todos = db.get_todo_list(user_id)
    todos_list = [
        {"id": todo.id, "user_id": todo.user_id, "category_id": todo.category_id}
        for todo in todos
    ]
    return jsonify(todos_list), 200


@app.route("/todo", methods=["POST"])
def add_todo():
    data = request.json  # Extraction des données JSON
    user_id = get_user_id(request.headers.get("Authorization"))
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    # Vérification des champs nécessaires
    if not data:
        return jsonify({"error": "Invalid Data"}), 400

    # Création de la nouvelle tâche
    new_todo = Todo(
        id=None,  # ID généré automatiquement
        user_id=user_id,
        category_id=data["category_id"],
    )
    db.add_todo_list(new_todo)
    db.commit()

    return jsonify({"message": "Todo added successfully"}), 201


# -------------Shopping-------------
@app.route("/shopping", methods=["GET"])
def get_shopping_list():
    # Récupération du user_id
    user_id = get_user_id(request.headers.get("Authorization"))
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    # Fetch de la liste d'achats pour l'utilisateur
    shopping_list = db.get_shopping_list(user_id)
    shopping_items = [
        {
            "user_id": item.user_id,
            "category_id": item.category_id,
            "amount": item.amount,
        }
        for item in shopping_list
    ]
    return jsonify(shopping_items), 200


@app.route("/shopping", methods=["POST"])
def add_shopping_item():
    data = request.json
    user_id = get_user_id(request.headers.get("Authorization"))
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401
    # Vérification des champs nécessaires
    if not data:
        return jsonify({"error": "Invalid Data"}), 400

    # Création d'un nouvel élément d'achat
    new_item = Shopping(
        user_id=user_id, category_id=data["category_id"], amount=data["amount"]
    )
    db.add_shopping_list(new_item)
    db.commit()

    return jsonify({"message": "Shopping item added successfully"}), 201


# -------------Contacts-------------
@app.route("/contacts", methods=["GET"])
def get_contacts():
    # Récuperer le user_id
    user_id = get_user_id(request.headers.get("Authorization"))
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    # Fetch de la liste de contacts
    contacts = db.get_contacts(user_id)
    contacts_list = [
        {
            "id": contact.id,
            "user_id": contact.user_id,
            "name": contact.name,
            "phone_number": contact.phone_number,
            "image_url": contact.image_url,
        }
        for contact in contacts
    ]
    return jsonify(contacts_list), 200


@app.route("/contacts", methods=["POST"])
def add_contact():
    data = request.json  # Extraction des données JSON

    # Vérification des champs nécessaires
    if not data:
        return jsonify({"error": "Invalid Data"}), 400

    # Vérification de l'authentification
    user_id = get_user_id(request.headers.get("Authorization"))
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    # Création d'un nouveau contact
    new_contact = Contact(
        id=None,  # ID généré automatiquement
        user_id=user_id,
        name=data["name"],
        phone_number=data["phone_number"],
        image_url=data["image_url"],
    )
    db.add_contact(new_contact)
    db.commit()

    return jsonify({"message": "Contact added successfully"}), 201


# -------------Image-------------
@app.route("/image", methods=["GET"])
def get_image():
    # Récuperer le user_id
    img_name = request.args.get("img_name", type=int)
    if not img_name:
        return jsonify({"error": "Image Name is missing"}), 400

    path = "img"
    img_path = os.path.join(path, img_name)
    if os.path.exists(img_path):
        with open(img_path, "rb") as image:
            encoded_image = base64_encode(image.read()).decode("utf-8")
            return jsonify({"image": encoded_image})
    else:
        return jsonify({"message": f"L'image {img_name} n'existe pas"})
