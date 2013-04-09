import json
import sys
import os
import re
_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))



def title_remover(func):
    f = open('clean_title_word_counts.json', 'r')
    to_write=open('clean_title_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)
        if func(line_arr):
            continue
        to_write.write(line)
    f.close()
    to_write.close()
    os.system('mv clean_title_word_counts.json.tmp clean_title_word_counts.json')


def body_remover(func):
    f = open('clean_body_word_counts.json', 'r')
    to_write=open('clean_body_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)
        if func(line_arr):
            continue
        to_write.write(line)
    f.close()
    to_write.close()
    os.system('mv clean_body_word_counts.json.tmp clean_body_word_counts.json')




'''removes words that don't appear many times based on total count'''
if '1' in sys.argv[1]:
    def remove_total_count_body(line_arr):
        return line_arr[1][0] <= 50
    def remove_total_count_title(line_arr):
        return line_arr[1][0] <= 2
    title_remover(remove_total_count_title)
    body_remover(remove_total_count_body)

'''removes more words that don't appear many times based on freq3'''
if '2' in sys.argv[1]:
    def remove_freq3_count_body(line_arr):
        return line_arr[1][1] <= 10

    body_remover(remove_freq3_count_body)

'''removes words with digits'''
if '3' in sys.argv[1]:
    def remove_digits(line_arr):
        return contains_digits(line_arr[0])
    title_remover(remove_digits)
    body_remover(remove_digits)



'''removes stop words'''
if '4' in sys.argv[1]:
    stop_words = json.loads(open('stop_words.json', 'r').read())

    def remove_stop_words(line_arr):
        return line_arr[0] in stop_words
    title_remover(remove_stop_words)
    body_remover(remove_stop_words)

if '5' in sys.argv[1]:
    print 'reached'
