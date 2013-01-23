import re
printTest = False
def find_basic_information(html, url, get_title, get_body, get_date):
    title = get_title(html, url)
    date = get_date(html, url)
    body = get_body(html, url)
    if not (title and date and body):
        return False
    if printTest:
        print '\n\n\n\n\n\n'
        print url
        print 'Title is: ',
        print title
        print 'Date is: ',
        print date, '\n'
        print 'Body is: ***********************',
        print body
        print '\n\n *********************************\n\n\n'
    return {'title' : title, 'body' : body, 'date' : date}

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
