CREATE SEQUENCE foo;

CREATE SEQUENCE foo AS integer;

CREATE SEQUENCE foo INCREMENT BY 3;

CREATE SEQUENCE foo MINVALUE 5 NO MAXVALUE;

CREATE SEQUENCE foo NO MINVALUE MAXVALUE 12;

CREATE SEQUENCE foo INCREMENT 5 START WITH 8 CACHE 4;

CREATE SEQUENCE foo NO CYCLE;

CREATE SEQUENCE foo OWNED BY NONE;

CREATE SEQUENCE foo OWNED BY my_table.my_column;

CREATE TEMP SEQUENCE IF NOT EXISTS foo;

CREATE TEMPORARY SEQUENCE foo;

CREATE SEQUENCE derp INCREMENT BY -5 MINVALUE -50 MAXVALUE -5;;
