CREATE PROC Reporting.DeclareProblem AS
BEGIN

	DECLARE @startdate AS DATE;

	DECLARE @DateNow DATE = GETDATE();

	DECLARE @DateStart DATETIME2 = GETDATE()
			,@DateEnd DATETIME2 = GETDATE()

	DECLARE @EOMONTH DATE = ('1900-01-01')

	SET @EOMONTH = ('2000-01-01')

	SET @EOMONTH = ('2001-01-01');

	IF OBJECT_ID('tempdb..#UP') IS NOT NULL DROP TABLE #UP;


END
