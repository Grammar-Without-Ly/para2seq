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
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
    # sentences = sent_tokenize(lemmatized_output)
    print(lemmatized_output)
    return lemmatized_output


def para2seq():
    # change file name for each person then merge after
    f = open("rawData.trung.txt", "r")
    data = f.read()
    correct_sentence_file = open("Correctsentence.trung.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    # print(sentences)
    for correct_structure in sentences:
         correct_sentence_file.write(correct_structure +'\n')
         incorrect_structure_formatted = change_structure(correct_structure)

         correct_sentence_file.write(incorrect_structure_formatted + '\n')

para2seq()



# def main():
#     # change file name for each person then merge after
#     f = open("rawData.trung.txt", "r")
#     data = f.read()
#     formatted_data_file = open("Correctsentence.trung.txt", "a")
#     # split paragraph to sentence
#     sentences = sent_tokenize(data)
#     # print(sentences)
#     for correct_sentence in sentences:
#         # write correct sentence to file
#         formatted_data_file.write(correct_sentence + '\n')
#         # ghi 1 cau sai
#         incorrect_sentence_formatted = incorrect_sentence(correct_sentence)
#         formatted_data_file.write(incorrect_sentence_formatted + '\n')
#         # print(correct_sentence)
#
#
# # cc
#
# main()

