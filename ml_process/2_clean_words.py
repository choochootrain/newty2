import json
import sys
import os
import re
_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

if '1' in sys.argv[1]:
    f = open('body_word_counts.json', 'r')
    to_write = open('clean_body_word_counts.json', 'w')
    for line in f:
        line_arr = json.loads(line)
        if line_arr[1][0] > 5:
            to_write.write(line)
    f.close()
    to_write.close()

    f = open('title_word_counts.json', 'r')
    to_write = open('clean_title_word_counts.json', 'w')
    for line in f:
        line_arr = json.loads(line)
        if line_arr[1][0] > 2:
            to_write.write(line)
    f.close()
    to_write.close()


if '2' in sys.argv[1]:
    f = open('clean_body_word_counts.json', 'r')
    to_write=open('clean_body_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)
        if line_arr[1][1] > 5:
            to_write.write(line)
        else:
            print line_arr[0]

    f.close()
    to_write.close()
    os.system('mv clean_body_word_counts.json.tmp clean_body_word_counts.json')


if '3' in sys.argv[1]:
    f = open('clean_body_word_counts.json', 'r')
    for line in f:
        line_arr = json.loads(line)
        if line_arr[1][0] > 750000:
            print line_arr[0]


    f.close()
    f = open('clean_title_word_counts.json', 'r')
    for line in f:
        line_arr = json.loads(line)

    f.close()

if '4' in sys.argv[1]:
    f = open('clean_body_word_counts.json', 'r')
    to_write=open('clean_body_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)
        if contains_digits(line_arr[0]):
           print line_arr[0]
        else:
            to_write.write(line)
    f.close()
    to_write.close()
    f = open('clean_title_word_counts.json', 'r')
    to_write=open('clean_title_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)
        if contains_digits(line_arr[0]):
           print line_arr[0]
        else:
            to_write.write(line)
    f.close()
    to_write.close()
    os.system('mv clean_body_word_counts.json.tmp clean_body_word_counts.json')
    os.system('mv clean_title_word_counts.json.tmp clean_title_word_counts.json')


if '5' in sys.argv[1]:
    f = open('clean_body_word_counts.json', 'r')
    to_write=open('clean_body_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)

    f.close()
    to_write.close()
    f = open('clean_title_word_counts.json', 'r')
    to_write=open('clean_title_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)

    f.close()
    to_write.close()
    os.system('mv clean_body_word_counts.json.tmp clean_body_word_counts.json')
    os.system('mv clean_title_word_counts.json.tmp clean_title_word_counts.json')

if '6' in sys.argv[1]:
    f = open('clean_body_word_counts.json', 'r')
    to_write=open('clean_body_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)

    f.close()
    to_write.close()
    f = open('clean_title_word_counts.json', 'r')
    to_write=open('clean_title_word_counts.json.tmp', 'w')
    for line in f:
        line_arr = json.loads(line)

    f.close()
    to_write.close()
    os.system('mv clean_body_word_counts.json.tmp clean_body_word_counts.json')
    os.system('mv clean_title_word_counts.json.tmp clean_title_word_counts.json')
