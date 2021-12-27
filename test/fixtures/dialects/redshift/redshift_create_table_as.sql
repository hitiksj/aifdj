CREATE TEMP TABLE t1 AS (
    SELECT something
    FROM t2
);

CREATE TEMP TABLE t1 AS
    SELECT something
    FROM t2
;

CREATE TEMPORARY TABLE t1 AS
    SELECT something
    FROM t2
;

CREATE TABLE t1 AS (
    SELECT something
    FROM t2
);

CREATE TABLE t1 AS
    SELECT something
    FROM t2
;

CREATE LOCAL TEMP TABLE t1 AS
    SELECT something
    FROM t2
;

CREATE TEMP TABLE t1
SORTKEY(col1) AS
SELECT
    col1
FROM t2
;

CREATE TABLE t1
SORTKEY(col1) AS
SELECT
    col1
FROM t2
;

CREATE TABLE t1
DISTKEY(col1) AS
SELECT
    col1
FROM t2
;

CREATE TABLE t1
DISTKEY(col1)
SORTKEY(col1) AS
SELECT
    col1
FROM t2
;

CREATE TABLE t1
DISTSTYLE EVEN AS
SELECT
    col1
FROM t2
;

CREATE TABLE t1
DISTSTYLE ALL
DISTKEY(col1)
SORTKEY(col1) AS
SELECT
    col1
FROM t2
;

CREATE TABLE t1 (col1 NUMERIC, col2 VARCHAR(10))
BACKUP YES AS
SELECT
    col1
    , col2
FROM t2
;
