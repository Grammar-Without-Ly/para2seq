import enum
import sqlite3
import random

from string import ascii_letters

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

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


class WordTypeDatabase(enum.Enum):
    Noun = 'n.'
    Subject = 's.'
    Verb = 'v.'
    Adjective = 'adj.'
    Adverb = 'adv.'
    Pronounce = 'pron.'
    Article = 'article.'
    PastParticiple = 'p. p.'  # v2
    Etymology = 'imp.'  # v3


class WordTypeWordNet(enum.Enum):
    ADJ, ADJ_SAT, ADV, NOUN, VERB = "a", "s", "r", "n", "v"


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


def words_list_to_sentence(words_list):
    result = ''
    index_of_word = 0
    for w in words_list:
        index_of_word += 1
        if index_of_word == 1:
            result += w.capitalize()
            continue
        if set(w).difference(ascii_letters):
            result += w
        result += ' ' + w
    return result


def make_sentence_incorrect(sentence):
    """Make sentence incorrect"""
    raw_words = word_tokenize(sentence)
    # words = [w.lower() for w in words]
    words = []
    for w in raw_words:
        w = w.lower()
        if w.find('es') == (len(w) - 2):
            w = w.replace('es', '')
        if w.find('s') == (len(w) - 1):
            w = w.replace('s', '')
        words.append(w)
    list_words_in_dictionary = find_words_in_db(words)
    type_group_by_word = {}
    for w in list_words_in_dictionary:
        raw_word = (w.get('word') or '').lower()
        if not type_group_by_word.get(raw_word):
            type_group_by_word[raw_word] = []
        word_type = (w.get('wordtype') or '').split(' & ')
        for w_type in word_type:
            w_type = w_type.split(' ')
            for t in w_type:
                if t not in type_group_by_word[raw_word]:
                    type_group_by_word[raw_word].append(t)

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
        type_to_change = None
        for t in word_types:
            if not WORD_STRUCTURE.get(t):
                continue
            current_type = WORD_STRUCTURE[t].get('after') or {}
            if previous_word in current_type.get('special_word'):
                correct_type = t

            number_of_find_type = 0
            while 1 != 0:
                if number_of_find_type > 5:
                    break

                number_of_find_type += 1
                random_type = WordTypeDatabase(list(WordTypeDatabase)[random.randint(0, 8)])
                if random_type not in [WordTypeDatabase.PastParticiple, WordTypeDatabase.Etymology] \
                        and (random_type.value not in current_type['type']) and (t != random_type.value):
                    type_to_change = random_type
                    break
                else:
                    continue

        if not type_to_change:
            continue
        if type_to_change == WordTypeDatabase.Noun:
            type_to_change = WordTypeWordNet.NOUN.value
        elif type_to_change == WordTypeDatabase.Verb:
            type_to_change = WordTypeDatabase.Verb.value
        elif type_to_change == WordTypeDatabase.Adverb:
            type_to_change = WordTypeWordNet.ADV.value
        elif type_to_change == WordTypeDatabase.Adjective:
            type_to_change = WordTypeWordNet.ADJ.value
        else:
            continue

        print(previous_word)
        print(WordNetLemmatizer.lemmatize('the', 'a'))
        a = WordNetLemmatizer.lemmatize(previous_word, type_to_change)
        print(a)
        words[random_word_index - 1] = previous_word
        return words_list_to_sentence(words)


def main():
    # change file name for each person then merge after
    f = open("rawData.thang.txt", "r")
    data = f.read()
    correct_sentence_file = open("correctSentence.thang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    for sentence in sentences:
        correct_sentence_file.write(sentence + '\n')
        incorrect_sentence = make_sentence_incorrect(sentence)


main()
