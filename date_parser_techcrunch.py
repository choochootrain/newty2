from datetime import datetime
import re


number_attached_letters = re.compile('(\d+)([A-Za-z]+)')
def remove_attached_letters(a_string):
    result = a_string
    a_string_array = a_string.split(' ')
    for i, word in enumerate(a_string_array):
        match_obj = number_attached_letters.match(word)
        if match_obj:
            result = result.replace(word, match_obj.group(1) + ',')
    return result
while True:
    user_input = raw_input('Input a date time field\n')
    user_input = remove_attached_letters(user_input)
    date_time = datetime.strptime(user_input, "%A, %B %d, %Y")
    print date_time
