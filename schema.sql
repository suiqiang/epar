drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  prjname text not null,
  prjdir text not null
); 
