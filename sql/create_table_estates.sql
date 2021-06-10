CREATE TABLE estates  (
  id text primary key,
  note text,
  price numeric(8,0),
  shop text, 
  place text, 
  prefecture text, 
  city text, 
  station text, 
  route text, 
  work text, 
  area numeric(8,2), 
  buildingarea numeric(8,2), 
  buildingyear text, 
  ldk text, 
  url text, 
  created timestamp
);

CREATE INDEX on estates(prefecture, city, station, route);

