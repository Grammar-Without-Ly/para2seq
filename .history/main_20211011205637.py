from nltk.tokenize import sent_tokenize

def find_word_in_database(word):
    return

def incorrect_sentence(sentence):
    # split sentence to word
    words = sentence.split(' ')
    for word in words:
        if word[0].isupper():
            break
        #find word in database
        is_word_in_dictionry = find_word_in_database(word)
        break
    return

def main():
    # change file name for each person then merge after
    f = open("rawData.quang.txt", "r")
    data = f.read()
    formatted_data_file = open("formattedData.quang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    # print(sentences)
    for correct_sentence in sentences:
        # write correct sentence to file
        formatted_data_file.write(correct_sentence + '\n')
        # ghi 1 cau sai
        incorrect_sentence_formatted = incorrect_sentence(correct_sentence)
        # print(correct_sentence)
        

# cc

main()
