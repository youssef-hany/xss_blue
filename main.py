import concurrent.futures
from multiprocessing import Process, current_process, cpu_count, Pool
#import threading
import queue
from deepblue import Deep
from base_functions import *
import sys
import os, signal
import colorama
from colorama import Fore, Back, Style
from spidermain import SpiderMain
import readline

readline.set_completer_delims(' \t\n=')
readline.parse_and_bind("tab: complete")
colorama.init()
try:
    os.system("cls")
except:
    os.system("clear")
print(Fore.GREEN + "XSS Detector " + Style.RESET_ALL + "[Deep Blue]  By" + Fore.RED + " - J-Odin -" + Style.RESET_ALL)
print("""
        Welcome to the Deep XSS Vulnerability Scanner """ +
        Fore.GREEN+' (DXVS)\n' + Style.RESET_ALL +
        """
        Please choose a fuzzing option for the cross-site scripter:-
            1) GET
            2) POST
            3) Load from file (Automized Tester)
            4) Spider (Recommended before Automated XSS)
		""")
CHOICE = input("[-] DXVS> ")
NUMBER_OF_THREADS = 0
SITE= ''
q = queue.Queue()
TFile = ''
tested_linkL = set()
processes = []
results = []
link_list = []
#Do the next job(link) in the queue
def work(page_url):
        SITE = page_url
        MODE = 'hl'
        PROJECT_NAME = SITE.replace('www', '').split('.')[-2].replace('http://', '').replace('https://', '').replace('/', '')
        print(f"[-] [{current_process().name}] Starting Job with PID [{os.getpid()}]")   
        Deep(CHOICE, SITE, MODE, PROJECT_NAME, TFILE, current_process().name)
        results.append((SITE,  Deep.Print_Results()))

#Creation of worker threads


def create_workers():
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     future_to_url = {
    #     executor.submit(getFormLinks): 'FEEDER DONE'}

    #     while future_to_url:
    #         # check for status of the futures which are currently working
    #         done, not_done = concurrent.futures.wait(
    #         future_to_url, return_when=concurrent.futures.FIRST_COMPLETED)

    # #     # if there is incoming work, start a new future
    #         while not q.empty():
    #     #         # fetch a url from the queue
    #             link = q.get()
    #             if link not in tested_linkL:
    #         #         # Start the load operation and mark the future with its URL
    #                 future_to_url[executor.submit(work, link)] = link
    #                 tested_linkL.append(link)

    #         for future in done:
    #             url = future_to_url[future]
    #             try:
    #                 data = future.result()
    #             except Exception as exc:
    #                 pass
    #                 #print('%r generated an exception: %s' % (url, exc))
    #             else:
    #                 pass
    #                 if url == 'FEEDER DONE':
    #                     pass
    #                     print(data)
    #                 else:
    #                     pass
    #                     #print('%r page is %d bytes' % (url, len(data)))

    # #     #         # remove the now completed future
    #             del future_to_url[future]
        
    #    while not q.empty():
    #         link = q.get()
    #         if link and link not in tested_linkL:
    #             tested_linkL.add(link)   
    #             executor.submit(work, link)    
            #ANOTHER THREADING MECH
        while not q.empty():
            link = q.get()
            if link and link not in tested_linkL:
                tested_linkL.add(link)
                if __name__ == "__main__":
                    process = Process(target=work,args=(link,))
                    process.daemon = True
                    processes.append(process)
                    process.start()
        # with Pool(NUMBER_OF_THREADS) as p:
        #     if __name__ == "__main__":
        #         p.map(work, link_list)



def get_cpu_cap():
    count = cpu_count()
    if int(count) > 0:
        print(Fore.GREEN + f"[-]Found {count} CPU Cores!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "[-] You have no Cores the program can thread on" + Style.RESET_ALL)
        sys.exit(0)
    return(count)

def check_kill_process(pstring):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.kill(int(pid), signal.SIGKILL)

def terminate_workers():
    for worker in processes:
        worker.terminate()

# Each link in queue is a new job
def getFormLinks():
    QUEUE_FILE = PROJECT_NAME + '/form_links.txt'
    TESTED_FILE = PROJECT_NAME + '/form_links_tested.txt'
    queued_links = file_to_set(QUEUE_FILE)
    tested_links = file_to_set(TESTED_FILE)
    if len(queued_links) > 0:
        print(Fore.BLUE + f'[-] Can Fuzz {NUMBER_OF_THREADS} Links Concurrently..' + Style.RESET_ALL)
        print('[-] ' + str(len(queued_links)) + ' Queued links To Fuzz')
        
        
        
        for link in queued_links:
            if link not in tested_links:             
                try:
                    q.put(link)  
                    link_list.append(link)
                    # with concurrent.futures.ProcessPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
                    #     executor.submit(work, link)   
                except Exception as e:
                    print(e)
                    continue

#GET_FUNCTION
if CHOICE.lower() == "1":
    SITE = input("[-] Enter URL with parameters (Ex. http://example.com/xss.php?parameter=): ")
    WFILE = input ("[-] Payload list for fuzzing (Ex. wordlist.txt): ")
    PROJECT_NAME = SITE.replace('www', '').split('.')[-2].replace('http://', '').replace('https://', '').replace('/', '')
    MODE = ''
    Deep(CHOICE, SITE, MODE, PROJECT_NAME, WFILE)

#POST_FUNCTION
elif CHOICE.lower() == '2':
    SITE = input("[-] URL for website (Ex. http://example.com/post.php): ")
    WFILE = input ("[-] Payload list for fuzzing (Ex. wordlist.txt): ")
    PROJECT_NAME = SITE.replace('www', '').split('.')[-2].replace('http://', '').replace('https://', '').replace('/', '')
    MODE = input("[-] Do you wand a Head/Headless launch?[H/HL] Default:[HL]: ")
    Deep(CHOICE, SITE, MODE, PROJECT_NAME, WFILE)

#AUTOMATIC FUZZING
elif CHOICE.lower() == "3":
    result = []
    TFILE = input ("[-] Payload list for all Threads to use (Ex. wordlist.txt): ")
    PROJECT_NAME = input ("[-] Provide project name directory given by crawler (Ex. testwebsite): ")
    MODE = 'hl'
    NUMBER_OF_THREADS = get_cpu_cap()
    getFormLinks()
    create_workers()
    while len(processes):
        for worker in processes:
            
            if not worker.is_alive():
                print(Style.RESET_ALL + f"[-] [{worker.name}] was TERMINATED!")
                #result.append((SITE,  Deep.Print_Results()))
                processes.remove(worker)
                worker.terminate()  
                
                print(f"[-] Workers Remaining --> {len(processes)}")
                if len(result) and (len(processes) == 0):
                    res = dict(result)
                    print(result)
                    print(res)
                    check_kill_process("firefox-esr")#killing processes to ensure that they are not run in bg
                    check_kill_process("geckodriver")#because seleniumDriver.quit() doesnt always close it idk why
                break
       


#SPIDER
elif CHOICE.lower() == "4":
    # TFILE = input ("[-] Payload list for all Threads to use (Ex. wordlist.txt): ")
    # PROJECT_NAME = input ("[-] Provide project name directory given by crawler (Ex. testwebsite): ")
    # MODE = 'hl'
    SpiderMain()
    
else:
    print("[-] Wrong option choose Wisely xD")
    sys.exit(0)


