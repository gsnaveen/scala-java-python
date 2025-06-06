./duckdb ./mydatabase.db


CREATE TABLE mytable AS
    SELECT * FROM read_csv('mydata.csv', ignore_errors = true);


CREATE TABLE mytable_summary AS SELECT * FROM (SUMMARIZE mytable);

COPY (SELECT * FROM mytable_summary) TO 'mytable_summary.csv' (HEADER, DELIMITER ',');

CREATE TABLE mytable_varchar_len as
Select MAX(LEN("Attribute Name"))
from mytable


