import enum
import sqlite3
import random

from string import ascii_letters
from nltk import pos_tag, ChartParser, CFG

from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

WORD_STRUCTURE = {
    'N': {
        'before': {
            'special_word': [],
            'type': ['R', 'V']
        },
        'after': {
            'special_word': ['this', 'that', 'these', 'those', 'a', 'the', 'Some', 'any', 'a lot', 'many'],
            'type': []
        }
    },
    'J': {
        'before': {
            'special_word': [],
            'type': ['N']
        },
        'after': {
            'special_word': ['become', 'get', 'look', 'seem', 'find', 'smell', 'sound', 'feel', 'taste', 'stay',
                             'remain', 'keep'],
            'type': ['V']  # i. is linking verb
        }
    },
    'R': {
        'before': {
            'special_word': [],
            'type': ['V', 'J.', 'R']
        },
        'after': {
            'special_word': [],
            'type': ['N', 'V']
        },
        'special_structure': [
            '1st_line'
        ]
    },
    'V': {
        'after': {
            'special_word': [],
            'type': ['N']
        }
    }
}


class WordTypeDatabase(enum.Enum):
    Noun = 'N'
    Verb = 'V'
    Adjective = 'J'
    Adverb = 'R'


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
            continue
        result += ' ' + w
    return result


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV
                }

    return tag_dict.get(tag)


def make_sentence_incorrect(sentence):
    """Make sentence incorrect"""
    text = word_tokenize(sentence)
    stemmer = SnowballStemmer('english')
    sentence_struct = {}
    for index, word in enumerate(text):
        form = get_wordnet_pos(word)
        sentence_struct[index] = {
            'word': word,
            'word_form': form.upper() if form else None
        }
    try_time = 0
    while 1 != 0:
        if try_time > 5:
            return None
        try_time += 1
        random_index_word = random.randint(0, len(text) - 1)
        current_word = sentence_struct[random_index_word]
        if set(current_word['word']).difference(ascii_letters) or not current_word['word_form']:
            continue
        tried = 0
        type_to_change = None
        while 1 != 0:
            if tried > 5:
                break
            tried += 1
            type_to_change = list(WordTypeDatabase)[random_index_word % 4]
            if type_to_change.value != current_word['word_form']:
                print(type_to_change.value + '----->' + current_word['word_form'])
                break

        if not type_to_change:
            continue
        ADJ, ADJ_SAT, ADV, NOUN, VERB = "a", "s", "r", "n", "v"
        if type_to_change == WordTypeDatabase.Adjective:
            type_to_change = ADJ
        elif type_to_change == WordTypeDatabase.Adverb:
            type_to_change = ADV
        elif type_to_change == WordTypeDatabase.Noun:
            type_to_change = NOUN
        elif type_to_change == WordTypeDatabase.Verb:
            type_to_change = VERB
        else:
            continue
        test = WordNetLemmatizer().lemmatize(stemmer.stem(current_word['word']), pos=type_to_change)
        print(current_word)
        print({'1': test, '2': type_to_change})
        print('---------------------')
        text[random_index_word] = test
        break
        # for happy_lemma in wordnet.lemmas():
        #     forms.add(happy_lemma)
        #     for related_lemma in happy_lemma.derivationally_related_forms():
        #         forms.add(related_lemma)
        # for lem in forms:
        #     print(lem)
        # break
    return words_list_to_sentence(text)


def main():
    # change file name for each person then merge after
    f = open("rawData.thang.txt", "r")
    data = f.read()
    correct_sentence_file = open("correctSentence.thang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    for sentence in sentences:
        incorrect_sentence = make_sentence_incorrect(sentence)
        if not incorrect_sentence:
            print('---skip-----')
            continue
        correct_sentence_file.write(sentence + '\n')
        correct_sentence_file.write(incorrect_sentence + '\n')


main()
