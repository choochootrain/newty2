import re
import HTMLParser
import traceback
from datetime import datetime
#from useful_functions import *
h = HTMLParser.HTMLParser()
def get_title(html, url):
    title_begin = html.find('<title>')
    title_end = html[title_begin :].find('</title>')
    if title_begin == -1 or title_end == -1:
        print 'failed title', url
        return False
    """fix offsets"""
    title_end += title_begin
    title_begin += 7

    title = html[title_begin : title_end]
    #print title
    return title
    
def get_body(html, url):
    a = html.find('<div class="body-copy">')
    html1 = html[a + 23 :]
    html_array = html1.split('</div>')
    if len(html_array) < 2:
        print 'failed', url
        return False
    body = html_array[1]
    'scripts in the body'
    if body.find('<script>') != -1 or body.find('</script>') != -1:
        print 'failed body', url
        return False
    clean_body = remove_tags(body).strip().replace('\n', ' ')
    clean_body = re.sub(r'\s+', ' ', clean_body)
    new_clean_body = h.unescape(clean_body)
    
    #print clean_body
    return new_clean_body

def get_date(html, url):
    length = len('<div class="post-time">')
    date_begin = html.find('<div class="post-time">')
    date_end = html[date_begin:].find('</div>')
    if date_begin == -1 or date_end == -1:
        print 'failed date', url
        return False
    date_end += date_begin
    date_begin += length

    date = html[date_begin : date_end]
    try:
        date_time = date_string_to_obj(date)
    except:
        print 'error date time not parsed'
        traceback.print_exc()
        return False
    #print date_time
    return date_time

number_attached_letters = re.compile('(\d+)([A-Za-z]+)')
def date_string_to_obj(date_string):
    result = date_string
    date_string_array = date_string.split(' ')
    for word in date_string_array:
        match_obj = number_attached_letters.match(word)
        if match_obj:
            result = result.replace(word, match_obj.group(1) + ',')
    date_time = datetime.strptime(result, "%A, %B %d, %Y")
    return date_time



date_match = re.compile('.*20[0-1][0-9]/[0-1][0-9]/[0-3][0-9].*')
def reject(url):
    if 'fr.techcrunch.com' in url or 'jp.techcrunch.com' in url or\
            'eu.techcrunch.com' in url or 'disrupt.techcrunch.com' in url:
        return True
    if url[-9:] == '#comments' or url[-5 :] == 'feed/':
        return True
    if not date_match.match(url):
        return True
    return False
