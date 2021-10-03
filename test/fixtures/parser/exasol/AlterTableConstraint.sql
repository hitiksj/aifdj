ALTER TABLE t1 ADD CONSTRAINT my_primary_key PRIMARY KEY (a);
ALTER TABLE t2 ADD CONSTRAINT my_foreign_key FOREIGN KEY (x) REFERENCES t1;
ALTER TABLE t2 MODIFY CONSTRAINT my_foreign_key DISABLE;
ALTER TABLE t2 RENAME CONSTRAINT my_foreign_key TO my_fk;
ALTER TABLE t2 DROP CONSTRAINT my_fk;
ALTER TABLE t1 DROP CONSTRAINT IF EXISTS PK_X;
