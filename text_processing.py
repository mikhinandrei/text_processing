import re
import postgresql.driver as driver
import scipy as sp
import lib.vectorizator as vec


def dist_raw(v1, v2):
    v1_norm = v1/sp.linalg.norm(v1.toarray())
    v2_norm = v2/sp.linalg.norm(v2.toarray())
    delta = v1_norm - v2_norm
    return sp.linalg.norm(delta.toarray())


if __name__ == '__main__':
    word = input()
    db = driver.connect(user='postgres', password='postgres', host='localhost', database='text_db', port=5432)

    f = vec.vectorize(word)

    dist = {}
    sorted_keys = []

    for line in vec.missed(f):
        for row in db.query("SELECT * FROM words WHERE vector = '%s'" % (line)):
            dist[row['word'].rstrip()] = vec.levenstein(word.lower(), row['word'].rstrip())

    sorted_keys = sorted(dist.keys(), key=lambda key: dist[key])
    print("Maybe you wanted to write ", sorted_keys[0], dist[sorted_keys[0]])
