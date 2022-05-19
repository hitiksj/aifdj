"""A List of MySQL SQL keywords.

https://dev.mysql.com/doc/refman/8.0/en/keywords.html
"""

mysql_reserved_keywords = """ACCESSIBLE
ADD
ALL
ALTER
ANALYZE
AND
AS
ASC
ASENSITIVE
BEFORE
BETWEEN
BIGINT
BINARY
BLOB
BOTH
BY
CALL
CASCADE
CASE
CHANGE
CHAR
CHARACTER
CHECK
COLLATE
COLUMN
CONDITION
CONSTRAINT
CONTINUE
CONVERT
CREATE
CROSS
CUME_DIST
CURRENT_DATE
CURRENT_TIME
CURRENT_TIMESTAMP
CURRENT_USER
CURSOR
DATABASE
DATABASES
DAY_HOUR
DAY_MICROSECOND
DAY_MINUTE
DAY_SECOND
DEC
DECIMAL
DECLARE
DEFAULT
DELAYED
DELETE
DENSE_RANK
DESC
DESCRIBE
DETERMINISTIC
DISTINCT
DISTINCTROW
DIV
DOUBLE
DROP
DUAL
EACH
ELSE
ELSEIF
EMPTY
ENCLOSED
ESCAPED
EXCEPT
EXISTS
EXIT
EXPLAIN
FALSE
FETCH
FIRST_VALUE
FLOAT
FLOAT4
FLOAT8
FOR
FORCE
FOREIGN
FROM
FULLTEXT
GENERATED
GET
GRANT
GROUP
GROUPING
GROUPS
HAVING
HIGH_PRIORITY
HOUR_MICROSECOND
HOUR_MINUTE
HOUR_SECOND
IF
IGNORE
IN
INDEX
INFILE
INNER
INOUT
INSENSITIVE
INSERT
INT
INT1
INT2
INT3
INT4
INT8
INTEGER
INTERSECT
INTERVAL
INTO
IO_AFTER_GTIDS
IO_BEFORE_GTIDS
IS
ITERATE
JOIN
JSON_TABLE
KEY
KEYS
KILL
LAG
LAST_VALUE
LATERAL
LEAD
LEADING
LEAVE
LEFT
LIKE
LIMIT
LINEAR
LINES
LOAD
LOCALTIME
LOCALTIMESTAMP
LOCK
LONG
LONGBLOB
LONGTEXT
LOOP
LOW_PRIORITY
MASTER_BIND
MASTER_SSL_VERIFY_SERVER_CERT
MATCH
MAXVALUE
MEDIUMBLOB
MEDIUMINT
MEDIUMTEXT
MIDDLEINT
MINUTE_MICROSECOND
MINUTE_SECOND
MOD
MODIFIES
NATURAL
NOT
NO_WRITE_TO_BINLOG
NTH_VALUE
NTILE
NULL
NUMERIC
OF
ON
OPTIMIZE
OPTIMIZER_COSTS
OPTION
OPTIONALLY
OR
ORDER
OUT
OUTER
OUTFILE
OVER
PARTITION
PERCENT_RANK
PRECISION
PRIMARY
PROCEDURE
PURGE
RANGE
RANK
READ
READS
READ_WRITE
REAL
RECURSIVE
REFERENCES
REGEXP
RELEASE
RENAME
REPEAT
REPLACE
REQUIRE
RESIGNAL
RESTRICT
RETURN
REVOKE
RIGHT
RLIKE
ROW_NUMBER
SCHEMA
SCHEMAS
SECOND_MICROSECOND
SELECT
SENSITIVE
SEPARATOR
SET
SHOW
SIGNAL
SMALLINT
SPATIAL
SPECIFIC
SQL
SQLEXCEPTION
SQLSTATE
SQLWARNING
SQL_BIG_RESULT
SQL_CALC_FOUND_ROWS
SQL_SMALL_RESULT
SSL
STARTING
STORED
STRAIGHT_JOIN
SYSTEM
TABLE
TERMINATED
THEN
TINYBLOB
TINYINT
TINYTEXT
TO
TRAILING
TRIGGER
TRUE
UNDO
UNION
UNIQUE
UNLOCK
UNSIGNED
UPDATE
USAGE
USE
USING
UTC_DATE
UTC_TIME
UTC_TIMESTAMP
VALUES
VARBINARY
VARCHAR
VARCHARACTER
VARYING
VIRTUAL
WHEN
WHERE
WHILE
WINDOW
WITH
WRITE
XOR
YEAR_MONTH
ZEROFILL
"""

mysql_unreserved_keywords = """ACCOUNT
ACTION
ACTIVE
ADMIN
AFTER
AGAINST
AGGREGATE
ALGORITHM
ALWAYS
ANALYSE
ANY
ARRAY
ASCII
AT
ATTRIBUTE
AUTHENTICATION
AUTOEXTEND_SIZE
AUTO_INCREMENT
AVG
AVG_ROW_LENGTH
BACKUP
BEGIN
BINLOG
BIT
BLOCK
BOOL
BOOLEAN
BTREE
BUCKETS
BYTE
CACHE
CASCADED
CATALOG_NAME
CHAIN
CHALLENGE_RESPONSE
CHANGED
CHANNEL
CHARSET
CHECKSUM
CIPHER
CLASS_ORIGIN
CLIENT
CLONE
CLOSE
COALESCE
CODE
COLLATION
COLUMNS
COLUMN_FORMAT
COLUMN_NAME
COMMENT
COMMIT
COMMITTED
COMPACT
COMPLETION
COMPONENT
COMPRESSED
COMPRESSION
CONCURRENT
CONNECTION
CONSISTENT
CONSTRAINT_CATALOG
CONSTRAINT_NAME
CONSTRAINT_SCHEMA
CONTAINS
CONTEXT
CPU
CUBE
CUME_DIST
CURRENT
CURSOR_NAME
DATA
DATAFILE
DATE
DATETIME
DAY
DEALLOCATE
DEFAULT_AUTH
DEFINER
DEFINITION
DELAY_KEY_WRITE
DENSE_RANK
DESCRIPTION
DES_KEY_FILE
DIAGNOSTICS
DIRECTORY
DISABLE
DISCARD
DISK
DO
DUMPFILE
DUPLICATE
DYNAMIC
EMPTY
ENABLE
ENCRYPTION
END
ENDS
ENFORCED
ENGINE
ENGINES
ENGINE_ATTRIBUTE
ENUM
ERROR
ERRORS
ESCAPE
EVENT
EVENTS
EVERY
EXCHANGE
EXCLUDE
EXECUTE
EXPANSION
EXPIRE
EXPORT
EXTENDED
EXTENT_SIZE
FACTOR
FAILED_LOGIN_ATTEMPTS
FAST
FAULTS
FIELDS
FILE
FILE_BLOCK_SIZE
FILTER
FINISH
FIRST
FIRST_VALUE
FIXED
FLUSH
FOLLOWING
FOLLOWS
FORMAT
FOUND
FULL
FUNCTION
GENERAL
GEOMCOLLECTION
GEOMETRY
GEOMETRYCOLLECTION
GET_FORMAT
GET_MASTER_PUBLIC_KEY
GET_SOURCE_PUBLIC_KEY
GLOBAL
GRANTS
GROUPING
GROUPS
GROUP_REPLICATION
GTID_ONLY
HANDLER
HASH
HELP
HISTOGRAM
HISTORY
HOST
HOSTS
HOUR
IDENTIFIED
IGNORE_SERVER_IDS
IMPORT
INACTIVE
INDEXES
INITIAL
INITIAL_SIZE
INITIATE
INSERT_METHOD
INSTALL
INSTANCE
INTERSECT
INVISIBLE
INVOKER
IO
IO_THREAD
IPC
ISOLATION
ISSUER
JSON
JSON_TABLE
JSON_VALUE
KEYRING
KEY_BLOCK_SIZE
LAG
LANGUAGE
LAST
LAST_VALUE
LATERAL
LEAD
LEAVES
LESS
LEVEL
LINESTRING
LIST
LOCAL
LOCKED
LOCKS
LOGFILE
LOGS
MASTER
MASTER_AUTO_POSITION
MASTER_COMPRESSION_ALGORITHMS
MASTER_CONNECT_RETRY
MASTER_DELAY
MASTER_HEARTBEAT_PERIOD
MASTER_HOST
MASTER_LOG_FILE
MASTER_LOG_POS
MASTER_PASSWORD
MASTER_PORT
MASTER_PUBLIC_KEY_PATH
MASTER_RETRY_COUNT
MASTER_SERVER_ID
MASTER_SSL
MASTER_SSL_CA
MASTER_SSL_CAPATH
MASTER_SSL_CERT
MASTER_SSL_CIPHER
MASTER_SSL_CRL
MASTER_SSL_CRLPATH
MASTER_SSL_KEY
MASTER_TLS_CIPHERSUITES
MASTER_TLS_VERSION
MASTER_USER
MASTER_ZSTD_COMPRESSION_LEVEL
MAX_CONNECTIONS_PER_HOUR
MAX_QUERIES_PER_HOUR
MAX_ROWS
MAX_SIZE
MAX_UPDATES_PER_HOUR
MAX_USER_CONNECTIONS
MEDIUM
MEMBER
MEMORY
MERGE
MESSAGE_TEXT
MICROSECOND
MIGRATE
MINUTE
MIN_ROWS
MODE
MODIFY
MONTH
MULTILINESTRING
MULTIPOINT
MULTIPOLYGON
MUTEX
MYSQL_ERRNO
NAME
NAMES
NATIONAL
NCHAR
NDB
NDBCLUSTER
NESTED
NETWORK_NAMESPACE
NEVER
NEW
NEXT
NO
NODEGROUP
NONE
NOWAIT
NO_WAIT
NTH_VALUE
NTILE
NULLS
NUMBER
NVARCHAR
OF
OFF
OFFSET
OJ
OLD
ONE
ONLY
OPEN
OPTIONAL
OPTIONS
ORDINALITY
ORGANIZATION
OTHERS
OVER
OWNER
PACK_KEYS
PAGE
PARSER
PARSE_GCOL_EXPR
PARTIAL
PARTITIONING
PARTITIONS
PASSWORD
PASSWORD_LOCK_TIME
PATH
PERCENT_RANK
PERSIST
PERSIST_ONLY
PHASE
PLUGIN
PLUGINS
PLUGIN_DIR
POINT
POLYGON
PORT
PRECEDES
PRECEDING
PREPARE
PRESERVE
PREV
PRIVILEGES
PRIVILEGE_CHECKS_USER
PROCESS
PROCESSLIST
PROFILE
PROFILES
PROXY
QUARTER
QUERY
QUICK
RANDOM
RANK
READ_ONLY
REBUILD
RECOVER
RECURSIVE
REDOFILE
REDO_BUFFER_SIZE
REDUNDANT
REFERENCE
REGISTRATION
RELAY
RELAYLOG
RELAY_LOG_FILE
RELAY_LOG_POS
RELAY_THREAD
RELOAD
REMOTE
REMOVE
REORGANIZE
REPAIR
REPEATABLE
REPLICA
REPLICAS
REPLICATE_DO_DB
REPLICATE_DO_TABLE
REPLICATE_IGNORE_DB
REPLICATE_IGNORE_TABLE
REPLICATE_REWRITE_DB
REPLICATE_WILD_DO_TABLE
REPLICATE_WILD_IGNORE_TABLE
REPLICATION
REQUIRE_ROW_FORMAT
RESET
RESOURCE
RESPECT
RESTART
RESTORE
RESUME
RETAIN
RETURNED_SQLSTATE
RETURNING
RETURNS
REUSE
REVERSE
ROLE
ROLLBACK
ROLLUP
ROTATE
ROUTINE
ROW
ROWS
ROW_COUNT
ROW_FORMAT
ROW_NUMBER
RTREE
SAVEPOINT
SCHEDULE
SCHEMA_NAME
SECOND
SECONDARY
SECONDARY_ENGINE
SECONDARY_ENGINE_ATTRIBUTE
SECONDARY_LOAD
SECONDARY_UNLOAD
SECURITY
SERIAL
SERIALIZABLE
SERVER
SESSION
SHARE
SHUTDOWN
SIGNED
SIMPLE
SKIP
SLAVE
SLOW
SNAPSHOT
SOCKET
SOME
SONAME
SOUNDS
SOURCE
SOURCE_AUTO_POSITION
SOURCE_BIND
SOURCE_COMPRESSION_ALGORITHMS
SOURCE_CONNECT_RETRY
SOURCE_DELAY
SOURCE_HEARTBEAT_PERIOD
SOURCE_HOST
SOURCE_LOG_FILE
SOURCE_LOG_POS
SOURCE_PASSWORD
SOURCE_PORT
SOURCE_PUBLIC_KEY_PATH
SOURCE_RETRY_COUNT
SOURCE_SSL
SOURCE_SSL_CA
SOURCE_SSL_CAPATH
SOURCE_SSL_CERT
SOURCE_SSL_CIPHER
SOURCE_SSL_CRL
SOURCE_SSL_CRLPATH
SOURCE_SSL_KEY
SOURCE_SSL_VERIFY_SERVER_CERT
SOURCE_TLS_CIPHERSUITES
SOURCE_TLS_VERSION
SOURCE_USER
SOURCE_ZSTD_COMPRESSION_LEVEL
SQL_AFTER_GTIDS
SQL_AFTER_MTS_GAPS
SQL_BEFORE_GTIDS
SQL_BUFFER_RESULT
SQL_CACHE
SQL_NO_CACHE
SQL_THREAD
SQL_TSI_DAY
SQL_TSI_HOUR
SQL_TSI_MINUTE
SQL_TSI_MONTH
SQL_TSI_QUARTER
SQL_TSI_SECOND
SQL_TSI_WEEK
SQL_TSI_YEAR
SRID
STACKED
START
STARTS
STATS_AUTO_RECALC
STATS_PERSISTENT
STATS_SAMPLE_PAGES
STATUS
STOP
STORAGE
STREAM
STRING
SUBCLASS_ORIGIN
SUBJECT
SUBPARTITION
SUBPARTITIONS
SUPER
SUSPEND
SWAPS
SWITCHES
SYSTEM
TABLES
TABLESPACE
TABLE_CHECKSUM
TABLE_NAME
TEMPORARY
TEMPTABLE
TEXT
THAN
THREAD_PRIORITY
TIES
TIME
TIMESTAMP
TIMESTAMPADD
TIMESTAMPDIFF
TLS
TRANSACTION
TRIGGERS
TRUNCATE
TYPE
TYPES
UNBOUNDED
UNCOMMITTED
UNDEFINED
UNDOFILE
UNDO_BUFFER_SIZE
UNICODE
UNINSTALL
UNKNOWN
UNREGISTER
UNTIL
UPGRADE
USER
USER_RESOURCES
USE_FRM
VALIDATION
VALUE
VARIABLES
VCPU
VIEW
VISIBLE
WAIT
WARNINGS
WEEK
WEIGHT_STRING
WINDOW
WITHOUT
WORK
WRAPPER
X509
XA
XID
XML
YEAR
ZONE
"""
