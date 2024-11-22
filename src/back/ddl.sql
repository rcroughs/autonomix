CREATE TABLE IF NOT EXISTS Users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  mail TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Recipes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  difficulty INTEGER NOT NULL,
  json TEXT NOT NULL,
  image_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  icon_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Recipes_Ingredients (
  recipe_id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  PRIMARY KEY (recipe_id, ingredient_id),
  FOREIGN KEY (recipe_id) REFERENCES Recipes (id),
  FOREIGN KEY (ingredient_id) REFERENCES Ingredients (id)
);

CREATE TABLE IF NOT EXISTS Contacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  image_url TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users (id)
);

CREATE TABLE IF NOT EXISTS Categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  icon_id INTEGER NOT NULL,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Todo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  description TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users (id),
  FOREIGN KEY (category_id) REFERENCES Categories (id)
);

CREATE TABLE IF NOT EXISTS Shopping (
  user_id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  amount INTEGER NOT NULL CHECK (amount >= 1),
  PRIMARY KEY (user_id, ingredient_id),
  FOREIGN KEY (user_id) REFERENCES Users (id),
  FOREIGN KEY (ingredient_id) REFERENCES Ingredients (id)
);

