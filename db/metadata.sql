SET NOCOUNT ON


;with cte 
        (
		ID,
		StagingTable,
		DeltaTable
		)
		as (
		SELECT 1,
		       N'stg.stagingObservations',
			   N'bi.observations'
			   )
INSERT INTO util.metadataCounts
               ( ID,
		         StagingTable,
				 DeltaTable
			   )
			   select * from cte

;With cte
        (
		ID,
		MetadataCountsId,
		StagingColumn,
		DeltaColumn,
		DeltaColumnId,
		PhotometryTable,
		DataTypeConversion,
		NullValuesConversion,
		JoinHint
		)
		as (
		SELECT 1,
		       1,
			   N'uPhotometry',
			   N'uPhotometry',
			   N'uPhotometryId',
			   N'bi.uPhotometry',
			   N'cast(uPhotometry as varchar)',
			   N'null',
			   N'inner join'
        UNION ALL
		SELECT 2,
		       1,
			   N'vPhotometry',
			   N'vPhotometry',
			   N'vPhotometryId',
			   N'bi.vPhotometry',
			   N'cast(vPhotometry as varchar)',
			   N'null',
			   N'inner join'
        UNION ALL
		SELECT 3,
		       1,
			   N'bPhotometry',
			   N'bPhotometry',
			   N'bPhotometryId',
			   N'bi.bPhotometry',
			   N'cast(bPhotometry as varchar)',
			   N'null',
			   N'inner join'
        UNION ALL
		SELECT 4,
		       1,
			   N'uPhotometryTime',
			   N'uPhotometryTime',
			   N'uPhotometryTimeId',
			   N'bi.uPhotometryTime',
			   N'cast(uPhotometryTime as varchar)',
			   N'null',
			   N'inner join'   
		UNION ALL
		SELECT 5,
		       1,
			   N'vPhotometryTime',
			   N'vPhotometryTime',
			   N'vPhotometryTimeId',
			   N'bi.vPhotometryTime',
			   N'cast(vPhotometryTime as varchar)',
			   N'null',
			   N'inner join' 
        UNION ALL
		SELECT 6,
		       1,
			   N'bPhotometryTime',
			   N'bPhotometryTime',
			   N'bPhotometryTimeId',
			   N'bi.bPhotometryTime',
			   N'cast(bPhotometryTime as varchar)',
			   N'null',
			   N'inner join' 
			   )
INSERT INTO util.metadataComparison
               ( ID,
		         MetadataCountsId,
		         StagingColumn,
		         DeltaColumn,
		         DeltaColumnId,
				 PhotometryTable,
		         DataTypeConversion,
		         NullValuesConversion,
		         JoinHint
			   )
			   select * from cte
GO
