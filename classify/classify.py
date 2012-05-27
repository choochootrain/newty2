import re


def percent_match(html, keywords):
    html_array = html.split(' ')
    total_length = len(html_array)
    num_matches = 0
    for keyword in keywords:
        num_matches += len(re.findall(keyword, html))
    return num_matches / float(total_length)


