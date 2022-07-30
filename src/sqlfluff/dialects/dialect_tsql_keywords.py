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
    "DBCC",
    "DEALLOCATE",
    "DECLARE",
    "DEFAULT",
    "DELETE",
    "DENY",
    "DESC",
    "DISK",
    "DISTINCT",
    "DISTRIBUTED",
    "DOUBLE",
    "DROP",
    "DUMP",
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
    "FOREIGN",
    "FORWARD_ONLY",
    "FREETEXT",
    "FREETEXTTABLE",
    "FROM",
    "FULL",
    "FUNCTION",
    "GLOBAL",
    "GO",
    "GOTO",
    "GRANT",
    "GROUP",
    "HAVING",
    "HOLDLOCK",
    "IDENTITY",
    "IDENTITYCOL",
    "IDENTITY_INSERT",
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
    "LOAD",
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
    "PRECISION",
    "PRIMARY",
    "PRINT",
    "PROC",
    "PROCEDURE",
    "PUBLIC",
    "RAISERROR",
    "READ",
    "READTEXT",
    "READ_ONLY",
    "RECONFIGURE",
    "REFERENCES",
    "REPLICATION",
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
    "SECURITYAUDIT",
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
    "TRAN",
    "TRANSACTION",
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
    "WITHINGROUP",
    "WRITETEXT",
]


UNRESERVED_KEYWORDS = [
    "ABORT_AFTER_WAIT",
    "AFTER",
    "ALGORITHM",
    "ALLOW_PAGE_LOCKS",
    "ALLOW_ROW_LOCKS",
    "ALWAYS",
    "ANSI_DEFAULTS",
    "ANSI_NULLS",
    "ANSI_NULL_DFLT_OFF",
    "ANSI_NULL_DFLT_ON",
    "ANSI_PADDING",
    "ANSI_WARNINGS",
    "APPLY",
    "ARITHABORT",
    "ARITHIGNORE",
    "AT",
    "AUTO",
    "BERNOULLI",
    "BLOCKERS",
    "CACHE",
    "CALLED",
    "CALLER",
    "CATCH",
    "CODEPAGE",
    "COLUMNSTORE",
    "COLUMNSTORE_ARCHIVE",
    "COLUMN_ENCRYPTION_KEY",
    "COMMITTED",
    "COMPRESSION_DELAY",
    "CONCAT_NULL_YIELDS_NULL",
    "CONTROL",
    "CURSOR_CLOSE_ON_COMMIT",
    "CYCLE",
    "DATASOURCE",
    "DATA_COMPRESSION",
    "DATE",
    "DATEFIRST",
    "DATEFORMAT",
    "DEADLOCK_PRIORITY",
    "DELAY",
    "DETERMINISTIC",
    "DISABLE",
    "DISTRIBUTION",  # Azure Synapse Analytics specific
    "DROP_EXISTING",
    "ENCRYPTED",
    "ENCRYPTION",
    "ENCRYPTION_TYPE",
    "ERRORFILE",
    "ERRORFILE_DATA_SOURCE",
    "EXPAND",
    "EXPLAIN",  # Azure Synapse Analytics specific
    "EXPLICIT",
    "EXTERNALPUSHDOWN",
    "FAST",
    "FIELDQUOTE",
    "FILESTREAM",
    "FILESTREAM_ON",
    "FILTER",
    "FIPS_FLAGGER",
    "FIRST",
    "FIRSTROW",
    "FMTONLY",
    "FOLLOWING",
    "FORCE",
    "FORCEPLAN",
    "FORCESCAN",
    "FORCESEEK",
    "FORMATFILE",
    "FORMATFILE_DATA_SOURCE",
    "GENERATED",
    "HASH",
    "HEAP",  # Azure Synapse Analytics specific
    "HIDDEN",
    "HINT",
    "IGNORE",
    "IGNORE_CONSTRAINTS",
    "IGNORE_DUP_KEY",
    "IGNORE_NONCLUSTERED_COLUMNSTORE_INDEX",
    "IGNORE_TRIGGERS",
    "IMPLICIT_TRANSACTIONS",
    "INCLUDE",
    "INCREMENT",
    "INLINE",
    "INSTEAD",
    "INTERVAL",
    "IO",
    "ISOLATION",
    "KEEP",
    "KEEPDEFAULTS",
    "KEEPFIXED",
    "KEEPIDENTITY",
    # LABEL is an Azure Synapse Analytics specific reserved keyword
    # but could break TSQL parsing to add there
    "LABEL",
    "LANGUAGE",
    "LAST",
    "LASTROW",
    "LEVEL",
    "LOCATION",
    "LOCK_TIMEOUT",
    "LOGIN",
    "LOOP",
    "MASKED",
    "MATCHED",
    "MAX",
    "MAXDOP",
    "MAXERRORS",
    "MAXRECURSION",
    "MAXVALUE",
    "MAX_DURATION",
    "MAX_GRANT_PERCENT",
    "MINUTES",
    "MINVALUE",
    "MIN_GRANT_PERCENT",
    "NEXT",
    "NO",
    "NOCOUNT",
    "NOEXEC",
    "NOEXPAND",
    "NOLOCK",
    "NONE",
    "NOWAIT",
    "NO_PERFORMANCE_SPOOL",
    "NUMERIC_ROUNDABORT",
    "OBJECT",
    "OFFSET",
    "ONLINE",
    "OPTIMIZE",
    "OPTIMIZE_FOR_SEQUENTIAL_KEY",
    "OUT",
    "OUTPUT",
    "OWNER",
    "PAD_INDEX",
    "PAGE",
    "PAGLOCK",
    "PARAMETER",
    "PARAMETERIZATION",
    "PARSEONLY",
    "PARTITION",
    "PARTITIONS",
    "PATH",
    "PERSISTED",
    "PRECEDING",
    "PRIOR",
    "PROFILE",
    "QUERYTRACEON",
    "QUERY_GOVERNOR_COST_LIMIT",
    "QUOTED_IDENTIFIER",
    "RANDOMIZED",
    "RANGE",
    "RAW",
    "READCOMMITTED",
    "READCOMMITTEDLOCK",
    "READONLY",
    "READPAST",
    "READUNCOMMITTED",
    "RECEIVE",
    "RECOMPILE",
    "RECURSIVE",
    "REMOTE_PROC_TRANSACTIONS",
    "RENAME",  # Azure Synapse Analytics specific
    "REPEATABLE",
    "REPEATABLEREAD",
    "RESPECT",
    "RESULT_SET_CACHING",  # Azure Synapse Analytics specific
    "RESUMABLE",
    "RETURNS",
    "ROBUST",
    "ROLE",
    "ROUND_ROBIN",  # Azure Synapse Analytics specific
    "ROW",
    "ROWLOCK",
    "ROWS",
    "S",
    "SCALEOUTEXECUTION",
    "SCHEMABINDING",
    "SELF",
    "SEQUENCE",
    "SEQUENCE_NUMBER",
    "SERIALIZABLE",
    "SERVER",
    "SETERROR",
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
    "SWITCH",
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
    "TRANSACTION_ID",
    "TRUNCATE_TARGET",  # Azure Synapse Analytics specific
    "TRY",
    "TYPE",
    "UNBOUNDED",
    "UNCOMMITTED",
    "UNKNOWN",
    "UPDLOCK",
    "USER_DB",  # Azure Synapse Analytics specific, deprecated
    "USING",
    "VALUE",
    "VIEW_METADATA",
    "WAIT_AT_LOW_PRIORITY",
    "WITHIN",
    "WORK",
    "XACT_ABORT",
    "XLOCK",
    "XML",
    "ZONE",
]

# RESERVED functions are documented at
# https://docs.microsoft.com/en-us/sql/t-sql/functions/functions?view=sql-server-ver16
# They are used with brackets (e.g. CONCAT('a', 'b')) opposed to KEYWORDS (e.g.
# CURRENT_USER)
BUILTIN_FUNCTIONS = [
    "ABS",
    "ACOS",
    "APPLOCK_MODE",
    "APPLOCK_TEST",
    "APP_NAME",
    "ASCII",
    "ASIN",
    "ASSEMBLYPROPERTY",
    "ATAN",
    "ATN2",
    "CAST",
    "CEILING",
    "CERTENCODED",
    "CERTPRIVATEKEY",
    "CHAR",
    "CHARINDEX",
    "CHOOSE",
    "COLUMNPROPERTY",
    "COL_LENGTH",
    "COL_NAME",
    "CONCAT",
    "CONCAT_WS",
    "CONVERT",
    "COS",
    "COT",
    "CUME_DIST",
    "CURSOR_STATUS",
    "DATABASEPROPERTYEX",
    "DATABASE_PRINCIPAL_ID",
    "DATEADD",
    "DATEDIFF",
    "DATEDIFF_BIG",
    "DATEFROMPARTS",
    "DATENAME",
    "DATEPART",
    "DATETIME2FROMPARTS",
    "DATETIMEFROMPARTS",
    "DATETIMEOFFSETFROMPARTS",
    "DATE_BUCKET",
    "DAY",
    "DB_ID",
    "DB_NAME",
    "DEGREES",
    "DENSE_RANK",
    "DIFFERENCE",
    "EOMONTH",
    "EXP",
    "FILEGROUPPROPERTY",
    "FILEGROUP_ID",
    "FILEGROUP_NAME",
    "FILEPROPERTY",
    "FILE_ID",
    "FILE_IDEX",
    "FILE_NAME",
    "FIRST_VALUE",
    "FLOOR",
    "FORMAT",
    "FULLTEXTCATALOGPROPERTY",
    "FULLTEXTSERVICEPROPERTY",
    "GETDATE",
    "GETUTCDATE",
    "GET_TRANSMISSION_STATUS",
    "HAS_PERMS_BY_NAME",
    "IIF",
    "INDEXKEY_PROPERTY",
    "INDEXPROPERTY",
    "INDEX_COL",
    "ISDATE",
    "ISJSON",
    "IS_MEMBER",
    "IS_ROLEMEMBER",
    "IS_SRVROLEMEMBER",
    "JSON_MODIFY",
    "JSON_PATH_EXISTS",
    "JSON_QUERY",
    "JSON_VALUE",
    "LAG",
    "LAST_VALUE",
    "LEAD",
    "LEFT",
    "LEN",
    "LOG",
    "LOG10",
    "LOGINPROPERTY",
    "LOWER",
    "LTRIM",
    "MIN_ACTIVE_ROWVERSION",
    "MONTH",
    "NCHAR",
    "NEWID",
    "NEWSEQUENTIALID",
    "NEXTVALUEFOR",
    "NTILE",
    "OBJECTPROPERTY",
    "OBJECTPROPERTYEX",
    "OBJECT_DEFINITION",
    "OBJECT_ID",
    "OBJECT_NAME",
    "OBJECT_SCHEMA_NAME",
    "ORIGINAL_DB_NAME",
    "ORIGINAL_LOGIN",
    "PARSE",
    "PARSENAME",
    "PATINDEX",
    "PERCENTILE_CONT",
    "PERCENTILE_DISC",
    "PERCENT_RANK",
    "PERMISSIONS",
    "PI",
    "POWER",
    "PWDCOMPARE",
    "PWDENCRYPT",
    "QUOTENAME",
    "RADIANS",
    "RAND",
    "RANK",
    "REPLACE",
    "REPLICATE",
    "REVERSE",
    "RIGHT",
    "ROUND",
    "ROW_NUMBER",
    "RTRIM",
    "SCHEMA_ID",
    "SCHEMA_NAME",
    "SCOPE_IDENTITY",
    "SERVERPROPERTY",
    "SIGN",
    "SIN",
    "SMALLDATETIMEFROMPARTS",
    "SOUNDEX",
    "SPACE",
    "SQRT",
    "SQUARE",
    "STATS_DATE",
    "STR",
    "STRING_AGG",
    "STRING_ESCAPE",
    "STRING_SPLIT",
    "STUFF",
    "SUBSTRING",
    "SUM",
    "SUSER_ID",
    "SUSER_NAME",
    "SUSER_SID",
    "SUSER_SNAME",
    "SWITCHOFFSET",
    "SYSDATETIME",
    "SYSDATETIMEOFFSET",
    "SYSUTCDATETIME",
    "TAN",
    "TEXTPTR",
    "TIMEFROMPARTS",
    "TODATETIMEOFFSET",
    "TRANSLATE",
    "TRIM",
    "TRY_CAST",
    "TRY_CONVERT",
    "TRY_PARSE",
    "TYPEPROPERTY",
    "TYPE_ID",
    "TYPE_NAME",
    "UNICODE",
    "UPPER",
    "USER_ID",
    "USER_NAME",
    "VERSION",
    "YEAR",
]
