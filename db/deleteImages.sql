Declare @query nvarchar(max)
set @query = ('delete from [Astro].[data].[images] where UploadTime < (select dateadd(hh,-24,getdate()))')
exec sp_executesql @query