CREATE TABLE b (
    b INT NOT NULL,
    CONSTRAINT c_a FOREIGN KEY (b) REFERENCES a(b) ON DELETE RESTRICT ON UPDATE RESTRICT
)
