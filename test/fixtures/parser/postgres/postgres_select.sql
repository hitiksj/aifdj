SELECT timestamp with time zone '2005-04-02 12:00:00-07' + interval '1 day';

SELECT DATEADD(day, -2, current_date);

SELECT timestamptz '2013-07-01 12:00:00' - timestamptz '2013-03-01 12:00:00';

SELECT 1.0::int;

SELECT ('2015-10-24 16:38:46'::timestamp AT TIME ZONE 'UTC');
