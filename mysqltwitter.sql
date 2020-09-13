USE master;

if exists (select * from sysdatabases where name='TwitterProject') then
        drop database TwitterProject
end if;


CREATE DATABASE TwitterProject;


use TwitterProject;


DROP TABLE MENTIONS;
DROP TABLE HASHTAGS;
DROP TABLE TWEETS;
DROP TABLE USERS;
DROP TABLE SEARCHES;
DROP TABLE RESEARCHERS;
DROP TABLE PLACES;

-- drop table place

CREATE TABLE RESEARCHERS (
    id    INT,
    full_name  VARCHAR(60) NOT NULL,
    profile    NVARCHAR(500),
    PRIMARY KEY(id)
);

INSERT INTO RESEARCHERS VALUES (1, 'Ana Laura Rodriguez',
                  'DB student student at Tec');
INSERT INTO RESEARCHERS VALUES (2, 'Jesus Lopez',
                  'DB student student at Tec');
INSERT INTO RESEARCHERS VALUES (3, 'Rafael Eduardo Aguirre',
                  'DB student student at Tec');
INSERT INTO RESEARCHERS VALUES (4, 'Diego Kaleb Samano',
                  'DB student student at Tec');

CREATE TABLE SEARCHES (
    id            INT,
    description   NVARCHAR(500),
    researcher_id INT,
    PRIMARY KEY(id),
    FOREIGN KEY(researcher_id) references RESEARCHERS(id)
);

INSERT INTO SEARCHES VALUES(1, 'Search tweets containing Harry Styles', 1);
INSERT INTO SEARCHES VALUES(2, 'Search tweets containing League of Legends', 2);
INSERT INTO SEARCHES VALUES(3, 'Search tweets containing NBA', 3);
INSERT INTO SEARCHES VALUES(4, 'Search tweets containing NFL season', 4);

CREATE TABLE USERS (
    id              BIGINT,
    verified        TINYINT,
    followers_count BIGINT,
    PRIMARY KEY(id)
);

-- create table place
CREATE TABLE PLACES (
    id              NVARCHAR(500),
    country_code    NVARCHAR(500),
    name            NVARCHAR(500),
    PRIMARY KEY(id)
);

-- añadir variables de read_tweets
CREATE TABLE TWEETS (
    id                  BIGINT,
    tweet_text          NVARCHAR(500),
    `user`              BIGINT,
    favorite_count      BIGINT,
    retweet_count       BIGINT,
    search_id           INT,
    place_id            NVARCHAR(500),
    PRIMARY KEY(id),
    FOREIGN KEY(`user`) references USERS(id),
    FOREIGN KEY(search_id) references SEARCHES(id),
    FOREIGN KEY(place_id) references PLACES(id)
);

CREATE TABLE MENTIONS (
    tweet_id        BIGINT,
    mention         NVARCHAR(500),
    PRIMARY KEY(tweet_id, mention),
    FOREIGN KEY(tweet_id) REFERENCES TWEETS(id)
);

CREATE TABLE HASHTAGS (
    tweet_id    BIGINT,
    hashtag     NVARCHAR(500),
    PRIMARY KEY(tweet_id, hashtag),
    FOREIGN KEY(tweet_id) references TWEETS(id)
);

