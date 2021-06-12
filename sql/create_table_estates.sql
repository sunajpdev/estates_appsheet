DROP TABLE estates;

CREATE TABLE estates  (
  id text primary key,
  note text,
  price numeric(8,0) not null,
  shop text, 
  place text not null, 
  prefecture text not null, 
  city text not null, 
  station text, 
  route text, 
  work text, 
  area numeric(8,2), 
  buildingarea numeric(8,2), 
  buildingyear text, 
  ldk text, 
  url text, 
  created timestamp not null default current_timestamp
);

CREATE INDEX on estates(prefecture, city, station, route);

