ALTER ROLE davide WITH PASSWORD 'hu8jmn3';
ALTER ROLE davide WITH PASSWORD NULL;
ALTER ROLE chris VALID UNTIL 'May 4 12:00:00 2015 +1';
ALTER ROLE fred VALID UNTIL 'infinity';
ALTER ROLE worker_bee SET maintenance_work_mem = '100000';
ALTER ROLE fred IN DATABASE devel SET client_min_messages TO DEFAULT;
ALTER ROLE fred IN DATABASE devel SET client_min_messages FROM CURRENT;
ALTER ROLE fred IN DATABASE devel RESET ALL;
ALTER ROLE miriam CREATEROLE CREATEDB;
ALTER USER davide WITH PASSWORD 'hu8jmn3';
ALTER USER davide WITH PASSWORD NULL;
ALTER USER chris VALID UNTIL 'May 4 12:00:00 2015 +1';
ALTER USER fred VALID UNTIL 'infinity';
ALTER USER worker_bee SET maintenance_work_mem = '100000';
ALTER USER fred IN DATABASE devel SET client_min_messages TO DEFAULT;
ALTER USER fred IN DATABASE devel SET client_min_messages FROM CURRENT;
ALTER USER fred IN DATABASE devel RESET ALL;
ALTER USER miriam CREATEROLE CREATEDB;
