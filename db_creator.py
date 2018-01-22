import postgresql.driver as driver
import lib.vectorizator as vec

db = driver.connect(user='postgres', password='postgres', host='localhost', database='text_db', port=5432)
db.execute("DROP TABLE words")
db.execute("CREATE TABLE IF NOT EXISTS words (id SERIAL PRIMARY KEY, word CHAR(32), vector CHAR(128))")

query = 'INSERT INTO words (word, vector) VALUES '

values = []

i = 0

english_words = vec.load_words()
for key in english_words.keys():
    query += "('%s', '%s') ," % (key, vec.vectorize(key))
    values.append(key)
    values.append(vec.vectorize(key))
    if i >= 1000000:
        query = query[:-2]
        db.query(query)
        query = 'INSERT INTO words (word, vector) VALUES '
        i = 0
    i += 1

query = query[:-2]
db.query(query)

db.query('CREATE INDEX vectors ON words(vector)')

db.close()