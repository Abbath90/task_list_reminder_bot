create table category(
    id integer primary key,
    name varchar(255),
    aliases text
);

create table tasks(
    id integer primary key,
    created datetime,
    category_id integer,
    text text,
    FOREIGN KEY(category_id) REFERENCES category(id)
);

insert into category (id, name, aliases)
values
    (0, "daily", "daily, d"),
    (1, "hourly", "hourly, h"),
    (2, "single", "single, s, one"),
    (3, "alarm", "alarm, a");