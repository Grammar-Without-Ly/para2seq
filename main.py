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
    index_of_quote = 0
    for w in words_list:
        index_of_word += 1
        if index_of_word == 1:
            result += w.capitalize()
            continue
        if set(w).difference(ascii_letters):
            if w == '"':
                index_of_quote += 1
                if (index_of_quote % 2) == 1:
                    result += ' ' + w
                    continue
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
    if len(text) < 3:
        return
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
        if try_time > 1000:
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
        # word_stem = stemmer.stem(current_word['word'])
        # test = WordNetLemmatizer().lemmatize(word_stem, pos=type_to_change)
        # if current_word['word'] == test:
        #     continue
        # print(current_word)

        allow_word_type = ["a", "s", "r", "n", "v"]
        forms = {}
        # print(current_word['word'])
        # print(current_word['word_form'].lower())
        if current_word['word_form'].lower() not in allow_word_type:
            continue
        for happy_lemma in wordnet.lemmas(
                WordNetLemmatizer().lemmatize(current_word['word'], current_word['word_form'].lower())):
            w_form = happy_lemma.synset().pos()
            forms[w_form] = happy_lemma.name()
            for related_lemma in happy_lemma.derivationally_related_forms():
                r_w_form = related_lemma.synset().pos()
                forms[r_w_form] = related_lemma.name()

        if not forms.get(type_to_change):
            continue
        change_word = forms.get(type_to_change)
        if (change_word.lower() == current_word['word'].lower()) or (
                type_to_change.lower() == current_word['word_form'].lower()):
            continue
        text[random_index_word] = forms.get(type_to_change)
        print(sentence)
        print(current_word['word_form'] + '----->' + type_to_change)
        # print({'word': current_word['word'], 'word_form': current_word['word_form'].lower()})
        # print({'1': forms[type_to_change], '2': type_to_change})
        print(current_word['word'] + '---->' + forms[type_to_change])
        print('---------------------')
        return sentence.replace(current_word['word'], forms[type_to_change])


skip_sentence = []

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def change_structure(correct_structure):
    lemmatizer = WordNetLemmatizer()
    word_list=[lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(correct_structure)]
    # print(word_list)
    lemmatized_output =' '.join([lemmatizer.lemmatize(w) for w in word_list])
    x = lemmatized_output.replace(' .', ". ")
    sentences = sent_tokenize(x)
    return x


def para2seq():
    # change file name for each person then merge after
    f = open("test.txt", "r")
    data = f.read()
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    index = 0
    for sentence in sentences:
        incorrect_sentence = make_sentence_incorrect(sentence)
        if not incorrect_sentence:
            # print('---skip-----')
            skip_sentence.append(sentence)
            continue
        # correct_sentence_file.write(incorrect_sentence + '|')
        # correct_sentence_file.write(sentence + '\n')
        correct_sentence_file.write(incorrect_sentence + '|')
        correct_sentence_file.write(sentence + '\n')
        index += 1
    print(index)
    print(len(skip_sentence))
    
