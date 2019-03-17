--generate_series
CREATE TABLE schema1.genseries
(
  s1 bigint,
  e1 bigint,
  da text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE schema1.genseries
  OWNER TO postgres;

INSERT INTO schema1.genseries(
            s1, e1, da)
    VALUES (1, 2, 'a'),(3, 6, 'b');

Select generate_series(s1,e1),* from schema1.genseries
