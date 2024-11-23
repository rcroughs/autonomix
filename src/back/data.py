from typing import Optional


class User:
    id: Optional[int]
    name: str
    mail: str
    password: str

    def __init__(self, id: Optional[int], name: str, mail: str, password: str):
        self.id = id
        self.name = name
        self.mail = mail
        self.password = password

    def get_id(self) -> Optional[int]:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_mail(self) -> str:
        return self.mail

    def get_password(self) -> str:
        return self.password


class Todo:
    id: Optional[int]
    user_id: int
    category_id: int

    def __init__(self, id: Optional[int], user_id: int, category_id: int):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id

    def get_id(self) -> Optional[int]:
        return self.id

    def get_user_id(self) -> int:
        return self.user_id

    def get_category_id(self) -> int:
        return self.category_id


class Shopping:
    user_id: int
    category_id: int
    amount: int

    def __init__(self, user_id: int, category_id: int, amount: int):
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount

    def get_user_id(self) -> int:
        return self.user_id

    def get_category_id(self) -> int:
        return self.category_id

    def get_amount(self) -> int:
        return self.amount


class RecipeIngredient:
    recipe_id: int
    ingredient_id: int
    amount: int

    def __init__(self, recipe_id: int, ingredient_id: int, amount: int):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.amount = amount

    def get_recipe_id(self) -> int:
        return self.recipe_id

    def get_ingredient_id(self) -> int:
        return self.ingredient_id

    def get_amount(self) -> int:
        return self.amount


class Recipe:
    id: Optional[int]
    name: str
    difficulty: int
    json: str
    image_url: str

    def __init__(
        self, id: Optional[int], name: str, difficulty: int, json: str, image_url: str
    ):
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.json = json
        self.image_url = image_url

    def get_id(self) -> Optional[int]:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_difficulty(self) -> int:
        return self.difficulty

    def get_json(self) -> str:
        return self.json

    def get_image_url(self) -> str:
        return self.image_url


class Ingredient:
    id: Optional[int]
    name: str
    icon_id: int

    def __init__(self, id: Optional[int], name: str, icon_id: int):
        self.id = id
        self.name = name
        self.icon_id = icon_id

    def get_id(self) -> Optional[int]:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_icon_id(self) -> int:
        return self.icon_id


class Category:
    id: Optional[int]
    name: str
    icon_id: int

    def __init__(self, id: Optional[int], name: str, icon_id: int):
        self.id = id
        self.name = name
        self.icon_id = icon_id

    def get_id(self) -> Optional[int]:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_icon_id(self) -> int:
        return self.icon_id


class Contact:
    id: Optional[int]
    user_id: int
    name: str
    phone_number: str
    image_url: str

    def __init__(
        self,
        id: Optional[int],
        user_id: int,
        name: str,
        phone_number: str,
        image_url: str,
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.phone_number = phone_number
        self.image_url = image_url

    def get_id(self) -> Optional[int]:
        return self.id

    def get_user_id(self) -> int:
        return self.user_id

    def get_name(self) -> str:
        return self.name

    def get_phone_number(self) -> str:
        return self.phone_number

    def get_image_url(self) -> str:
        return self.image_url
