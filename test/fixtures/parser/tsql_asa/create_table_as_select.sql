CREATE TABLE [dbo].[PL_stage]
WITH (DISTRIBUTION = HASH([ID]), HEAP)
AS
SELECT 	 e.[ID]
		,e.[ArriveDate]
		,e.[Contribution]
		,e.[DischargeDate]
		,e.[Encounter]
		,e.[Facility]
		,e.[Region]
		,e.[LOS]
FROM dbo.Encounter e
JOIN dbo.Finance f ON e.[ID] = f.[ID]
