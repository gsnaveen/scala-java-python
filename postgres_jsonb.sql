create table anom1.jb_test ( id integer, jb jsonb);
 
Select * from anom1.jb_test;
 
insert into anom1.jb_test values(1,'{"name": "myname"}');
 
update anom1.jb_test set jb = jb || '{"name2": "myname2"}';

--Will update the existing key if not exisitng will insert
update anom1.jb_test set jb = jsonb_set(jb,'{name}','"myname1"',True);

--Will only update, if the key does not exist then no changes
update anom1.jb_test set jb = jsonb_set(jb,'{namey}','"myname1"',False);

--Will add the key value to the attribute
update anom1.jb_test set jb = jsonb_set(jb,'{namex}','"myname1"',True);
