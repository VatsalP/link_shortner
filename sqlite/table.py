import sqlite3

with sqlite3.connect("../link_shortner.db") as db:
    c = db.cursor()
    with open("./table.sql", 'r') as file:
        c.executescript(file.read())
