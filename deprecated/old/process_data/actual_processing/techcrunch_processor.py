import re


news_name = 'techcrunch_data'

"""@toedit"""
def get_title(html):
    print 'get title not yet implemented'



"""@toedit"""
def get_body(html):
    print 'get body not yet implemented'
    a = html.find('<div class="body-copy">')
    html1 = html[a + 23 :]
    html_array = html1.split('</div>')
    body = html_array[0]
    clean_body = remove_tags(body)
    print clean_body


"""@toedit"""
def get_date(html):
    print 'get date not yet implemented'
    



begin_tags = r'<(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'
end_tags = r'</(div|td|tr|th|table|a|body|area|form|font|h1|h2|h3|h4|h5|h6|head|title|li|p|center|html|input|option|select|textarea|ul|i|b|label|footer|span)(>|[\s][^>^<^]*>)'

tags_regex = '<[^<^>]*>'


def remove_tags(html):
    tags = [(x.start(), x.end()) for x in re.finditer(tags_regex, html)]
    clean_html = ''
    prev_end = 0
    for begin, end in tags:
        clean_html += html[prev_end : begin]
        prev_end = end
    clean_html += html[prev_end : ]
    return clean_html
