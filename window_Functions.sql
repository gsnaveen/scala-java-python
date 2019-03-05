

select cust_id,item_id
, sum(amt) over (partition by cust_id order by item_id desc) runningSum
, max(item_id) over() max_all
, max(item_id) over(partition by cust_id) maxByCust
, count(*) over()
, round(count(*) over() * .5) 
, floor(count(*) over() * .5) flr
, row_number() over() rownum
, row_number() over(partition by cust_id) rownumbyCustitem
, abs(-10)
, case when row_number() over() <= floor(count(*) over() * .5) then True else False end toFilter
,first_value(item_id) over (partition by cust_id) firstValue
,last_value(item_id) over (partition by cust_id) lastValue
,lead(item_id,1) over (partition by cust_id order by item_id ) Lead
,lag(item_id ,1) over (partition by cust_id order by item_id ) lag
from schema1.sales


CREATE TABLE schema1.sales
(
  cust_id bigint,
  item_id bigint,
  amt bigint
)
WITH (
  OIDS=FALSE
);
ALTER TABLE schema1.sales
  OWNER TO postgres;


INSERT INTO schema1.sales(
            cust_id, item_id, amt)
    VALUES (1, 1, 10),
	   (1, 2, 10),
	   (1, 3, 10),
	   (2, 1, 10),
	   (2, 2, 10);
