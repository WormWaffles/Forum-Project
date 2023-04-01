CREATE DATABASE barhive;

-- WAIT TO ADD TABLES UNTIL AFTER THE DATABASE IS CREATED

CREATE TABLE "user" (
    user_id SERIAL NOT NULL,
    username VARCHAR(80) NOT NULL,
    password VARCHAR(80) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE post (
    post_id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    title varchar(80) NOT NULL,
    content varchar(500) NOT NULL,
    file varchar(255) NOT NULL,
    likes INTEGER NOT NULL,
    PRIMARY KEY (post_id)
);