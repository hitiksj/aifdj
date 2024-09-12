CREATE TABLE t1
(
  CHECK (c1 <> c2),
  c1 INT CHECK (c1 > 10),
  c2 INT CONSTRAINT c2_positive CHECK (c2 > 0),
  c3 INT CHECK (c3 < 100),
  CONSTRAINT c1_nonzero CHECK (c1 <> 0),
  CHECK (c1 > c3)
);

ALTER TABLE t1
ALTER CHECK c2_positive NOT ENFORCED;

ALTER TABLE t1
DROP CONSTRAINT c1_nonzero;
