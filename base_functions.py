import os
import colorama
from colorama import Fore, Back, Style
colorama.init()

# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name , "queue.txt")
    crawled = os.path.join(project_name,"crawled.txt")
    form_file = os.path.join(project_name,"form_links.txt")
    form_file_tested = os.path.join(project_name,"form_links_tested.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(form_file):
        write_file(form_file, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    if not os.path.isfile(file_name):
        project_name = file_name.split('form_')[0]
        try:
            if not os.path.exists(project_name):
                print(Fore.RED + f"[-BF Error]: Didn't find previous crawled project by the name {project_name}" + Fore.GREEN + " Creating one!" + Style.RESET_ALL)
                os.makedirs(project_name)
            if not os.path.isfile(file_name):
                fileName = "form_" + str(file_name.split("form_")[1]) 
            #write_file(file_name, '')
            print(Fore.GREEN + f"[-BF Error]: Create file {fileName} and fill this file with your probable targets or just run the spider on the website!" + Style.RESET_ALL)
        except Exception as e:
            print(e)
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    if not os.path.isfile(file_name):
        print(Fore.LIGHTYELLOW_EX + "[-BF Error]: Save File not found. Dont worry it will auto-create!" + Style.RESET_ALL)
        write_file(file_name, '')
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")
    print(Fore.LIGHTGREEN_EX + "[-BF Error]: Save File created" + Style.RESET_ALL)
