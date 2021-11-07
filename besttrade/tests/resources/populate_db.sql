-- populate investor
insert into investor (name, status) values ('admin', 'ACTIVE');
insert into investor (name, status) values ('user1', 'ACTIVE');
insert into investor (name, status) values ('user2', 'INACTIVE');
-- Populate accounts
insert into account (investor_id, balance) values (1, 10000);
insert into account (investor_id, balance) values (1, 5000);
insert into account (investor_id, balance) values (2, 12000);