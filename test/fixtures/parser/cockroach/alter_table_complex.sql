ALTER TABLE t1
    DROP COLUMN a,
    ADD COLUMN b BOOLEAN DEFAULT FALSE,
    ADD COLUMN c TEXT,
    ADD COLUMN d JSONB,
    ALTER COLUMN e DROP NOT NULL,
    ADD CONSTRAINT c1 CHECK ((d IS NOT NULL) != (e IS NOT NULL)),
    ADD CONSTRAINT c2 CHECK (b = (e IS NOT NULL));
