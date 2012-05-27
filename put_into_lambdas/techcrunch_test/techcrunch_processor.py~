from process_template import ProcessTemplate
import sys
from multiprocessing import Pool
news_name = 'techcrunch_data'


class TechcrunchProcessor(ProcessTemplate):
    @classmethod
    def map_files(cls):
        for x in cls.file_queue:
            cls.sort_information(x)
    #pool = Pool(processes=5)
        #pool.map(cls.function_on_file, queue_list)
    


    @classmethod
    def get_title(cls, html):
        print 'get title not yet implemented'
    @classmethod
    def get_body(cls, html):
        print 'get body not yet implemented'
        a = html.find('<div class="body-copy">')
        html1 = html[a + 23 :]
        html_array = html1.split('</div>')
        body = html_array[0]
        clean_body = cls.remove_tags(body)
        print clean_body
    @classmethod
    def get_date(cls, html):
        print 'get date not yet implemented'
    
    
if __name__ == '__main__':
    main_dir = sys.argv[1]
    test = TechcrunchProcessor(main_dir, news_name)
    test.map_files()
