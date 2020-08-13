--Employees

CREATE TABLE Employee (
  Id INT,
  Name VARCHAR(255),
  Salary INT,
  DepartmentId INT
);

CREATE TABLE Department (
  Id INT,
  Name VARCHAR(255)
);

INSERT INTO Employee 
  (Id, Name, Salary, DepartmentId) 
VALUES 
  (1, 'Joe', 70000, 1), 
  (2, 'Henry', 80000, 2), 
  (3, 'Sam', 60000, 2), 
  (4, 'Max', 90000, 1), 
  (5, 'Janet', 69000, 1), 
  (6, 'Randy', 85000, 1);
  
 INSERT INTO Department 
  (Id, Name) 
VALUES 
  (1, 'IT'), 
  (2, 'Sales');
 
 
 with da as (select d.name , salary, rank() over(partition by d.name order by e.salary desc) rnk
 from employee e inner join department d on e.departmentid = d.id)
 select name , salary , rnk
 from da where rnk = 1
 
 --Top 3
  with da as (select d.name , salary, rank() over(partition by d.name order by e.salary desc) rnk
 from employee e inner join department d on e.departmentid = d.id)
 select name , salary , rnk
 from da where rnk <= 3
 
--third highest salary 
 with da as (select * from employee order by salary desc limit 3)
 select name, salary from da order by salary desc limit 1
 
 
 --customer never ordered

create table customer (
id int,
Name text);

insert into customer values (1,'Joe'), (2,'Mario'), (3,'Sam') , (4,'Bob');

create table orders(id int, customerId int);

insert into orders values (1,3),(2,1);

select c.name
from  customer c left outer join orders o on c.id = o.customerId
where o.id is null

--Friends request

create schema sqlt

SET search_path to sqlt

create table friend_request(
sender_id int,
send_to_id int,
request_date date
)

insert into friend_request values(1,2,'2016-06-01');
insert into friend_request values(1,3,'2016-06-01');
insert into friend_request values(1,4,'2016-06-01');
insert into friend_request values(2,3,'2016-06-02');
insert into friend_request values(3,4,'2016-06-09');

create table request_accepted(
requester_id int,
acceepter_id int,
acceept_date date
)

insert into request_accepted values(1,2,'2016-06-03');
insert into request_accepted values(1,3,'2016-06-08');
insert into request_accepted values(2,3,'2016-06-08');
insert into request_accepted values(3,4,'2016-06-09');
insert into request_accepted values(3,4,'2016-06-10');

select *
from friend_request fr left outer join request_accepted ra on fr.send_to_id  = ra.acceepter_id 

select *
from request_accepted ra

with sent as (select count(*) sent from request_accepted),
	 accept as (select count(*) accept from request_accepted),
	 sentaccept as ( select count(* ) sentaccept from friend_request fr inner join (select distinct requester_id,acceepter_id from  request_accepted) ra on fr.send_to_id  = ra.acceepter_id and fr.sender_id = ra.requester_id )
	 select sent,accept, sentaccept, round(sentaccept/coalesce ((sent * 1.00),1) ,2) from sent , accept, sentaccept

	 

