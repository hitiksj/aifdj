ALTER VIRTUAL SCHEMA s2
    SET CONNECTION_STRING = 'jdbc:hive2://localhost:10000/default';
ALTER VIRTUAL SCHEMA s2 REFRESH;
