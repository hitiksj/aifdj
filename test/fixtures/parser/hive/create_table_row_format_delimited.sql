
CREATE TABLE foo(
    col1 INT PRIMARY KEY,
    col2 BIGINT NOT NULL,
    col3 STRING,
    col4 STRING COMMENT 'Column 4')
 COMMENT 'This is a test table'
 ROW FORMAT DELIMITED
   FIELDS TERMINATED BY '\001'
   COLLECTION ITEMS TERMINATED BY '\002'
   MAP KEYS TERMINATED BY '\003'
   LINES TERMINATED BY '\004'
   NULL DEFINED AS '\005'
STORED AS SEQUENCEFILE;