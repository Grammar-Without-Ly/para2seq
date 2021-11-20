import csv
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


def ProperNounExtractor(correct_structure):
    sentences = nltk.sent_tokenize(correct_structure)
    text = ""
    for sentence in sentences:
        s = sentence
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word not in set(stopwords.words('english'))]
        tagged = nltk.pos_tag(words)
        for (word, tag) in tagged:
            if tag == 'NNP':  # If the word is a proper noun
                s = s.replace(str(word),str(word).lower())
        text += s
    return text
def para2seq():
    # change file name for each person then merge after
    f = open("rawData.trung.txt", "r")
    data = f.read()
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    # print(sentences)
    correct_sentence_file = open("test.csv", "a")
    for correct_structure in sentences:
        incorrect_ProperNoun_formatted = ProperNounExtractor(correct_structure)
        if correct_structure != incorrect_ProperNoun_formatted:
            correct_sentence_file.write(incorrect_ProperNoun_formatted + '|' + correct_structure + '\n')
        else:
            print('No change : ' + correct_structure + incorrect_ProperNoun_formatted)
para2seq()


