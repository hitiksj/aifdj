CREATE TABLE [dbo].[EC DC] (
    [Column B] [varchar](100),
    [ColumnC] varchar(100),
    [ColumnDecimal] decimal(10,3)
)

-- Test various forms of quoted data types
CREATE TABLE foo (
    pk int PRIMARY KEY,
    quoted_name [custom udt],
    qualified_name sch.qualified,
    quoted_qualified "my schema".qualified,
    more_quoted "my schema"."custom udt",
    quoted_udt sch.[custom udt]
);

-- computed column
-- https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver16#column_name-as-computed_column_expression
-- https://learn.microsoft.com/en-us/sql/relational-databases/tables/specify-computed-columns-in-a-table?view=sql-server-ver16
CREATE TABLE dbo.Products (
    ProductID int IDENTITY (1,1) NOT NULL
    , InventoryTs datetime2(0)
    , QtyAvailable smallint
    , QtySold smallint
    , UnitPrice money
    , InventoryValue AS QtyAvailable * UnitPrice
    , [SoldValue] AS (QtySold * [UnitPrice])
    , InventoyDate AS CAST(InventoryTs AS date)
);
