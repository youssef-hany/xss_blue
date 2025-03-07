from urllib.request import urlopen
from urllib import parse
from tag_finder import TagFinder
from base_functions import *
from domain import *


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    form_links_file = ''
    queue = set()
    crawled = set()
    form_links = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.form_links_file = Spider.project_name + '/form_links.txt'
        self.boot()
        self.crawl_page('Master Spider', Spider.base_url)

    # static methods to prevent warning for static class python coding convention idk xD
    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.form_links = file_to_set(Spider.form_links_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled: # using crawled set for faster operation rather than file
            #print(thread_name + ' now crawling ' + page_url)
            print('Queue (' + str(len(Spider.queue)) + ') | Crawled  (' + str(len(Spider.crawled)) + ') | Forms  (' + str(len(Spider.form_links)) + ')')
            Spider.add_links_to_queue(Spider.get_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def get_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_string = response.read().decode("utf-8")
            finder = TagFinder(Spider.base_url, page_url)
            finder.feed(html_string)
            for link in finder.page_form_links():
                Spider.form_links.add(link)
            
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_form_link_to_file(links):
        for url in links:
            set_to_file(links, Spider.form_links_file)


    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(parse.urljoin(Spider.base_url, url))

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        set_to_file(Spider.form_links, Spider.form_links_file)