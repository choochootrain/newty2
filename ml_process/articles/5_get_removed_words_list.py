import json


clean_words = open('clean_body_word_counts.json', 'r')
all_words = open('body_word_counts.json', 'r')


clean_words_set = set()
removed_words_list = []
for line in clean_words:
    clean_words_set.add(json.loads(line)[0])

for line in all_words:
    if json.loads(line)[0] not in clean_words_set:
        removed_words_list.append(json.loads(line)[0])


clean_words.close()
all_words.close()


removed_words = open('removed_words.json', 'w')
removed_words.write(json.dumps(removed_words_list))
removed_words.close()
