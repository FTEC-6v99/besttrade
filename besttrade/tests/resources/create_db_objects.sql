drop table if exists investor;
drop table if exists portfolio;
drop table if exists account;

create table investor (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL
);