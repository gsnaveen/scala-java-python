
with temp
as (
   select emp_id ,emp_name,dated, row_number() over ( partition by emp_id order by dated desc ) rank1
   from schema1.dupetable
)
delete from schema1.dupetable dd where exists (select 1 from temp t1 where dd.emp_id = t1.emp_id and dd.dated = t1.dated and rank1 > 1)

with temp
as (
   select emp_id ,emp_name,dated, row_number() over ( partition by emp_id order by dated desc ) rank1
   from schema1.dupetable
)
delete from schema1.dupetable dd USING temp t1 where dd.emp_id = t1.emp_id and dd.dated = t1.dated and rank1 > 1
