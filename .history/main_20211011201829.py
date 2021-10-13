from nltk.tokenize import sent_tokenize


def main():
    # change file name for each person then merge after
    f = open("rawData.quang.txt", "r")
    data = f.read()
    correct_sentence_file = open("correctSentence.quang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    for sentence in sentences:
        print(sentence)
        correct_sentence_file.write(sentence + '\n')

# cc

main()
