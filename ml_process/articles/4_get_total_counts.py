import json
f = open('clean_body_word_counts.json', 'r')
total = 0
freq3 = 0
freq5 = 0
freq10 = 0
freq15 = 0
freq25 = 0
for line in f:
    line_arr = json.loads(line)
    total += line_arr[1][0]
    freq3 += line_arr[1][1]
    freq5 += line_arr[1][2]
    freq10 += line_arr[1][3]
    freq15 += line_arr[1][4]
    freq25 += line_arr[1][5]
f.close()
total_word_counts = open('total_body_word_counts.json', 'a')
total_word_counts.write(json.dumps({'total' : total, 'freq3' : freq3, 'freq5' : freq5, 'freq10' : freq10, 'freq15' : freq15, 'freq25' : freq25}))
total_word_counts.close()
