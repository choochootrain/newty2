import re
import HTMLParser
import traceback
from datetime import datetime
from useful_functions import *
import urllib2
h = HTMLParser.HTMLParser()


def get_title(html, url):
    title_begin = html.find('<title>')
    title_end = html[title_begin :].find('</title>')
    if title_begin == -1 or title_end == -1:
        print 'failure title', url
        return False
    """fix offsets"""
    title_end += title_begin
    title_begin += 7

    title = html[title_begin : title_end]
    return title



def get_body(html, url):
    body1 = get_body1(html, url)
    if body1:
        return body1
    body2 = get_body2(html, url)
    if body2:
        return body2
    print 'failure body', url
    return False

begin_matcher = re.compile('<p itemprop="articleBody">')
def get_body1(html, url):
    div_article_body = html.find('<div class="articleBody">')
    first_p = html[div_article_body:].find('<p itemprop="articleBody">') + len('<p itemprop="articleBody">') + div_article_body
    last_p = html.rfind('<p itemprop="articleBody">')
    end = html[last_p : ].find('</p>') + last_p
    body = html[first_p : end]
    '''scripts in the body'''
    if body.find('<script>') != -1 or body.find('</script>') != -1:
        return False
    clean_body = remove_tags(body).strip().replace('\n', ' ')
    clean_body = re.sub(r'\s+', ' ', clean_body)
    clean_body = h.unescape(clean_body)
    return clean_body

def get_body2(html, url):
    start_body = html.find('<div class="entry-content">') + len('<div class="entry-content">')
    end_body = html.find('<div class="entry-meta">')
    if start_body  == -1 or end_body  == -1:
        return False
    body =  html[start_body : end_body]
    clean_body = remove_tags(body).strip().replace('\n', ' ')
    clean_body = re.sub(r'\s+', ' ', clean_body)
    clean_body = h.unescape(clean_body)
    return clean_body


def get_date(html, url):
    date1 = get_date1(html, url)
    if date1:
        return date1
    date2 = get_date2(html, url)
    if date2:
        return date2
    date3 = get_date3(html, url)
    if date3:
        return date3
    print 'failure date' , url
    return False

def get_date1(html, url):
    date_begin = html.find('<meta name="ptime" content="') + len('<meta name="ptime" content="')
    date_end = html[date_begin : ].find('"') + date_begin
    return html[date_begin : date_end].strip()

def get_date2(html, url):
    length = len('<meta itemprop="datePublished" content="')
    date_begin = html.find('<meta itemprop="datePublished" content="')
    date_end = html[date_begin:].find('">')
    if date_begin == -1 or date_end == -1:
        return False
    date_end += date_begin
    date_begin += length
    date = html[date_begin : date_end]
    return date

def get_date3(html, url):
    start_looking = html.find('<time datetime=')
    date_begin = html[start_looking :].find('>') + len('>') + start_looking
    date_end = html[date_begin:].find('</time>') + date_begin
    if date_begin == -1 or date_end == -1:
        return False
    return html[date_begin : date_end]

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
