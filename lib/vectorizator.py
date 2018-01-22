import json

BASIS = list('abcdefghijklmnopqrstuvwxyz')


def load_words():
    try:
        filename = "dictionary.json"
        with open(filename,"r") as english_dictionary:
            valid_words = json.load(english_dictionary)
            return valid_words
    except Exception as e:
        return str(e)


def vectorize(word):
    letters = {x: 0 for x in BASIS}
    word_arr = list(word.lower())
    for symbol in word_arr:
        if symbol not in BASIS:
            continue
        letters[symbol] += 1
    return ''.join([str(x) for x in list(letters.values())])


def levenstein(a, b):
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def missed(s):
    res = [s]

    arr = [int(x) for x in list(s)]
    for i in range(len(arr)):
        arr[i] += 1
        res.append(''.join([str(x) for x in arr]))
        arr[i] -= 1

    return res
