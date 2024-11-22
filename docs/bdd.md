# Base de données

## Tables

- Users(id, mail, password, name)
- Recipes(id, name, difficulty, json, image_url)
- Ingredients(id, name, icon_id)
- Recipes_Ingredients(id_ingredient, id_recipe)
- Contact(id, user_id, name, phone_number, image_url)
- Todo(id, user_id, date, category_id)
- Categories(id, icon_id, name)
- Shopping(user_id; ingredients_id)


