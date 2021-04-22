create table exchange(
    id integer primary key AUTOINCREMENT,
    open_time real
);
create table sumbols(
    id_smb integer primary key AUTOINCREMENT,
    exchange integer,
    name varchar(255),
    price real,
    FOREIGN KEY (exchange) REFERENCES exchange (id)
);
