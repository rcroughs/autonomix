import sqlite3
import data


class Database:
    def __init__(self, db_path: str, ddl_path: str) -> None:
        self.connection: sqlite3.Connection = sqlite3.connect(
            db_path, check_same_thread=False
        )
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        with open(ddl_path, "r") as ddl_file:
            ddl_script = ddl_file.read()
            self.cursor.executescript(ddl_script)
        self.connection.commit()

    def get_user(self, user_id: int) -> data.User:
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()

        if result:
            return data.User(result[0], result[1], result[2], result[3])

    def get_user_by_email(self, email: str) -> data.User:
        self.cursor.execute("SELECT * FROM users WHERE mail = ?", (email,))
        result = self.cursor.fetchone()

        if result:
            return data.User(result[0], result[1], result[2], result[3])

    def get_users(self) -> list[data.User]:
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        return [data.User(row[0], row[1], row[2], row[3]) for row in result]

    def get_todo_list(self, user_id: int) -> list[data.Todo]:
        self.cursor.execute("SELECT * FROM todo WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchall()
        return [data.Todo(row[0], row[1], row[2]) for row in result]

    def get_shopping_list(self, user_id: int) -> list[data.Shopping]:
        self.cursor.execute("SELECT * FROM shopping WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchall()
        return [data.Shopping(row[0], row[1], row[2]) for row in result]

    def get_contacts(self, user_id: int) -> list[data.Contact]:
        self.cursor.execute("SELECT * FROM contacts WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchall()
        return [data.Contact(row[0], row[1], row[2], row[3], row[4]) for row in result]

    def get_categories(self) -> list[data.Category]:
        self.cursor.execute("SELECT * FROM categories")
        result = self.cursor.fetchall()
        return [data.Category(row[0], row[1], row[2]) for row in result]

    def get_category(self, category_id: int) -> data.Category:
        self.cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        result = self.cursor.fetchone()
        return data.Category(result[0], result[1], result[2])

    def get_ingredients(self) -> list[data.Ingredient]:
        self.cursor.execute("SELECT * FROM ingredients")
        result = self.cursor.fetchall()
        return [data.Ingredient(row[0], row[1], row[2]) for row in result]

    def get_ingredient(self, ingredient_id: int) -> data.Ingredient:
        self.cursor.execute("SELECT * FROM ingredients WHERE id = ?", (ingredient_id,))
        result = self.cursor.fetchone()
        return data.Ingredient(result[0], result[1], result[2])

    def get_ingredient_by_name(self, name: str) -> data.Ingredient:
        self.cursor.execute("SELECT * FROM ingredients WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        return data.Ingredient(result[0], result[1], result[2])

    def get_recipes(self) -> list[data.Recipe]:
        self.cursor.execute("SELECT * FROM recipes")
        result = self.cursor.fetchall()
        return [data.Recipe(row[0], row[1], row[2], row[3], row[4]) for row in result]

    def get_recipe(self, recipe_id: int) -> data.Recipe:
        self.cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        result = self.cursor.fetchone()
        return data.Recipe(result[0], result[1], result[2], result[3], result[4])

    def get_last_inserted_recipe(self) -> data.Recipe:
        # Requête SQL pour obtenir la dernière recette insérée
        self.cursor.execute("SELECT * FROM recipes ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()

        if result:
            return data.Recipe(result[0], result[1], result[2], result[3], result[4])

    def get_recipe_ingredients(self, recipe_id: int) -> list[data.RecipeIngredient]:
        self.cursor.execute(
            "SELECT * FROM recipes_ingredients WHERE recipe_id = ?", (recipe_id,)
        )
        result = self.cursor.fetchall()
        return [data.RecipeIngredient(row[0], row[1], row[2]) for row in result]

    def add_category(self, category: data.Category) -> None:
        self.cursor.execute(
            "INSERT INTO categories (id, name, icon_id) VALUES (?, ?, ?)",
            (category.id, category.name, category.icon_id),
        )

    def add_user(self, user: data.User) -> None:
        self.cursor.execute(
            "INSERT INTO users (name, mail, password) VALUES (?, ?, ?)",
            (user.name, user.mail, user.password),
        )

    def add_todo_list(self, todo: data.Todo) -> None:
        self.cursor.execute(
            "INSERT INTO todo (id, user_id, category_id) VALUES (?, ?, ?)",
            (todo.id, todo.user_id, todo.category_id),
        )

    def add_shopping_list(self, shopping: data.Shopping) -> None:
        self.cursor.execute(
            "INSERT INTO shopping (user_id, ingredient_id, amount) VALUES (?, ?, ?)",
            (shopping.user_id, shopping.category_id, shopping.amount),
        )

    def add_recipe(self, recipe: data.Recipe) -> None:
        self.cursor.execute(
            "INSERT INTO recipes (name, difficulty, json, image_url) VALUES (?, ?, ?, ?)",
            (
                recipe.name,
                recipe.difficulty,
                recipe.json,
                recipe.image_url,
            ),
        )

    def add_ingredient(self, ingredient: data.Ingredient) -> None:
        self.cursor.execute(
            "INSERT INTO ingredients (name, icon_id) VALUES (?, ?)",
            (ingredient.name, ingredient.icon_id),
        )

    def add_recipe_ingredient(self, recipe_ingredient: data.RecipeIngredient) -> None:
        self.cursor.execute(
            "INSERT INTO recipes_ingredients (recipe_id, ingredient_id, amount) VALUES (?, ?, ?)",
            (
                recipe_ingredient.recipe_id,
                recipe_ingredient.ingredient_id,
                recipe_ingredient.amount,
            ),
        )

    def add_contact(self, contact: data.Contact) -> None:
        self.cursor.execute(
            "INSERT INTO contacts (user_id, name, phone_number, image_url) VALUES (?, ?, ?, ?)",
            (
                contact.user_id,
                contact.name,
                contact.phone_number,
                contact.image_url,
            ),
        )

    def remove_todo_list(self, todo_id: int) -> None:
        self.cursor.execute("DELETE FROM todo WHERE id = ?", (todo_id,))

    def remove_shopping_list(self, shopping_id: int) -> None:
        self.cursor.execute("DELETE FROM shopping WHERE id = ?", (shopping_id,))

    def remove_shopping_item(self, user_id: int, ingredient_id: int) -> None:
        self.cursor.execute(
            "DELETE FROM shopping WHERE user_id = ? AND ingredient_id = ?",
            (user_id, ingredient_id),
        )

    def increment_shopping_item(self, user_id: int, ingredient_id: int) -> None:
        self.cursor.execute(
            "UPDATE shopping SET amount = amount + 1 WHERE user_id = ? AND ingredient_id = ?",
            (user_id, ingredient_id),
        )

    def get_shopping_item_amount(self, user_id: int, ingredient_id: int) -> int:
        self.cursor.execute(
            "SELECT amount FROM shopping WHERE user_id = ? AND ingredient_id = ?",
            (user_id, ingredient_id),
        )
        result = self.cursor.fetchone()

    def decrement_shopping_item(self, user_id: int, ingredient_id: int) -> None:
        if self.get_shopping_item_amount(user_id, ingredient_id) > 1:
            self.cursor.execute(
                "UPDATE shopping SET amount = amount - 1 WHERE user_id = ? AND ingredient_id = ?",
                (user_id, ingredient_id),
            )
        else:
            self.remove_shopping_item(user_id, ingredient_id)

    def user_exists(self, email: str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE mail = ?", (email,))
        return self.cursor.fetchone() is not None

    def valid_password(self, email: str, password: str) -> bool:
        self.cursor.execute(
            "SELECT * FROM users WHERE mail = ? AND password = ?", (email, password)
        )
        return self.cursor.fetchone() is not None

    def commit(self) -> None:
        self.connection.commit()
