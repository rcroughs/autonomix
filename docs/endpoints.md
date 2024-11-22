# Endpoints

## Authentification

- POST /login
- POST /register

## Recipes

- GET /recipes: te retourne default 50 recettes
```json
[
  {
    "id": "id"
    "name": "name"
    "difficulty": 2
    "image_url": "url"
  }
]
```
- GET /recipes/{id}: retourne toutes les infos d'une recettes (meme json sauf que ca renvoie les ingredients dans une liste et le json)
- POST /recipes: poster une recette

## Todo

- GET /todo: retourne les todos
```json
[
  {
    "id"
    "date"
    "category"
  }
]
```
- GET /todo/{id}: retourne toutes les infos d'un todo (vérifier que todo appartient l'utilisateur)
- POST /todo

## Shopping

- GET /shopping

```json
[
  {
    "id"
    "date"
    "ingredient"
  }
]
```
- POST /shopping
- DELETE /shopping/{id}

## Contacts

- GET /contacts
```json
[
  {
    "name"
    "phoneNumber"
    "image_url"
  }
]
```
- POST /contacts
- DELETE /contacts

## Image

- GET /image/{name}: renvoie l'image
