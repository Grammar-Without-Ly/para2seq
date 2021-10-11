from nltk.tokenize import word_tokenize, sent_tokenize


def para2seq():
    # change file name for each person then merge after
    f = open("rawData.thang.txt", "r")
    data = f.read()
    correct_sentence_file = open("correctSentence.thang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    for word in sentences:
        x = word.split()
        print(x)
    #     correct_sentence_file.write(sentencen')
para2seq()


