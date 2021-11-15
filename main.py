from nltk.tokenize import sent_tokenize, word_tokenize
import sqlite3
from string import ascii_letters
import random


def con_db():
    con = sqlite3.connect('Dictionary.db')
    return con.cursor()


dictionary_db = con_db()


def remove_space_between_words(words):
    return words[0] + words[1]


def get_random_character():
    return random.choice('abcdefghiklmnopqrstuvwxyz')


def insert_random_character(word):
    random_character = get_random_character()
    random_character_index = random.randint(0, len(word) - 1)
    return word[:random_character_index] + random_character + word[random_character_index:]


#
# # house
# # position = 3
# # swap_type = 1
# # hosue
#
#
def array_to_sentence(word_array):
    result = ''
    index = 0
    for word in word_array:
        index += 1
        if set(word).difference(ascii_letters):
            result += word
        else:
            if index:
                result += ' ' + word
            else:
                result += word
    return result


def array_to_word(word_array):
    return ''.join(word_array)


def split_word_to_char(word):
    return [char for char in word]


def swap_character(word):
    try:
        position = random.randint(0, len(word) - 2)
        swap_type = random.randint(0, 1)
        characters = split_word_to_char(word)
        if swap_type:
            temp = characters[position]
            try:
                characters[position] = characters[position + 1]
                characters[position + 1] = temp
            except Exception as e:
                print(word)
        return array_to_word(characters)
    except Exception as e:
        print(word)


def find_word_in_database(word):
    try:
        sql = """SELECT * FROM entries WHERE  lower("word") = '%s'""" % word
        word_list = dictionary_db.execute(sql)
        return word_list.fetchall()
    except Exception as e:
        print(e)
        return


def random_number(data):
    return random.randint(0, len(data) - 1)


log_case = {
    '0': 0,
    '1': 0,
    '2': 0
}


def incorrect_sentence(sentence):
    # split sentence to word
    words = word_tokenize(sentence)
    is_satisfy = False
    try_time = 0
    while not is_satisfy:
        if try_time > 5:
            print('---skip---')
            return None
        try_time += 1
        # no need to check all words in sentence
        random_index_word = random_number(words)
        word = words[random_index_word]

        # special noun
        if word.isupper() and random_index_word != 0:
            continue

        word = word.lower()
        if len(word) < 4:
            continue
        is_word_in_dictionary = find_word_in_database(word)
        if is_word_in_dictionary:
            random_case = random.randint(0, 2)
            log_case[str(random_case)] = log_case[str(random_case)] + 1
            if random_case == 0:
                modify_word = swap_character(word)
                if modify_word:
                    # words[random_index_word] = modify_word
                    sentence = sentence.replace(word, modify_word)
                    print(word + '------->' + modify_word)
                else:
                    print(sentence)
                    continue
            elif random_case == 1:
                modify_word = insert_random_character(word)
                if modify_word:
                    # words[random_index_word] = modify_word
                    sentence = sentence.replace(word, modify_word)
                    print(word + '------->' + modify_word)
                else:
                    print(sentence)
                    continue
            else:
                modify_word = remove_space_between_words([words[random_index_word - 1], word])
                if modify_word:
                    # words[random_index_word] = modify_word
                    # del words[random_index_word - 1]
                    sentence = sentence.replace(words[random_index_word - 1] + ' ' + word, modify_word)
                    print(words[random_index_word - 1] + ' ' + word + '------->' + modify_word)
                else:
                    print(sentence)
                    continue
            is_satisfy = True
    return sentence


def main():
    # change file name for each person then merge after
    f = open("rawData.quang.txt", "r")
    data = f.read()
    formatted_data_file = open("formattedData.quang.txt", "a")
    # split paragraph to sentence
    sentences = sent_tokenize(data)
    print(len(sentences))
    a = 0
    for correct_sentence in sentences:
        a += 1
        print(a)
        incorrect_sentence_formatted = incorrect_sentence(correct_sentence)
        if incorrect_sentence_formatted:
            correct_sentence = correct_sentence.replace("\n", " ")
            formatted_data_file.write(incorrect_sentence_formatted + '|' + correct_sentence + '\n')
    print(log_case)


main()
