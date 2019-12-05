

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
---Running Sum
CREATE TABLE schema1.subs_revenue
(
  user_id bigint,
  subscription_date date,
  revenue bigint
)
WITH (
  OIDS=FALSE
);
ALTER TABLE schema1.subs_revenue
  OWNER TO postgres;

delete from schema1.subs_revenue;

INSERT INTO schema1.subs_revenue(
            user_id, subscription_date, revenue)
    VALUES (10,'2001-01-01', 100),
	   (20,'2010-09-09',150),
	   (30,'2002-02-01',200),
	   (40,'2005-05-03',300);

Window Function:
select subscription_date,sum(revenue) over(order by subscription_date)
from schema1.subs_revenue
order by subscription_date

Self Join:
SELECT  a.user_id,a.revenue,sum(b.revenue) runningSum
  FROM schema1.subs_revenue a inner join schema1.subs_revenue b on a.user_id >= b.user_id
 group by a.user_id,a.revenue
 order by runningSum

-- Rows for the window functions:
COUNT(DISTINCT a) OVER (PARTITION BY c ORDER BY d ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)

(ROWS | RANGE) BETWEEN (UNBOUNDED | [num]) PRECEDING AND ([num] PRECEDING | CURRENT ROW | (UNBOUNDED | [num]) FOLLOWING)
(ROWS | RANGE) BETWEEN CURRENT ROW AND (CURRENT ROW | (UNBOUNDED | [num]) FOLLOWING)
(ROWS | RANGE) BETWEEN [num] FOLLOWING AND (UNBOUNDED | [num]) FOLLOWING
							 
RANK
ROW_NUMBER
DENSE_RANK
CUME_DIST
PERCENT_RANK
NTILE
