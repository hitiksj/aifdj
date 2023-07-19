"""A list of all SQL key words.

https://docs.microsoft.com/en-us/sql/t-sql/language-elements/reserved-keywords-transact-sql?view=sql-server-ver15
"""

RESERVED_KEYWORDS = [
    "ADD",
    "ALL",
    "ALTER",
    "AND",
    "ANY",
    "APPEND",
    "AS",
    "ASC",
    "AUTHORIZATION",
    "BACKUP",
    "BATCHSIZE",
    "BEGIN",
    "BETWEEN",
    "BREAK",
    "BROWSE",
    "BULK",
    "BY",
    "CASCADE",
    "CASE",
    "CHECK",
    "CHECKPOINT",
    "CHECK_CONSTRAINTS",
    "CLOSE",
    "CLUSTERED",
    "COALESCE",
    "COLLATE",
    "COLUMN",
    "COMMIT",
    "COMPUTE",
    "CONSTRAINT",
    "CONTAINS",
    "CONTAINSTABLE",
    "CONTINUE",
    "CONVERT",
    "CREATE",
    "CROSS",
    "CURRENT",
    "CURRENT_DATE",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "CURRENT_USER",
    "CURSOR",
    "DATABASE",
    "DAY",
    "DBCC",
    "DEALLOCATE",
    "DECLARE",
    "DEFAULT",
    "DELETE",
    "DENY",
    "DESC",
    "DISTINCT",
    "DISTRIBUTED",
    "DOUBLE",
    "DROP",
    "DYNAMIC",
    "ELSE",
    "END",
    "ERRLVL",
    "ESCAPE",
    "EXCEPT",
    "EXEC",
    "EXECUTE",
    "EXISTS",
    "EXIT",
    "EXTERNAL",
    "FAST_FORWARD",
    "FETCH",
    "FILE",
    "FILLFACTOR",
    "FOR",
    "FORWARD_ONLY",
    "FOREIGN",
    "FREETEXT",
    "FREETEXTTABLE",
    "FROM",
    "FULL",
    "FULLSCAN",
    "FUNCTION",
    "GLOBAL",
    "GO",
    "GOTO",
    "GRANT",
    "GROUP",
    "HAVING",
    "HOLDLOCK",
    "IDENTITY_INSERT",
    "IDENTITY",
    "IDENTITYCOL",
    "IF",
    "IN",
    "INDEX",
    "INNER",
    "INSERT",
    "INTERSECT",
    "INTO",
    "IS",
    "JOIN",
    "KEY",
    "KEYSET",
    "KILL",
    "LEFT",
    "LIKE",
    "LINENO",
    "LOCAL",
    "MERGE",
    "NATIONAL",
    "NATIVE_COMPILATION",
    "NOCHECK",
    "NONCLUSTERED",
    "NOT",
    "NULL",
    "NULLIF",
    "OF",
    "OFF",
    "OFFSETS",
    "ON",
    "OPEN",
    "OPENDATASOURCE",
    "OPENQUERY",
    "OPENROWSET",
    "OPENXML",
    "OPTIMISTIC",
    "OPTION",
    "OR",
    "ORDER",
    "OUTER",
    "OVER",
    "PERCENT",
    "PIVOT",
    "PLAN",
    "PRIMARY",
    "PRINT",
    "PROC",
    "PROCEDURE",
    "PUBLIC",
    "RAISERROR",
    "READ",
    "READ_ONLY",
    "READTEXT",
    "RECONFIGURE",
    "REFERENCES",
    "REPLICATION",
    "RESAMPLE",
    "RESTORE",
    "RESTRICT",
    "RETURN",
    "REVERT",
    "REVOKE",
    "RIGHT",
    "ROLLBACK",
    "ROWCOUNT",
    "ROWGUIDCOL",
    "RULE",
    "SAVE",
    "SCHEMA",
    "SCROLL",
    "SCROLL_LOCKS",
    "SELECT",
    "SEMANTICKEYPHRASETABLE",
    "SEMANTICSIMILARITYDETAILSTABLE",
    "SEMANTICSIMILARITYTABLE",
    "SESSION_USER",
    "SET",
    "SETUSER",
    "SHUTDOWN",
    "SOME",
    "STATIC",
    "STATISTICS",
    "SYSTEM_USER",
    "TABLE",
    "TABLESAMPLE",
    "TEXTSIZE",
    "THEN",
    "TO",
    "TOP",
    "TRAN",
    "TRANSACTION",
    "TRAN",
    "TRIGGER",
    "TRUNCATE",
    "TRY_CONVERT",
    "TSEQUAL",
    "TYPE_WARNING",
    "UNION",
    "UNIQUE",
    "UNPIVOT",
    "UPDATE",
    "UPDATETEXT",
    "USE",
    "USER",
    "VALUES",
    "VARYING",
    "VIEW",
    "WAITFOR",
    "WHEN",
    "WHERE",
    "WHILE",
    "WITH",
    "WRITETEXT",
]


UNRESERVED_KEYWORDS = [
    "ABORT_AFTER_WAIT",
    "ABORT",
    "ABSENT",
    "AFTER",
    "ALGORITHM",
    "ALLOW_PAGE_LOCKS",
    "ALLOW_ROW_LOCKS",
    "ALWAYS",
    "ANSI_DEFAULTS",
    "ANSI_NULL_DFLT_OFF",
    "ANSI_NULL_DFLT_ON",
    "ANSI_NULLS",
    "ANSI_PADDING",
    "ANSI_WARNINGS",
    "APPEND_ONLY",
    "APPLY",
    "ARITHABORT",
    "ARITHIGNORE",
    "AT",
    "AUTO_CREATE_TABLE",
    "AUTO",
    "BERNOULLI",
    "BINARY",
    "BLOCKERS",
    "BREAK",
    "CACHE",
    "CALLED",
    "CALLER",
    "CAST",
    "CATCH",
    "CODEPAGE",
    "COLUMN_ENCRYPTION_KEY",
    "COLUMNSTORE_ARCHIVE",
    "COLUMNSTORE",
    "COMMITTED",
    "COMPRESS_ALL_ROW_GROUPS",
    "COMPRESSION_DELAY",
    "COMPRESSION",
    "CONCAT_NULL_YIELDS_NULL",
    "CONCAT",
    "CONNECTION_OPTIONS",
    "CONTAINED",
    "CONTINUE",
    "CONTROL",
    "CREDENTIAL",
    "COPY",
    "CURSOR_CLOSE_ON_COMMIT",
    "CYCLE",
    "DATA_COMPRESSION",
    "DATA_CONSISTENCY_CHECK",
    "DATA_DELETION",
    "DATA_SOURCE",
    "DATA",
    "DATAFILETYPE",
    "DATASOURCE",
    "DATE_FORMAT",
    "DATE",
    "DATEFIRST",
    "DATEFORMAT",
    "DEADLOCK_PRIORITY",
    "DELAY",
    "DELIMITEDTEXT",
    "DELTA",
    "DENSE_RANK",
    "DETERMINISTIC",
    "DISABLE",
    "DISK",  # listed as reserved but functionally unreserved
    "DISTRIBUTION",  # Azure Synapse Analytics specific
    "DROP_EXISTING",
    "DUMP",  # listed as reserved but functionally unreserved
    "DURABILITY",
    "ELEMENTS",
    "ENCODING",
    "ENCRYPTED",
    "ENCRYPTION_TYPE",
    "ENCRYPTION",
    "ERRORFILE_CREDENTIAL",
    "ERRORFILE_DATA_SOURCE",
    "ERRORFILE",
    "EXPAND",
    "EXPLAIN",  # Azure Synapse Analytics specific
    "EXPLICIT",
    "EXTERNALPUSHDOWN",
    "FAST",
    "FIELD_TERMINATOR",
    "FIELDQUOTE",
    "FIELDTERMINATOR",
    "FILE_FORMAT",
    "FILESTREAM",
    "FILESTREAM_ON",
    "FILESTREAM",
    "FILE_TYPE",
    "FILETABLE_COLLATE_FILENAME",
    "FILETABLE_DIRECTORY",
    "FILETABLE_FULLPATH_UNIQUE_CONSTRAINT_NAME",
    "FILETABLE_PRIMARY_KEY_CONSTRAINT_NAME",
    "FILETABLE_STREAMID_UNIQUE_CONSTRAINT_NAME",
    "FILTER_COLUMN",
    "FILTER_PREDICATE",
    "FILTER",
    "FIPS_FLAGGER",
    "FIRE_TRIGGERS",
    "FIRST_ROW",
    "FIRST",
    "FIRSTROW",
    "FMTONLY",
    "FOLLOWING",
    "FOR",
    "FORCE",
    "FORCEPLAN",
    "FORCESCAN",
    "FORCESEEK",
    "FORMAT_OPTIONS",
    "FORMAT_TYPE",
    "FORMAT",
    "FORMATFILE_DATA_SOURCE",
    "FORMATFILE",
    "GENERATED",
    "HASH",
    "HEAP",  # Azure Synapse Analytics specific
    "HIDDEN",
    "HIGH",
    "HINT",
    "HISTORY_RETENTION_PERIOD",
    "HISTORY_TABLE",
    "IGNORE_CONSTRAINTS",
    "IGNORE_DUP_KEY",
    "IGNORE_NONCLUSTERED_COLUMNSTORE_INDEX",
    "IGNORE_TRIGGERS",
    "IGNORE",
    "IMPLICIT_TRANSACTIONS",
    "INBOUND",
    "INCLUDE_NULL_VALUES",
    "INCLUDE",
    "INCREMENT",
    "INLINE",
    "INSTEAD",
    "INTERVAL",
    "IO",
    "ISOLATION",
    "JSON",
    "KEEP",
    "KEEPDEFAULTS",
    "KEEPFIXED",
    "KEEPIDENTITY",
    "KEEPNULLS",
    "KILOBYTES_PER_BATCH",
    "LABEL",  # *reserved* keyword in Azure Synapse; but would break TSQL parsing
    "LANGUAGE",
    "LAST",
    "LASTROW",
    "LEDGER_VIEW",
    "LEDGER",
    "LEVEL",
    "LOAD",  # listed as reserved but functionally unreserved
    "LOB_COMPACTION",
    "LOCATION",
    "LOCK_TIMEOUT",
    "LOG",
    "LOGIN",
    "LOOP",
    "LOW",
    "MASKED",
    "MATCHED",
    "MAX_DURATION",
    "MAX_GRANT_PERCENT",
    "MAX",
    "MAXDOP",
    "MAXERRORS",
    "MAXRECURSION",
    "MAXVALUE",
    "MEMORY_OPTIMIZED",
    "MIGRATION_STATE",
    "MIN_GRANT_PERCENT",
    "MINUTES",
    "MINVALUE",
    "NEXT",
    "NO_PERFORMANCE_SPOOL",
    "NO",
    "NOCOUNT",
    "NOEXEC",
    "NOEXPAND",
    "NOLOCK",
    "NONE",
    "NORMAL",
    "NOWAIT",
    "NTILE",
    "NUMERIC_ROUNDABORT",
    "OBJECT",
    "OFFSET",
    "ONLINE",
    "OPENJSON",
    "OPERATION_TYPE_COLUMN_NAME",
    "OPERATION_TYPE_DESC_COLUMN_NAME",
    "OPTIMIZE_FOR_SEQUENTIAL_KEY",
    "OPTIMIZE",
    "ORC",
    "OUT",
    "OUTBOUND",
    "OUTPUT",
    "OWNER",
    "PAD_INDEX",
    "PAGE",
    "PAGLOCK",
    "PARAMETER",
    "PARAMETERIZATION",
    "PARQUET",
    "PARSEONLY",
    "PARSER_VERSION",
    "PARTITION",
    "PARTITIONS",
    "PATH",
    "PAUSE",
    "PAUSED",
    "PERCENTAGE",
    "PERCENTILE_CONT",
    "PERCENTILE_DISC",
    "PERIOD",
    "PERSISTED",
    "PRECEDING",
    "PRECISION",  # listed as reserved but functionally unreserved
    "PRIOR",
    "PROFILE",
    "PUSHDOWN",
    "QUERY_GOVERNOR_COST_LIMIT",
    "QUERYTRACEON",
    "QUOTED_IDENTIFIER",
    "R",  # sqlcmd command
    "RANDOMIZED",
    "RANGE",
    "RANK",
    "RAW",
    "RCFILE",
    "READCOMMITTED",
    "READCOMMITTEDLOCK",
    "READONLY",
    "READPAST",
    "READUNCOMMITTED",
    "REBUILD",
    "RECEIVE",
    "RECOMPILE",
    "RECURSIVE",
    "REJECT_SAMPLE_VALUE",
    "REJECT_TYPE",
    "REJECT_VALUE",
    "REJECTED_ROW_LOCATION",
    "REMOTE_DATA_ARCHIVE",
    "REMOTE_PROC_TRANSACTIONS",
    "RENAME",  # Azure Synapse Analytics specific
    "REORGANIZE",
    "REPEATABLE",
    "REPEATABLEREAD",
    "REPLACE",
    "REPLICATE",  # Azure Synapse Analytics
    "RESPECT",
    "RESULT_SET_CACHING",  # Azure Synapse Analytics specific
    "RESUMABLE",
    "RESUME",
    "RETENTION_PERIOD",
    "RETURNS",
    "ROBUST",
    "ROLE",
    "ROOT",
    "ROUND_ROBIN",  # Azure Synapse Analytics specific
    "ROW_NUMBER",
    "ROW",
    "ROWGUIDCOL",
    "ROWLOCK",
    "ROWS_PER_BATCH",
    "ROWS",
    "ROWTERMINATOR",
    "S",
    "SCALEOUTEXECUTION",
    "SCHEMA_AND_DATA",
    "SCHEMA_ONLY",
    "SCHEMABINDING",
    "SCOPED",
    "SECRET",
    "SECURITYAUDIT",  # listed as reserved but functionally unreserved
    "SELF",
    "SEQUENCE_NUMBER_COLUMN_NAME",
    "SEQUENCE_NUMBER",
    "SEQUENCE",
    "SERDE_METHOD",
    "SERIALIZABLE",
    "SERVER",
    "SETERROR",
    "SETVAR",  # sqlcmd command
    "SHOWPLAN_ALL",
    "SHOWPLAN_TEXT",
    "SHOWPLAN_XML",
    "SINGLE_BLOB",
    "SINGLE_CLOB",
    "SINGLE_NCLOB",
    "SNAPSHOT",
    "SORT_IN_TEMPDB",
    "SOURCE",
    "SPARSE",
    "SPATIAL_WINDOW_MAX_CELLS",
    "START",
    "STATISTICS_INCREMENTAL",
    "STATISTICS_NORECOMPUTE",
    "STRING_AGG",
    "STRING_DELIMITER",
    "SWITCH",
    "SYNONYM",
    "SYSTEM_TIME",
    "SYSTEM_VERSIONING",
    "SYSTEM",
    "TABLOCK",
    "TABLOCKX",
    "TAKE",
    "TARGET",
    "TEXTIMAGE_ON",
    "THROW",
    "TIES",
    "TIME",
    "TIMEOUT",
    "TIMESTAMP",
    "TRANSACTION_ID_COLUMN_NAME",
    "TRANSACTION_ID",
    "TRUNCATE_TARGET",  # Azure Synapse Analytics specific
    "TRY",
    "TYPE",
    "UNBOUNDED",
    "UNCOMMITTED",
    "UNKNOWN",
    "UPDLOCK",
    "USE_TYPE_DEFAULT",
    "USER_DB",  # Azure Synapse Analytics specific, deprecated
    "USING",
    "VALUE",
    "VIEW_METADATA",
    "WAIT_AT_LOW_PRIORITY",
    "WAITFOR",
    "WHILE",
    "WITHIN",
    "WITHOUT_ARRAY_WRAPPER",
    "WORK",
    "XACT_ABORT",
    "XLOCK",
    "XML_COMPRESSION",
    "XML",
    "XMLDATA",
    "XMLSCHEMA",
    "XSINIL",
    "ZONE",
]
