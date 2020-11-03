SELECT view_name,count(*) cnt
            FROM view_columns WHERE view_name like '%name%'
            GROUP BY view_name
         
select * from tables WHERE table_name LIKE upper('%name%' ) LIMIT 10

select * from public.tables  
