import sqlite3
import data


class Database:
    def __init__(self, db_path: str, ddl_path: str) -> None:
        self.connection: sqlite3.Connection = sqlite3.connect(db_path)
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        with open(ddl_path, "r") as ddl_file:
            ddl_script = ddl_file.read()
            self.cursor.executescript(ddl_script)
        self.connection.commit()

    def get_user(self, user_id: int) -> data.User:
        return NotImplemented

    def get_users(self) -> list[data.User]:
        return NotImplemented

    def get_todo_list(self, user_id: int) -> list[data.Todo]:
        return NotImplemented

    def get_shopping_list(self, user_id: int) -> list[data.Shopping]:
        return NotImplemented

    def get_contacts(self, user_id: int) -> list[data.Contact]:
        return NotImplemented

    def get_categories(self) -> list[data.Category]:
        return NotImplemented

    def get_category(self, category_id: int) -> data.Category:
        return NotImplemented

    def get_ingredients(self) -> list[data.Ingredient]:
        return NotImplemented

    def get_ingredient(self, ingredient_id: int) -> data.Ingredient:
        return NotImplemented

    def get_recipes(self) -> list[data.Recipe]:
        return NotImplemented

    def get_recipe(self, recipe_id: int) -> data.Recipe:
        return NotImplemented

    def get_recipe_ingredients(self, recipe_id: int) -> list[data.RecipeIngredient]:
        return NotImplemented

    def add_category(self, category: data.Category) -> None:
        return NotImplemented

    def add_user(self, user: data.User) -> None:
        return NotImplemented

    def add_todo_list(self, todo: data.Todo) -> None:
        return NotImplemented

    def add_shopping_list(self, shopping: data.Shopping) -> None:
        return NotImplemented

    def remove_todo_list(self, todo_id: int) -> None:
        return NotImplemented

    def remove_shopping_list(self, shopping_id: int) -> None:
        return NotImplemented
