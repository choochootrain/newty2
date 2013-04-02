import json
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
