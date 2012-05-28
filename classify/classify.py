import re
import codecs
import math
def percent_match(html, keywords):
    html_array = html.split(' ')
    total_length = len(html_array)
    num_matches = 0
    for keyword in keywords:
        num_matches += num_match(html, keyword)
    return num_matches / float(total_length)


def num_match(html, keyword):
    return len(re.findall(keyword, html))



"""gets mean occurence and standard deviation of an occurence of each keyword in keywords"""
"""returns {keyword1 : [mean, std_dev], keyword2 : [mean, std_dev]}"""
"""file_paths are the list of file_paths we are training on"""
def get_stats(file_paths, keywords):
    keywords_upper = []
    for x in keywords:
        keywords_upper.append(x.upper())
    keywords = keywords_upper

    result = {}
    """freq_table -> {keyword : [freq_file_1, freq_file2]}"""
    freq_table = {}
    for x in keywords:
        freq_table[x] = []
    for file in file_paths:
        f = codecs.open(file, 'r', 'iso-8859-1')
        html = ' ' + f.read().upper() + ' '
        for keyword in keywords:
            keyword_freq = html.count(' ' + keyword + ' ')
            freq_table[keyword].append(keyword_freq)

    for k, v in freq_table.items():
        mean = sum(v)/len(v)
        std_dev = math.sqrt(sum([(x - mean) ** 2 for x in v])/len(v))
        result[k] = (mean, std_dev)
    return result
    
        
    
