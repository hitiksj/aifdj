"""The MSSQL T-SQL PDW/Azure SQL DW/Azure Synapse Analytics dialect.

https://docs.microsoft.com/en-us/sql/t-sql/language-elements/language-elements-transact-sql
https://docs.microsoft.com/en-us/sql/analytics-platform-system/tsql-statements?view=aps-pdw-2016-au7
"""

from sqlfluff.core.parser import (
    BaseSegment,
    Sequence,
    OneOf,
    Bracketed,
    Ref,
    Anything,
    Nothing,
    RegexLexer,
    CodeSegment,
    RegexParser,
    Delimited,
    Matchable,
    NamedParser,
    StartsWith,
    OptionallyBracketed,
)

from sqlfluff.core.dialects import load_raw_dialect
from sqlfluff.dialects.tsql_asa_keywords import RESERVED_KEYWORDS
from sqlfluff.dialects.tsql_asa_keywords import UNRESERVED_KEYWORDS


ansi_dialect = load_raw_dialect("ansi")
tsql_dialect = load_raw_dialect("tsql")
tsql_asa_dialect = tsql_dialect.copy_as("tsql_asa")

# Update only RESERVED Keywords
# Should really clear down the old keywords but some are needed by certain segments
# tsql_asa_dialect.sets("reserved_keywords").clear()
tsql_asa_dialect.sets("unreserved_keywords").update(UNRESERVED_KEYWORDS)

@tsql_asa_dialect.segment(replace=True)
class CreateTableStatementSegment(BaseSegment):
    """A `CREATE TABLE` statement."""

    type = "create_table_statement"
    # https://crate.io/docs/sql-99/en/latest/chapters/18.html
    # https://docs.microsoft.com/en-us/sql/t-sql/statements/create-table-azure-sql-data-warehouse?view=aps-pdw-2016-au7
    match_grammar = Sequence(
        "CREATE",
        "TABLE",
        Ref("TableReferenceSegment"),
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
        Ref("TableDistributionIndexClause")
    )


@tsql_asa_dialect.segment()
class TableDistributionIndexClause(BaseSegment):
    """`CREATE TABLE` distribution / index clause."""

    type = "table_distribution_index_clause"

    match_grammar=Sequence(
        "WITH",
        Bracketed(
            OneOf(
                Sequence(Ref("TableDistributionClause"),",",Ref("TableIndexClause")),
                Sequence(Ref("TableIndexClause"),",",Ref("TableDistributionClause")),
                Ref("TableDistributionClause"),
                Ref("TableIndexClause"),
            )
        ),
    )


@tsql_asa_dialect.segment()
class TableDistributionClause(BaseSegment):
    """`CREATE TABLE` distribution clause."""

    type = "table_distribution_clause"

    match_grammar=Sequence(
        "DISTRIBUTION",
        "=",
        OneOf(
            "REPLICATE",
            "ROUND_ROBIN",
            Sequence(
                "HASH",
                Bracketed(Ref("ColumnReferenceSegment")),
            )
        )
    )

@tsql_asa_dialect.segment()
class TableIndexClause(BaseSegment):
    """`CREATE TABLE` table index clause."""

    type = "table_index_clause"

    match_grammar=Sequence(
        OneOf(
            "HEAP",
            Sequence(
                "CLUSTERED",
                "COLUMNSTORE",
                "INDEX"
            )
        )
    )
