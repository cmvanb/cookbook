DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS recipe_tag;
DROP TABLE IF EXISTS recipe_tag_map;
DROP TABLE IF EXISTS ingredient;
DROP TABLE IF EXISTS recipe_ingredient_map;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE recipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT NOT NULL,
    source_url TEXT NOT NULL,
    image_path TEXT NOT NULL,
    servings INTEGER NOT NULL,
    prep_time INTEGER NOT NULL,
    cook_time INTEGER NOT NULL,
    instructions TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE recipe_tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE recipe_tag_map (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipe (id),
    FOREIGN KEY (tag_id) REFERENCES recipe_tag (id)
);

CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    base_unit TEXT NOT NULL,
    base_weight REAL NOT NULL
);

CREATE TABLE recipe_ingredient_map (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    -- ingredient_id INTEGER NOT NULL,
    input_text TEXT NOT NULL,
    count REAL NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    -- FOREIGN KEY (ingredient_id) REFERENCES ingredient (id)
);
