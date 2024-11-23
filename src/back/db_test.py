import db
import data

database = db.Database("db.sqlite", "ddl.sql")


def test_users():
    database.add_user(data.User(None, "Romain", "romain.croughs@gmail.com", "password"))
    result = database.get_user_by_email("romain.croughs@gmail.com")
    assert result is not None


def test_categories():
    database.add_category(data.Category(None, "Test", 0))
    result = database.get_categories()
    assert result is not None


def test_todos():
    user = database.get_user_by_email("romain.croughs@gmail.com")
    if user.id is not None:
        database.add_todo_list(data.Todo(None, user.id, 1))
    else:
        assert False
    assert database.get_todo_list(user.id) is not None


def test_ingredients():
    database.add_ingredient(data.Ingredient(None, "Test", 0))
    result = database.get_ingredients()
    assert result is not None


def test_recipes():
    database.add_recipe(data.Recipe(None, "Test", 1, "", ""))
    result = database.get_recipes()
    assert result is not None


def test_recipe_ingredients():
    recipe = database.get_recipes()[0]
    ingredient = database.get_ingredients()[0]
    if recipe.id is not None and ingredient.id is not None:
        database.add_recipe_ingredient(
            data.RecipeIngredient(recipe.id, ingredient.id, 1)
        )
        result = database.get_recipe_ingredients(recipe.id)
    else:
        assert False
    assert result is not None


def test_contacts():
    database.add_contact(data.Contact(None, 1, "Test", "", ""))
    assert database.get_contacts(1) is not None


def test_shopping_list():
    user = database.get_user_by_email("romain.croughs@gmail.com")
    if user.id is not None:
        database.add_shopping_list(data.Shopping(user.id, 1, 1))
    else:
        assert False
    assert database.get_shopping_list(user.id) is not None
