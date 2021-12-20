SELECT current_date + INTERVAL '2' DAY;

SELECT current_date - INTERVAL '1' DAY AS yesterday;

SELECT current_date + INTERVAL '12' HOUR;

-- These examples are from:
-- https://cwiki.apache.org/confluence/display/hive/languagemanual+types#LanguageManualTypes-Intervals
SELECT INTERVAL '1' DAY;

SELECT INTERVAL '1-2' YEAR TO MONTH;

SELECT INTERVAL '1' YEAR + INTERVAL '2' MONTH;

SELECT INTERVAL '1 2:3:4.000005' DAY;

SELECT INTERVAL '1' DAY+
       INTERVAL '2' HOUR +
       INTERVAL '3' MINUTE +
       INTERVAL '4' SECOND +
       INTERVAL '5' NANO;

SELECT INTERVAL 1 DAY;

-- This interpretation may be too simplistic
-- Original example was: INTERVAL (1+dt) DAY
SELECT INTERVAL (1+2) DAY;

SELECT 1 DAY;

SELECT INTERVAL 1 DAY;

SELECT '1-2' YEAR TO MONTH;

SELECT INTERVAL '1-2' YEARS TO MONTH;

SELECT 2 SECONDS;

SELECT 2 SECOND;
