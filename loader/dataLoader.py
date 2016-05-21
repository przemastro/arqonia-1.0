import pyodbc


connection = pyodbc.connect('Driver={SQL Server};Server=SAMSUNG-PC\SQLEXPRESS;Database=astro;Trusted_Connection=yes;uid=SAMSUNG-PC\SAMSUNG;pwd=')

cursor = connection.cursor()

insert_value = ("insert into tychoStaging(id, Name) values(2,'testowo')")

print insert_value

cursor.execute(insert_value)
connection.commit()

cursor.close()

connection.close()
