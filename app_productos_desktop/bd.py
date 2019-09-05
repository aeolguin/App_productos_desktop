import mysql.connector
db=mysql.connector.connect(
    host="localhost",
    user="ariel1",
    passwd="martina2712",
    db="database")
c = db.cursor(mysql.cursors.DictCursor)
c.execute("SELECT * FROM producto")
result_set = c.fetchall()
for row in result_set:
    print(row["Nombre"])