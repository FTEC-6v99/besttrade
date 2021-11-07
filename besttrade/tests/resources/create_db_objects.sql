drop table if exists investor;
drop table if exists portfolio;
drop table if exists account;

create table investor (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL
);

create table account (
    account_number INTEGER PRIMARY KEY,
    investor_id INTEGER NOT NULL,
    balance FLOAT NOT NULL,
    FOREIGN KEY(investor_id) REFERENCES investor(id)
)