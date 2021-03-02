import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (id INTEGER PRIMARY KEY AUTOINCREMENT, \
    name TEXT NOT NULL, stars real, daily REAL NOT NULL, state TEXT NOT NULL, city TEXT NOT NULL)"

cria_hotel = "INSERT INTO hoteis (name, stars, daily, state, city) VALUES \
    ('Pigatto Hotel', 4, 345,'Rio Grande do Sul', 'Frederico Westphalen')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)
connection.commit()
connection.close()