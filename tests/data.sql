INSERT INTO user (email, display_name, password)
VALUES
    ('test@gmail.com', 'Test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
    ('other@gmail.com', 'Other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO recipe
    (user_id, created, title, author, description, source_url, image_path,
    servings, prep_time, cook_time, instructions)
VALUES 
    (1, '2018-01-01 00:00:00', 'test recipe', 'chef ramsay', 'yummy',
    'http://example.com', 'user_images/whatever.jpg', 2, 5, 10, 'put the bla in the bla
    then do the thing');

INSERT INTO recipe_ingredient_map (recipe_id, input_text, count)
VALUES
    (1, '1tbsp nonsense', 1);
