from nltk.tokenize import sent_tokenize

def incorrect_sentence(sentence):
    return

def main():
    # change file name for each person then merge after
    f = open("rawData.quang.txt", "r")
    data = f.read()
    correct_sentence_file = open("correctSentence.quang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    for correct_sentence in sentences:
        # ghi 1 cau dung
        correct_sentence_file.write(correct_sentence + '\n')
        # ghi 1 cau sai
        incorrect_sentence_formatted = incorrect_sentence(correct_sentence)
        print(correct_sentence)
        

# cc

main()
