--date  functions
https://prestodb.io/docs/current/functions/datetime.html

SELECT  (cast(current_date - interval '3' year as date))

select cast(date_parse('18-FEB-2021','%d-%b-%Y') as date)

select from_iso8601_timestamp('2021-03-12T16:07:22Z')
