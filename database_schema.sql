CREATE DATABASE barhive;

-- WAIT TO ADD TABLES UNTIL AFTER THE DATABASE IS CREATED

CREATE TABLE "user" (
    user_id SERIAL NOT NULL,
    username VARCHAR(80) NOT NULL,
    password VARCHAR(80) NOT NULL,
    first_name VARCHAR(80),
    last_name VARCHAR(80),
    email VARCHAR(80) NOT NULL,
    about_me VARCHAR(500),
    private BOOLEAN DEFAULT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE business (
    business_id SERIAL NOT NULL,
    business_name VARCHAR(80) NOT NULL,
    email VARCHAR(80) NOT NULL,
    password VARCHAR(80) NOT NULL,
    business_description VARCHAR(500),
    address VARCHAR(80),
    city VARCHAR(80),
    state VARCHAR(80),
    zip_code INTEGER,
    phone INTEGER,
    website VARCHAR(80),
    PRIMARY KEY (business_id)
);

CREATE TABLE post (
    post_id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    title varchar(80) NOT NULL,
    content varchar(500) NOT NULL,
    likes INTEGER NOT NULL,
    PRIMARY KEY (post_id)
);

CREATE TABLE user_likes (
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    like_type INTEGER NOT NULL,
    PRIMARY KEY (user_id, post_id)
);

-- post has poster_id which connects to user, business, or admin