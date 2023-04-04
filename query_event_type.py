# Just a debug program I use to query different event types in the database
# Don't run this unless you're working on the code
db = sqlite3.connect("database.db")
cursor = db.cursor()
while True:
    print(cursor.execute(f'SELECT * FROM socket_recv WHERE json LIKE \'%"t":"'+input("event> ")+'"%\'').fetchone())