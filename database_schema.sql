CREATE DATABASE barhive;

-- WAIT TO ADD TABLES UNTIL AFTER THE DATABASE IS CREATED

CREATE TABLE "user" (
    user_id SERIAL NOT NULL,
    username VARCHAR(80) NOT NULL,
    password VARCHAR(80) NOT NULL,
    first_name VARCHAR(80),
    last_name VARCHAR(80),
    email VARCHAR(80),
    about_me VARCHAR(500),
    profile_pic BYTEA,
    banner_pic BYTEA,
    private BOOLEAN DEFAULT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE post (
    post_id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    title varchar(80) NOT NULL,
    content varchar(500) NOT NULL,
    file BYTEA,
    likes INTEGER NOT NULL,
    PRIMARY KEY (post_id)
);

CREATE TABLE user_likes (
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    like_type INTEGER NOT NULL,
    PRIMARY KEY (user_id, post_id)
);