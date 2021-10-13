import random
from nltk.tokenize import sent_tokenize
import sqlite3


def remove_space_between_words(sentence):
    return sentence


def insert_random_charater(word):
    return word


def con_db():
    con = sqlite3.connect('Dictionary.db')
    return con.cursor()


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
        characters[position + 1] = temp
        print(array_to_word(characters))
    return array_to_word(characters)


def find_word_in_database(word):
    sql = """SELECT * FROM entries WHERE  lower("word") = '%s'""" % word
    word_list = dictionary_db.execute(sql)
    return word_list.fetchall()


def random_number(data):
    return random.randint(0, len(data) - 1)


def incorrect_sentence(sentence):
    # split sentence to word
    words = sentence.split(' ')
    is_satisfy = False
    while not is_satisfy:

        # no need to check all words in sentence
        random_index_word = random_number(words)
        word = words[random_index_word]
        print(word)

        # special noun
        if word.isupper() and random_index_word != 0:
            continue

        word = word.lower()
        is_word_in_dictionary = find_word_in_database(word)
        if is_word_in_dictionary:
            random_case = 1
            if random_case:
                words[random_index_word] = swap_character(word)
            else:
                print('toschool')
            is_satisfy = True
        print(words)
    return array_to_sentence(words)


dictionary_db = con_db()


def main():
    print('alo')
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


main()
