import random

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

from string import ascii_letters


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
    word_list = word_tokenize(correct_structure)
    result = correct_structure
    for word in word_list:
        if set(word).difference(ascii_letters):
            continue
        pos_word_net = get_wordnet_pos(word)
        if pos_word_net.lower() == 'v':
            change_word = lemmatizer.lemmatize(word, pos_word_net)
            if change_word != word:
                result = result.replace(word, change_word)
                print(result)
                break
    return result


def para2seq():
    # change file name for each person then merge after
    f = open("test.txt", "r")
    data = f.read()
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    # print(sentences)
    correct_sentence_file = open("test.csv", "w")
    for correct_structure in sentences:
        incorrect_structure_formatted = change_structure(correct_structure)
        if correct_structure != incorrect_structure_formatted:
            correct_sentence_file.write(incorrect_structure_formatted + '|' + correct_structure + '\n')
        else:
            print('No change\t' + correct_structure + '\t' + incorrect_structure_formatted)


# def para2seq():
#     # change file name for each person then merge after
#     f = open("rawData.trung.txt", "r")
#     data = f.read()
#     formatted_data_file = open("Correctsentence.trung.txt", "a")
#     # split paragraph to sentence
#     sentences = sent_tokenize(data)
#     # print(sentences)
#     correct_sentence_file = open("test.txt", "a")
#     for correct_structure in sentences:
#         incorrect_structure_formatted = change_structure(correct_structure)
#         correct_sentence_file.write(incorrect_structure_formatted + '\t')
#         correct_sentence_file.write(correct_structure + '\n')


para2seq()
