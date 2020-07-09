# XSS Blue

Project Beta created by Youssef Hany for LEGAL website testing purposes.

Please make sure you have the appropriate permissions before use.

## Fuzzing Function
This program works with GET and POST requests. By either fuzzing the payload in the url (GET), or auto-search for formdata to fill with payloads then submit the form (POST).
```
Expected URL in get GET: https://example.com/page.php?var=
```
```
Expected URL in get POST: https://example.com/page
                          https://example.com/page.php
```
## Spider Function
The spider crawls the target website and provides all the available clickable href links that are under the same Domain Name to stay in scope. Also as it crawls the website it saves the pages contianing forms in file named '${project_name}/form_links.txt'. It creates a project folder with the name of the website. Conclusively it collects all the form pages that are found in a website to fuzz later.

## Automization Function
Chooses a folder that is named after the website name as a project name for the folder. It should contain the files created by the crawler, Queue.txt, crawled.txt, form_links.txt, form_links_tested.txt. On providing the project name the program automatically will try to fuzz all the links in the file concurrently through multiprocessing and threading. So you will see different links being fuzzed at the same time.

## Results
The program will keep fuzzing until it finds 5 unique payloads or will just finish all the payloads available and print out whatever worked.

## Difference between other XSS programs
As there are some XSS programs that work well. However, most of the programs just dont always work right. And if they do work they dont always get the payload even if it is really vulnerable. Moreover, if a website loads Dynamically other XSSers will not be able to pick up the form data after render so will not be able to fuzz. XSS BLUE, have overcome this hardship by using dynamic javascript rendering, we first render the page and scroll through it to make sure all elements apear.

## Side Notes
This is just a beta version so it may have many issues and bugs. But over time my hope is that it improves alot to become the best and most reliable XSS Vulnerability Testing program

------------------
Disclaimer: I am not responsible for any actions taken by the individuals who have used this programs for negative/illegal purposes. I hope that people only use it to discover vulnerabilities in their own websites rather than try to invade other websites.. Stay Ethical!
