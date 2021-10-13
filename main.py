import enum
import sqlite3
import random

from string import ascii_letters

from nltk.tokenize import sent_tokenize, word_tokenize

WORD_STRUCTURE = {
    'n.': {
        'before': {
            'special_word': [],
            'type': []
        },
        'after': {
            'special_word': ['this', 'that', 'these', 'those', 'a', 'the', 'Some', 'any', 'a lot', 'many'],
            'type': ['article.', 'pron.']
        }
    },
    'adj.': {
        'before': {
            'special_word': [],
            'type': ['n.']
        },
        'after': {
            'special_word': ['become', 'get', 'look', 'seem', 'find', 'smell', 'sound', 'feel', 'taste', 'stay',
                             'remain', 'keep'],
            'type': ['i.', 'v.']  # i. is linking verb
        }
    },
    'adv.': {
        'before': {
            'special_word': [],
            'type': ['v.', 'adj.', 'adv.']
        },
        'after': {
            'special_word': [],
            'type': ['n.', 'v.']
        },
        'special_structure': [
            '1st_line'
        ]
    },
    'v.': {
        'after': {
            'special_word': [],
            'type': ['n.']
        }
    }
}


class WordType(enum.Enum):
    Noun = 'n.'
    Subject = 's.'
    Verb = 'v.'
    Adjective = 'adj.'
    Adverb = 'adv.'
    Pronounce = 'pron.'
    Article = 'article.'
    PastParticiple = 'p. p.'  # v2
    Etymology = 'imp.'  # v3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connection_db():
    con = sqlite3.connect('Dictionary.db')
    con.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    return con.cursor()


dictionary_db = connection_db()


def find_words_in_db(words):
    sql = """SELECT *  FROM entries WHERE lower(word) IN {}"""
    cursor = dictionary_db.execute(sql.format(tuple(words)))
    return cursor.fetchall()


def find_word_family(word):
    sql = """SELECT * FROM entries WHERE """
    return


def random_number(data=None):
    if data:
        return random.randint(0, len(data) - 1)
    return random.random()


def make_sentence_incorrect(sentence):
    """Make sentence incorrect"""
    words = word_tokenize(sentence)
    words = [w.lower() for w in words]
    list_words_in_dictionary = find_words_in_db(words)
    type_group_by_word = {}
    for w in list_words_in_dictionary:
        raw_word = (w.get('word') or '').lower()
        if not type_group_by_word.get(raw_word):
            type_group_by_word[raw_word] = []
        word_type = (w.get('wordtype') or '').split(' & ')
        for w_type in word_type:
            if w_type not in type_group_by_word[raw_word]:
                type_group_by_word[raw_word].append(w_type)

    while 1 != 0:
        random_word_index = random_number(words)
        modify_word = words[random_word_index]
        word_types = type_group_by_word.get(modify_word)
        if set(modify_word).difference(ascii_letters):
            continue

        if not word_types:
            continue

        previous_word = words[random_word_index - 1]
        if set(previous_word).difference(ascii_letters):
            next_word = words[random_word_index + 1]
        previous_word_type = type_group_by_word[previous_word]


        return sentence


def main():
    # change file name for each person then merge after
    f = open("rawData.thang.txt", "r")
    data = f.read()
    correct_sentence_file = open("correctSentence.thang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)

    for sentence in sentences:
        print(sentence)
        correct_sentence_file.write(sentence + '\n')
        incorrect_sentence = make_sentence_incorrect(sentence)


main()
