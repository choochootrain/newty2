from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
from scrapy.utils.markup import remove_tags, remove_tags_with_content, replace_escape_chars

import string
import sqlite3
from os import path

class DataCleanPipeline(object):
  def __init__(self):
    self.urls_seen = set()

  def process_item(self, item, spider):
    if item['title'] and item['author'] and item['date'] and item['text'] and item['link']:
      if not item['link'] in self.urls_seen:
        item['text'] = remove_tags(remove_tags_with_content(replace_escape_chars(filter(lambda x: x in string.printable, item['text'][25:])), which_ones=('div', 'img', 'script')))
        item['title'] = filter(lambda x: x in string.printable, item['title'])
        self.urls_seen.add(item['link'])
        return item
      else:
        raise DropItem('Duplicate item %s' % item)
    else:
      raise DropItem('Missing fields %s' % item)

class SqlitePipeline(object):
  filename = '/media/flash/techcrunch/items.db'

  def __init__(self):
    self.conn = None
    dispatcher.connect(self.initialize, signals.engine_started)
    dispatcher.connect(self.finalize, signals.engine_stopped)

  def process_item(self, item, spider):
    try:
      self.conn.execute('insert into items values(?,?,?,?,?)',
          (item['link'], item['title'], item['author'], item['date'], item['text']))
    except:
      print 'Failed to insert item: ' + item['link']
      return item

  def initialize(self):
    if path.exists(self.filename):
      self.conn = sqlite3.connect(self.filename)
    else:
      self.conn = self.create_table(self.filename)

  def finalize(self):
    if self.conn is not None:
      self.conn.commit()
      self.conn.close()
      self.conn = None

  def create_table(self, filename):
    conn = sqlite3.connect(filename)
    conn.execute("""create table items
      (link text primary key, title text, author text, date text, body text)""")
    conn.commit()
    return conn
