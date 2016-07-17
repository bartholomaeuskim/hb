drop table if exists users;
drop table if exists vehicle;
drop table if exists code;

create table users (
  id string primary key not null,
  password string not null,
  admin_permission boolean default 0
);

create table vehicle (
  id integer not null auto_increment,
  vin string primary key not null,
  code string not null,
  color_code string,
  option string,
  cif integer,
  departed_date date,
  arrived_date date,
  kaida_reg date,
  sagai_reg date,
  seats string
);

create table code (
  code string not null,
  brand string not null,
  model_name string not null,
  trim_level string not null,
  engine string not null,
  transmission string,
  stop_start boolean
);

insert into users (id, password, admin_permission) values("admin", "hy046790hy", 1);
