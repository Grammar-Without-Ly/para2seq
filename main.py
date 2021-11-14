import csv
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

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
    # print(sentences)
    correct_sentence_file = open("test.csv", "a")
    for correct_structure in sentences:
        incorrect_structure_formatted = change_structure(correct_structure)
        if correct_structure != incorrect_structure_formatted:
            correct_sentence_file.write(incorrect_structure_formatted + '|')
            correct_sentence_file.write(correct_structure +'\n')
        else:
            print('No change' + correct_structure + incorrect_structure_formatted )

# def para2seq():
#     # change file name for each person then merge after
#     f = open("rawData.trung.txt", "r")
#     data = f.read()
#     # split paragraph to sentence
#     sentences = sent_tokenize(data)
#     # print(sentences)
#     correct_sentence_file = open("test.txt", "a")
#     for correct_structure in sentences:
#         incorrect_structure_formatted = change_structure(correct_structure)
#         correct_sentence_file.write(incorrect_structure_formatted + '\t')
#         correct_sentence_file.write(correct_structure + '\n')



para2seq()


