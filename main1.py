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
lemmatizer = WordNetLemmatizer()
f = open("rawData.trung.txt", "r")
data = f.read()
word_list=[lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(data)]
lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
correct_sentence_file = open("Correctsentence.trung.txt", "a")
sentences = sent_tokenize(lemmatized_output)
for word in sentences:
    # x = word.split()
    # correct_sentence_file.write(word + '\n')
    # print(word)
    print(sentences)