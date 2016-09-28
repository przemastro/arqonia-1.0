Declare @query nvarchar(max)
Declare @value nvarchar(max)
set @query = ('set @value = (select Convert(varchar, Cast(CAST(getdate() AS TIMESTAMP) as bigint)))')
exec sp_executesql @query, @Params = N'@value varchar(50) output', @value = @value output

Declare @name varchar(100)
set @name = 'c:\backups\\'+@value+'.bak'

backup database Astro to disk = @name