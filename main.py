import random
from nltk.tokenize import sent_tokenize
import sqlite3


def remove_space_between_words(sentence):
    return sentence


def insert_random_charater(word):
    return word

def connDb():
    con = sqlite3.connect('Dictionary.db')
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM entries "):
        z = row[0]
        print(z)

# house
# position = 3
# swap_type = 1
# hosue

def array_to_sentence(word_array):
    return ' '.join(word_array)


def array_to_word(word_array):
    return ''.join(word_array)


def split_word_to_char(word):
    return [char for char in word]


def swap_character(word):
    position = random.randint(0, len(word) - 1)
    swap_type = random.randint(0, 1)
    characters = split_word_to_char(word)
    if swap_type:
        temp = characters[position]
        characters[position] = characters[position + 1]
        characters[position + 1]
        print(array_to_word(characters))
    return array_to_word(characters)


def find_word_in_database(word):
    return word


def incorrect_sentence(sentence):
    # split sentence to word
    words = sentence.split(' ')
    i = 0
    for word in words:
        if word[0].isupper() and i:
            i += i
            break
        # find word in database
        # is_word_in_dictionary = find_word_in_database(word)
        is_word_in_dictionary = True
        if is_word_in_dictionary:
            # random_case = random.randint(0, 1)
            random_case = 1
            if random_case:
                # print(random_case)
                word = swap_character(word)
                # print(word)
            break
        else:
            # toschool
            break
    # print(words)
    return array_to_sentence(words)


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
        formatted_data_file.write(incorrect_sentence_formatted + '\n')
        # print(correct_sentence)


# main()
connDb()
