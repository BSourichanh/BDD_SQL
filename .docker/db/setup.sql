-- auto-generated definition
create schema test_1 collate utf8mb4_unicode_ci;
create schema test_2 collate utf8mb4_unicode_ci;
create schema test_3 collate utf8mb4_unicode_ci;
create schema test_5 collate utf8mb4_unicode_ci;
create schema test_6 collate utf8mb4_unicode_ci;
create schema test_7 collate utf8mb4_unicode_ci;
create schema query_playground collate utf8mb4_unicode_ci;

create table if not exists test_1.users
(
    id     int auto_increment,
    name  varchar(255) null,
    salary int,
    constraint users_id_uindex
        unique (id)
);
insert into test_1.users (id, name, salary)
VALUES (2304,'Tim', 400),
       (1996,'Faab', 250),
       (8181,'Jesper', 225);

create table if not exists test_2.users
(
    id     int auto_increment,
    name  varchar(255) null,
    salary int,
    constraint users_id_uindex
        unique (id)
);
insert into test_2.users (id, name, salary)
VALUES (2304, 'Tim', 400),
       (1996, 'Faab', 250),
       (8181, 'Jesper', 225),
       (3698, 'Max', 333),
       (9999, 'Dennis', 987),
       (7530, 'Mick', 150),
       (147, 'Jacco', 10);

create table if not exists test_2.department
(
    id         int auto_increment,
    name      varchar(255) null,
    manager_id int,
    constraint department_id_uindex
        unique (id)
);
insert into test_2.department (id, name, manager_id)
VALUES (1, 'Headvillage', 2304),
       (4, 'Mob', 147),
       (7, 'Mountain', 9999),
       (9, 'Amstelpeat', 3698);

create table if not exists test_2.employees
(
    department_id int,
    user_id       int
);
insert into test_2.employees (department_id, user_id)
VALUES (1, 2304),
       (4, 2304),
       (4, 147),
       (4, 7530),
       (7, 2304),
       (7, 9999),
       (7, 3698),
       (9, 2304),
       (9, 1996),
       (9, 8181),
       (9, 9999),
       (9, 3698),
       (9, 7530),
       (9, 147);

alter table test_2.users
    add primary key (id);

alter table test_2.department
    add primary key (id);


#TEST 3
create table if not exists test_3.customer
(
    id   varchar(255),
    name varchar(255) null,
    iban varchar(255) null
);
insert into test_3.customer (id, name, iban)
VALUES ('45b35f81-8faa-46c5-801f-5a96b7a67e99', 'Dennis', 'NL01TEST1234567890'),
       ('37e08b4a-4af9-4fbf-a82a-679fd69988f4', 'Becca', 'NL09FAKE9876543210'),
       ('02147ae2-44eb-47ce-9b2a-a19e1aa19848', 'Fret', 'DE88TAXI8529637140'),
       ('57a7b554-63cb-4b61-b2ad-6c28a410185e', 'Student', 'BE66GENT4206942069');

create table if not exists test_3.product
(
    name        varchar(255),
    description varchar(255) null,
    price       float        null
);
insert into test_3.product (name, description, price)
VALUES ('Stereo Headset',
        'Handle phone calls handsfree with this stylish headset Lightweight and comfortable, this handsfree kit enables you to carry on conversations while you continue to do other things.',
        7.4),
       ('Universal USB C Mains Charger',
        'Supports 4 power profiles so you can use with your laptop, phone, tablet & wearables.', 13.55),
       ('Dashcam', 'Full 1080P dashcam for front or back windows of your camera', 39.94);



create table if not exists test_3.bought_last_month
(
    customer_id  varchar(255),
    product_name varchar(255) null,
    amount       int
);
insert into test_3.bought_last_month (customer_id, product_name, amount)
VALUES ('37e08b4a-4af9-4fbf-a82a-679fd69988f4', 'Universal USB C Mains Charger', 1),
       ('37e08b4a-4af9-4fbf-a82a-679fd69988f4', 'Universal USB C Mains Charger', 2),
       ('37e08b4a-4af9-4fbf-a82a-679fd69988f4', 'Universal USB C Mains Charger', 3),
       ('45b35f81-8faa-46c5-801f-5a96b7a67e99', 'Stereo Headset', 1),
       ('45b35f81-8faa-46c5-801f-5a96b7a67e99', 'Stereo Headset', 1),
       ('45b35f81-8faa-46c5-801f-5a96b7a67e99', 'Dashcam', 1),
       ('02147ae2-44eb-47ce-9b2a-a19e1aa19848', 'Dashcam', 2);

-- TEST 4
create table if not exists test_5.scores
(
    id     int auto_increment,
    player varchar(255),
    score  int,
    constraint scores_id_uindex
        unique (id)
);
alter table test_5.scores
    add primary key (id);

insert into test_5.scores (player, score)
VALUES ('tim', 11),
       ('tim', 19),
       ('tim', 6),
       ('tim', 13),
       ('tim', 1),
       ('tim', -1),
       ('tim', 7),
       ('tim', 12),
       ('tim', 19),
       ('tim', 18),
       ('jan', -1),
       ('jan', 1),
       ('jan', 2),
       ('jan', 3),
       ('jan', 4),
       ('jan', 5),
       ('jan', 6),
       ('jan', 8),
       ('jan', 12),
       ('jan', 14),
       ('jan', 16),
       ('jan', 19),
       ('jan', 21),
       ('kees', -12),
       ('kees', -11),
       ('kees', -22),
       ('kees', -9),
       ('kees', -6),
       ('kees', -3),
       ('kees', -5),
       ('kees', -2),
       ('kees', -6),
       ('klass', 1),
       ('klass', -1),
       ('klass', 1),
       ('klass', -2),
       ('klass', 1);


-- TEST 6


create table if not exists test_6.bills_amsterdam
(
    id         int auto_increment,
    bill_id    int,
    euro_cache int,
    employee   varchar(255),
    constraint bills_amsterdam_id_uindex
        unique (id)
);

create table if not exists test_6.bills_haarlem
(
    id         int auto_increment,
    bill_id    int,
    euro_cache int,
    employee   varchar(255),
    constraint bills_haarlem_id_uindex
        unique (id)
);

create table if not exists test_6.bills_leiden
(
    id         int auto_increment,
    bill_id    int,
    euro_cache int,
    employee   varchar(255),
    constraint bills_leiden_id_uindex
        unique (id)
);

create table if not exists test_6.bills_groningen
(
    id         int auto_increment,
    bill_id    int,
    euro_cache int,
    employee   varchar(255),
    constraint bills_groningen_id_uindex
        unique (id)
);

create table if not exists test_6.bills_antwerpen
(
    id         int auto_increment,
    bill_id    int,
    euro_cache int,
    employee   varchar(255),
    constraint bills_antwerpen_id_uindex
        unique (id)
);

insert into test_6.bills_amsterdam (bill_id, euro_cache, employee)
values (12, 11, 'Tim'),
       (13, 14, 'Damjan'),
       (15, 19, 'Tim'),
       (18, 1, 'Amy'),
       (19, 0, 'Grey'),
       (29, 23, 'Jort');

insert into test_6.bills_haarlem (bill_id, euro_cache, employee)
values (6, 12, 'Ray'),
       (24, 111, 'Romy');

insert into test_6.bills_leiden (bill_id, euro_cache, employee)
values (14, 5, 'Gerrit'),
       (16, 1, 'Dagomar'),
       (20, 3, 'Dagomar'),
       (21, 4, 'Dagomar'),
       (22, 33, 'Gerrit'),
       (23, 0, 'Gerrit');

insert into test_6.bills_groningen (bill_id, euro_cache, employee)
values (7, 2, 'Danny'),
       (11, 1, 'Erica'),
       (17, 2, 'Erica'),
       (25, 1, 'Erica'),
       (26, 2, 'Danny'),
       (27, 1, 'Danny'),
       (28, 2, 'Erica');

insert into test_6.bills_antwerpen (bill_id, euro_cache, employee)
values (1, 2, 'Kobe'),
       (2, 4, 'Jari'),
       (3, 3, 'Iza'),
       (4, 3, 'Iza'),
       (5, 3, 'Iza'),
       (8, 1, 'Kobe'),
       (9, 2, 'Jari'),
       (10, 12, 'Iza');

# TEST 7
create table if not exists test_7.message
(
    id         int auto_increment,
    char_message    int,
    constraint message_id_uindex
        unique (id)
);
insert into test_7.message (char_message)
values
    (72),
    (101),
    (108),
    (108),
    (111),
    (32),
    (87),
    (111),
    (114),
    (108),
    (100);


# TEST 8 mais qui est le 9 de sqlBattle le 8 étant vraiment complexe sur les tables du test 6

