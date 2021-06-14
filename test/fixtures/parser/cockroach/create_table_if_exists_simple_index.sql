CREATE TABLE IF NOT EXISTS t1 (
    a UUID PRIMARY KEY,
    b VARCHAR NOT NULL,
    c TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    d TIMESTAMP NOT NULL,
    e JSONB,

    INDEX i1(d)
);
