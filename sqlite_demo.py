import sqlite3

conn = sqlite3.connect('test.db')

c = conn.cursor()

# c.execute("""CREATE TABLE employees (
#             first text,
#             last text,
#             pay integer
#             )""")

# c.execute("INSERT INTO employees VALUES ('Mary', 'Gubkin', 70000)")

# conn.commit()

c.execute("SELECT * FROM employees WHERE last='Gubkin'")

print(c.fetchall())


conn.commit()

conn.close()
