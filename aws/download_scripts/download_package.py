'''Contains the functions that are shared by both get_html.py and force_get_html.py'''
import re
import urllib2
import os


"""Handles opening sites that force you to redirect. """
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302


'''Variables'''
delete_last_slash = re.compile('(.*)/')
directory_regex = re.compile('(.*)/[^/]+')
directories_exist = set()
"""Url Parser : use as page = url_opener.open(url)"""
cookie_handler = urllib2.HTTPCookieProcessor()
url_opener = urllib2.build_opener(MyHTTPRedirectHandler, cookie_handler)
url_opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5')]




def download_and_write_page(url, file_parent_path):
    page = url_opener.open(url)
    html = page.read()
    url_no_http = url.replace('http://', '')
    account_for_last_slash = delete_last_slash.search(url_no_http)
    if account_for_last_slash and account_for_last_slash.group(0) == url_no_http:
        url_no_http = account_for_last_slash.group(1)
    ensure_path(file_parent_path + url_no_http)
    f = open(file_parent_path + url_no_http + '_file', 'w')
    f.write(html)
    f.close()
    return html
    

'''If the path for the url exists, do nothing. If path does not exist, creates the path'''
def ensure_path(url_no_http):
    if '/' not in url_no_http:
        return
    path = directory_regex.search(url_no_http).group(1)
    if path in directories_exist:
        return
    if not os.path.exists(path):
        os.makedirs(path)
        directories_exist.add(path)



def to_bytestring (s, enc='utf-8'):
    """Convert the given unicode string to a bytestring, using the standard encoding,                                                                                                                     
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)





whitespace_regex = re.compile('\s*')
def parse_file_by_line(file_name):
    to_return = []
    try:
        f = open(file_name, 'r')
        to_return = [line.strip() for line in f if line.strip() != '']
        print 'closed'
        f.close()
    except IOError as e:
        ensure_path(file_name)
        f = open(file_name, 'w')
        f.close()
    return to_return

