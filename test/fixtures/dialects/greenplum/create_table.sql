CREATE TABLE measurement (
city_id int NOT NULL,
logdate date NOT NULL,
peaktemp int,
unitsales int
) WITH (appendoptimized=true, compresslevel=5)
DISTRIBUTED BY (txn_id, other_field);


CREATE TABLE measurement (
city_id int NOT NULL,
logdate date NOT NULL,
peaktemp int,
unitsales int
) WITH (appendoptimized=true, orientation="column")
DISTRIBUTED BY (txn_id);


CREATE TEMP TABLE test (
test_id int NOT NULL,
logdate date NOT NULL,
test_text int
)
DISTRIBUTED BY (txn_id);


CREATE TABLE test_randomly (
test_id int NOT NULL,
logdate date NOT NULL,
test_text int
)
DISTRIBUTED RANDOMLY;

CREATE TABLE test_replicated (
test_id int NOT NULL,
logdate date NOT NULL,
test_text int
)
DISTRIBUTED REPLICATED;

create table table1 (
    column1 int
    , column2 varchar
    , column3 boolean
)
with (appendoptimized = true, compresstype = zstd)
distributed by (column1, column2);
