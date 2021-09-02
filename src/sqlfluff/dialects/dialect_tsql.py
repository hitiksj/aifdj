""" The MSSQL T-SQL dialect.

https://docs.microsoft.com/en-us/sql/t-sql/language-elements/language-elements-transact-sql


"""
from enum import Enum
from typing import Any, Generator, List, Tuple, NamedTuple, Optional, Union

from sqlfluff.core.parser import (
    BaseSegment,
    Sequence,
    OneOf,
    Bracketed,
    Ref,
    Anything,
    RegexLexer,
    CodeSegment,
    RegexParser,
    Delimited,
    OptionallyBracketed,
    AnyNumberOf,
)

from sqlfluff.core.dialects.base import Dialect
from sqlfluff.core.dialects.common import AliasInfo
from sqlfluff.core.parser.segments.base import BracketedSegment

from sqlfluff.dialects.ansi_keywords import (
    ansi_reserved_keywords,
    ansi_unreserved_keywords,
)


from sqlfluff.core.dialects import load_raw_dialect
from sqlfluff.dialects.dialect_ansi import StatementSegment

ansi_dialect = load_raw_dialect("ansi")
tsql_dialect = ansi_dialect.copy_as("tsql")


# Update only RESERVED Keywords, not working yet, error UsingKeywordSegment
# from sqlfluff.dialects.tsql_keywords import (
#     RESERVED_KEYWORDS,
# )
# tsql_dialect.sets("reserved_keywords").clear()
# tsql_dialect.sets("reserved_keywords").update(RESERVED_KEYWORDS)


tsql_dialect.replace(
    ParameterNameSegment=RegexParser(
        r"[@][A-Za-z0-9_]+", CodeSegment, name="parameter", type="parameter"
    ),
    QuotedIdentifierSegment=Bracketed(
        RegexParser(
            r"[A-Z][A-Z0-9_]*", CodeSegment, name="quoted_identifier", type="identifier"
        ),
        bracket_type="square",
    ),
    # QuotedIdentifierSegment=NamedParser(
    #     BracketedSegment(
    #         CodeSegment,
    #         start_bracket="sq_brackets_open",
    #         end_bracket="sq_brackets_close",
    #     ),
    #     name="quoted_identifier",
    #     type="identifier",
    # )
)

tsql_dialect.insert_lexer_matchers(
    [
        RegexLexer(
            "atsign",
            r"[@][a-zA-Z0-9_]+",
            CodeSegment,
        ),
    ],
    before="code",
)

# Below statement or similar is required to make sqlfluff understand the different statements within a file as these are not seperated by semicolons.
@tsql_dialect.segment(replace=True)
class StatementSegment(BaseSegment):
    """A generic segment, to any of its child subsegments."""

    type = "statement"
    match_grammar = OneOf(
        Ref("SelectableGrammar"),
        Ref("InsertStatementSegment"),
        Ref("TransactionStatementSegment"),
        Ref("DropStatementSegment"),
        Ref("TruncateStatementSegment"),
        Ref("AlterDefaultPrivilegesSegment"),
        Ref("AccessStatementSegment"),
        Ref("CreateTableStatementSegment"),
        Ref("CreateTypeStatementSegment"),
        Ref("CreateRoleStatementSegment"),
        Ref("AlterTableStatementSegment"),
        Ref("CreateSchemaStatementSegment"),
        Ref("SetSchemaStatementSegment"),
        Ref("DropSchemaStatementSegment"),
        Ref("CreateDatabaseStatementSegment"),
        Ref("CreateExtensionStatementSegment"),
        Ref("CreateIndexStatementSegment"),
        Ref("DropIndexStatementSegment"),
        Ref("CreateViewStatementSegment"),
        Ref("DeleteStatementSegment"),
        Ref("UpdateStatementSegment"),
        Ref("CreateFunctionStatementSegment"),
        Ref("CreateModelStatementSegment"),
        Ref("DropModelStatementSegment"),
        Ref("DescribeStatementSegment"),
        Ref("UseStatementSegment"),
        Ref("ExplainStatementSegment"),
        Ref("ExplainStatementSegment"),
        Ref("CreateProcedureStatementSegment"),
    )


#     parse_grammar = OneOf(
#         Ref("SelectableGrammar"),
#         Ref("InsertStatementSegment"),
#         Ref("TransactionStatementSegment"),
#         Ref("DropStatementSegment"),
#         Ref("TruncateStatementSegment"),
#         Ref("AlterDefaultPrivilegesSegment"),
#         Ref("AccessStatementSegment"),
#         Ref("CreateTableStatementSegment"),
#         Ref("CreateTypeStatementSegment"),
#         Ref("CreateRoleStatementSegment"),
#         Ref("AlterTableStatementSegment"),
#         Ref("CreateSchemaStatementSegment"),
#         Ref("SetSchemaStatementSegment"),
#         Ref("DropSchemaStatementSegment"),
#         Ref("CreateDatabaseStatementSegment"),
#         Ref("CreateExtensionStatementSegment"),
#         Ref("CreateIndexStatementSegment"),
#         Ref("DropIndexStatementSegment"),
#         Ref("CreateViewStatementSegment"),
#         Ref("DeleteStatementSegment"),
#         Ref("UpdateStatementSegment"),
#         Ref("CreateFunctionStatementSegment"),
#         Ref("CreateModelStatementSegment"),
#         Ref("DropModelStatementSegment"),
#         Ref("DescribeStatementSegment"),
#         Ref("UseStatementSegment"),
#         Ref("ExplainStatementSegment"),
#     )


@tsql_dialect.segment()
class GoStatementSegment(BaseSegment):
    """This is a Go statement to signal end of batch"""

    type = "go_statement"
    type = "go_statement"
    match_grammar = Sequence("GO")


@tsql_dialect.segment()
class SchemaNameSegment(BaseSegment):
    """This is a schema name optionally bracketed"""

    type = "schema_name"
    name = "schema"
    match_grammar = Sequence(
        Ref("StartSquareBracketSegment", optional=True),
        Ref("SingleIdentifierGrammar"),
        Ref("EndSquareBracketSegment", optional=True),
        Ref("DotSegment"),
    )


@tsql_dialect.segment()
class ObjectNameSegment(BaseSegment):
    """This is the body of a `CREATE FUNCTION AS` statement."""

    type = "object_name"
    match_grammar = Sequence(
        Ref("StartSquareBracketSegment", optional=True),
        Ref("SingleIdentifierGrammar"),
        Ref("EndSquareBracketSegment", optional=True),
    )


# @tsql_dialect.segment(replace=True)
# class TableConstraintSegment(BaseSegment):
#     """A table constraint, e.g. for CREATE TABLE."""

#     type = "table_constraint_definition"
#     # Later add support for CHECK constraint, others?
#     # e.g. CONSTRAINT constraint_1 PRIMARY KEY(column_1)
#     match_grammar = Sequence(
#         Sequence(  # [ CONSTRAINT <Constraint name> ]
#             "CONSTRAINT", Ref("ObjectReferenceSegment"), optional=True
#         ),
#         OneOf(
#             Sequence(  # UNIQUE ( column_name [, ... ] )
#                 "UNIQUE",
#                 Ref("BracketedColumnReferenceListGrammar"),
#                 # Later add support for index_parameters?
#             ),
#             Sequence(  # PRIMARY KEY ( column_name [, ... ] ) index_parameters
#                 Ref("PrimaryKeyGrammar"),
#                 # Columns making up PRIMARY KEY constraint
#                 Ref("BracketedColumnReferenceListGrammar"),
#                 # Later add support for index_parameters?
#             ),
#             Sequence(  # FOREIGN KEY ( column_name [, ... ] )
#                 # REFERENCES reftable [ ( refcolumn [, ... ] ) ]
#                 "FOREIGN",
#                 "KEY",
#                 # Local columns making up FOREIGN KEY constraint
#                 Ref("BracketedColumnReferenceListGrammar"),
#                 "REFERENCES",
#                 Ref("ColumnReferenceSegment"),
#                 # Foreign columns making up FOREIGN KEY constraint
#                 Ref("BracketedColumnReferenceListGrammar"),
#                 # Later add support for [MATCH FULL/PARTIAL/SIMPLE] ?
#                 # Later add support for [ ON DELETE/UPDATE action ] ?
#             ),
#         ),
#     )


@tsql_dialect.segment(replace=True)
class CreateTableStatementSegment(BaseSegment):
    """A `CREATE TABLE` statement."""

    type = "create_table_statement"
    # https://docs.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver15

    match_grammar = Sequence(
        "CREATE",
        Ref("OrReplaceGrammar", optional=True),
        Ref("TemporaryTransientGrammar", optional=True),
        "TABLE",
        Ref("IfNotExistsGrammar", optional=True),
        Ref("SchemaNameSegment", optional=True),
        Ref("TableReferenceSegment"),
        # Anything(),
        OneOf(
            # Columns and comment syntax:
            Sequence(
                Bracketed(
                    Delimited(
                        OneOf(
                            Ref("TableConstraintSegment"),
                            Ref("ColumnDefinitionSegment"),
                        ),
                    )
                ),
                Ref("CommentClauseSegment", optional=True),
            ),
            # Create AS syntax:
            Sequence(
                "AS",
                OptionallyBracketed(Ref("SelectableGrammar")),
            ),
            # Create like syntax
            Sequence("LIKE", Ref("TableReferenceSegment")),
        ),
        Ref("GoStatementSegment", optional=True),
    )


# @tsql_dialect.segment(replace=True)
# class DatatypeIdentifierSegment(BaseSegment):
#     name="data_type_identifier",
#     type="data_type_identifier",
#     match_grammar = RegexParser(
#         r"\[?[A-Z][A-Z0-9_]*\]?",
#         CodeSegment,
#     ),


@tsql_dialect.segment(replace=True)
class DatatypeSegment(BaseSegment):
    """A data type segment."""

    type = "data_type"
    match_grammar = Sequence(
        Sequence(
            # Some dialects allow optional qualification of data types with schemas
            Sequence(
                Ref("StartSquareBracketSegment", optional=True),
                Ref("SingleIdentifierGrammar"),
                Ref("EndSquareBracketSegment", optional=True),
                Ref("DotSegment"),
                allow_gaps=False,
                optional=True,
            ),
            Ref("StartSquareBracketSegment", optional=True),
            Ref("DatatypeIdentifierSegment"),
            Ref("EndSquareBracketSegment", optional=True),
            allow_gaps=False,
        ),
        Bracketed(
            OneOf(
                Delimited(Ref("ExpressionSegment")),
                # The brackets might be empty for some cases...
                optional=True,
            ),
            # There may be no brackets for some data types
            optional=True,
        ),
        Ref("CharCharacterSetSegment", optional=True),
    )


@tsql_dialect.segment(replace=True)
class ColumnOptionSegment(BaseSegment):
    """A column option; each CREATE TABLE column can have 0 or more."""

    type = "column_constraint"
    # Column constraint from
    # https://www.postgresql.org/docs/12/sql-createtable.html
    match_grammar = Sequence(
        Sequence(
            "CONSTRAINT",
            Ref("ObjectReferenceSegment"),  # Constraint name
            optional=True,
        ),
        OneOf(
            Sequence(Ref.keyword("NOT", optional=True), "NULL"),  # NOT NULL or NULL
            Sequence(  # DEFAULT <value>
                "DEFAULT",
                OneOf(
                    Ref("LiteralGrammar"),
                    Ref("FunctionSegment"),
                    # ?? Ref('IntervalExpressionSegment')
                ),
            ),
            Ref("PrimaryKeyGrammar"),
            "UNIQUE",  # UNIQUE
            "CLUSTERED",
            "AUTO_INCREMENT",  # AUTO_INCREMENT (MySQL)
            "UNSIGNED",  # UNSIGNED (MySQL)
            Sequence(  # REFERENCES reftable [ ( refcolumn) ]
                "REFERENCES",
                Ref("ColumnReferenceSegment"),
                # Foreign columns making up FOREIGN KEY constraint
                Ref("BracketedColumnReferenceListGrammar", optional=True),
            ),
            Ref("CommentClauseSegment"),
        ),
    )


@tsql_dialect.segment(replace=True)
class ColumnDefinitionSegment(BaseSegment):
    """A column definition, e.g. for CREATE TABLE or ALTER TABLE."""

    type = "column_definition"
    match_grammar = Sequence(
        Ref("StartSquareBracketSegment", optional=True),
        Ref("SingleIdentifierGrammar"),  # Column name
        Ref("EndSquareBracketSegment", optional=True),
        Ref("DatatypeSegment"),  # Column type
        Bracketed(Anything(), optional=True),  # For types like VARCHAR(100)
        AnyNumberOf(
            Ref("ColumnOptionSegment", optional=True),
        ),
    )


@tsql_dialect.segment(replace=True)
class CreateFunctionStatementSegment(BaseSegment):
    """A `CREATE FUNCTION` statement.

    This version in the TSQL dialect should be a "common subset" of the
    structure of the code for those dialects.
    postgres: https://www.postgresql.org/docs/9.1/sql-createfunction.html
    snowflake: https://docs.snowflake.com/en/sql-reference/sql/create-function.html
    bigquery: https://cloud.google.com/bigquery/docs/reference/standard-sql/user-defined-functions
    tsql/mssql : https://docs.microsoft.com/en-us/sql/t-sql/statements/create-function-transact-sql?view=sql-server-ver15
    """

    type = "create_function_statement"

    match_grammar = Sequence(
        "CREATE",
        Sequence("OR", "ALTER", optional=True),
        "FUNCTION",
        Anything(),
    )
    parse_grammar = Sequence(
        "CREATE",
        Sequence("OR", "ALTER", optional=True),
        "FUNCTION",
        Ref("SchemaNameSegment"),
        Ref("ObjectNameSegment"),
        Ref("FunctionParameterListGrammar"),
        Sequence(  # Optional function return type
            "RETURNS",
            Ref("DatatypeSegment"),
            optional=True,
        ),
        "AS",
        Ref("FunctionDefinitionGrammar"),
        Ref("GoStatementSegment", optional=True),
    )


@tsql_dialect.segment(replace=True)
class FunctionDefinitionGrammar(BaseSegment):
    """This is the body of a `CREATE FUNCTION AS` statement."""

    type = "function_statement"
    name = "function_statement"

    match_grammar = Sequence(Anything())


@tsql_dialect.segment()
class CreateProcedureStatementSegment(BaseSegment):
    """A `CREATE PROCEDURE` statement.
    https://docs.microsoft.com/en-us/sql/t-sql/statements/create-procedure-transact-sql?view=sql-server-ver15
    """

    type = "create_procedure_statement"

    match_grammar = Sequence(
        "CREATE",
        Sequence("OR", "ALTER", optional=True),
        OneOf("PROCEDURE", "PROC"),
        Ref("SchemaNameSegment", optional=True),
        Ref("ObjectNameSegment"),
        Ref("FunctionParameterListGrammar", optional=True),
        "AS",
        Ref("ProcedureDefinitionGrammar"),
        Ref("GoStatementSegment", optional=True),
    )


@tsql_dialect.segment()
class ProcedureDefinitionGrammar(BaseSegment):
    """This is the body of a `CREATE OR ALTER PROCEDURE AS` statement."""

    type = "procedure_statement"
    name = "procedure_statement"

    match_grammar = Sequence(Anything())


@tsql_dialect.segment(replace=True)
class CreateViewStatementSegment(BaseSegment):
    """A `CREATE VIEW` statement."""

    type = "create_view_statement"
    # https://docs.microsoft.com/en-us/sql/t-sql/statements/create-view-transact-sql?view=sql-server-ver15#examples
    match_grammar = Sequence(
        "CREATE",
        Sequence("OR", "ALTER", optional=True),
        "VIEW",
        Ref("SchemaNameSegment", optional=True),
        Ref("ObjectNameSegment"),
        "AS",
        Ref("SelectableGrammar"),
        Ref("GoStatementSegment", optional=True),
    )
