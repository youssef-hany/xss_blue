import threading
from queue import Queue
from spider import Spider
from domain import *
from base_functions import *

def SpiderMain():
    print("[-] Welcome to spider please fill out options")
    SITE_URL = input("[-] please provide url:$ ")
    PROJECT_NAME = SITE_URL.replace('www', '').split('.')[-2].replace('http://', '').replace('https://', '').replace('/', '')
    DOMAIN_NAME = get_domain_name(SITE_URL)
    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
    NUMBER_OF_THREADS = 8
    queue = Queue()
    #init Master Spider
    Spider(PROJECT_NAME, SITE_URL, DOMAIN_NAME)

    #Creation of worker threads
    def create_workers():
        for _ in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=work)
            t.daemon = True
            t.start()

    #Do the next job(link) in the queue
    def work():
        while True:
            url = queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            queue.task_done()


    # Each link in queue is a new job
    def create_jobs():
        for link in file_to_set(QUEUE_FILE):
            queue.put(link)
        queue.join()
        crawl()

    # check if there are links in the queue if so crawl in threaded mode
    def crawl():
        queued_links = file_to_set(QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + ' Queued Links')
            create_jobs()

    create_workers()
    crawl()