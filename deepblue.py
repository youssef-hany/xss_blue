#!/usr/bin/python
from bs4 import BeautifulSoup
from urllib.parse import urljoin
#from xpathIter import xpath_soup
import concurrent.futures
import requests
import time
import sys
import colorama
from colorama import Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from base_functions import *
colorama.init()

class Deep:
	found = 0
	counter = 0
	project_name = ''
	ThreadName=""
	Wfile = ''
	site = ''
	choice = ''
	mode = ''
	pog = ''
	seleniumBrowser = ''
	form_links_file = ''
	form_links_tested_file = ''
	form_links = set()
	form_links_testing = set()
	form_links_tested = set()
	current_executor = ''
	ptrForms = []
	payloads = ''
	formdata = ''
	Wpayloads = []
	working_payloads = ''
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
	

	
	def __init__(self, choice, site, mode, project_name, Wfile, ThreadName="Master Thread"):
			Deep.choice = choice
			Deep.site = site
			Deep.mode = mode
			Deep.ThreadName = ThreadName
			Deep.project_name = project_name
			Deep.Wfile = Wfile	
			
			if Deep.choice.lower() == "1":
				self.Get_Funtion(Deep.site, Deep.Wfile)

			elif Deep.choice.lower() == '2':
				self.Post_Function(Deep.site, Deep.Wfile, Deep.mode)

			elif Deep.choice.lower() == "3":	
				Deep.form_links_file = Deep.project_name + '/form_links.txt'
				Deep.form_links_tested_file = Deep.project_name + '/form_links_tested.txt'
				Deep.form_links = file_to_set(Deep.form_links_file)
				Deep.form_links_tested = file_to_set(Deep.form_links_tested_file)
				self.Automated_Function(Deep.site, Deep.Wfile, Deep.mode)
			else:
				print("[-] Wrong option choose Wisely xD")
				sys.exit(0)
			
	
	
	
	
		
	@staticmethod
	def Get_Funtion(site, file):
		
		try:
			Deep.site = site
			r = requests.post(Deep.site, headers = Deep.header)
			options = FirefoxOptions()
			options.add_argument("--headless")
			Deep.seleniumBrowser = webdriver.Firefox(options=options)
			print("[-] Website State: " + Fore.GREEN +  "Live!" + Style.RESET_ALL)
			print(Fore.GREEN + "[-] Selenium Successfully launched!" + Style.RESET_ALL)

		except Exception as e:

			print("[-] Website State: " + Fore.RED + "No response from website" + Style.RESET_ALL)
			time.sleep(3)
			print(e)
			#try another thing here before exit
			sys.exit(0)

		try:
			payloads = open(file, "r")
		except FileNotFoundError:
			print(Fore.RED + "[-] The file " + file + " doesn't exist in specified location!" + Style.RESET_ALL)
			Deep.CloseProgram()

		print(Fore.BLUE + "[-] Starting The Process... \n" + Style.RESET_ALL)
		for line in payloads:
			time.sleep(.5)
			Deep.counter += 1
			print("[-] Testing payload [F(" + str(Deep.found)+") C("+ str(Deep.counter) + ")]: " + line.rstrip())
			if Deep.found > 5:
				midCheck = input("[-] You have found" + str(Deep.found) +"payloads do you still want to continue? ")
				if midCheck.lower() == "yes":
					continue
				elif midCheck.lower() == "no":
					break
				else:
					print("[-] Invalid Input (continuing...) ctrl+C for break")
					continue
			try:
				text = requests.get(Deep.site + line, headers=Deep.header).text
			except:
				print("[-] Could not get website text after Testing")
				continue
			if line in text:
				#up until here it will be found in the page text but this gives false positives
				print(Fore.YELLOW + "[-] Possible XSS Vector!" + Style.RESET_ALL)	
				try:
					Deep.seleniumBrowser.get(requests.get(Deep.site + line, headers=Deep.header).url)
					WebDriverWait(Deep.seleniumBrowser, 3).until(EC.alert_is_present(),
		                           Fore.MAGENTA + "[-] Nope, it's a false positive don't bother" + Style.RESET_ALL)
					alert = Deep.seleniumBrowser.switch_to.alert
					alert.accept()
					print(Fore.BLUE + "[-] Alert Accepted" + Style.RESET_ALL)
					if alert:
						Deep.found += 1
						print(Fore.GREEN + "[-] XSS FOUND: " + requests.get(Deep.site + line, headers=Deep.header).url + Style.RESET_ALL)
						print(Fore.BLUE + "[-] Number of available payloads until now: " + str(Deep.found) + "\n"  + Style.RESET_ALL)
				except Exception as e:
					print(e)
					continue
			else:
    			#this also could be a false positive in some cases so should be resolved
				print(Fore.RED + "[-] NO XSS" + Style.RESET_ALL)
		print("[-] Finished fuzzing the input...")

		if Deep.found > 0:

			print(Fore.GREEN + """ 
			 _______________________________
			|Number Available|	{}	|
			|----------------|--------------|
			| Available XSS	 |	here	|
			|________________|______________|
			""".format(Deep.found))
		else:
			print(Fore.RED + """
					 _________________________________________________
					|		Website Seems Secure		  |
					|No XSS was found in the website, try another file|
					|_________________________________________________|
					""")


	@staticmethod
	def Post_Function(site, file, mode):
		seleniumBrowser = '' # TO AVOID CRASHING WHEN CALLED BUT NOT INITIALIZED

		try:
			print("[-] Testing URL: " + site)
			r = requests.get(site, headers=Deep.header)
			html_text = r.text
			soupParser = BeautifulSoup(html_text, 'html.parser')
			print("[-] Selenium settings set...")
			options = FirefoxOptions()
			browserHeadOp = mode
			if browserHeadOp:
				if(browserHeadOp.lower() == "h"):
					pass #doNothing because it launched head by default
				elif browserHeadOp.lower() == "hl":
					options.add_argument("--headless")
				else:
					print("Not a valid input")
					browserHeadOp = input("[-] Do you wand a Head/Headless launch?[H/HL] Default:[HL]: ")
			else:
				options.add_argument("--headless")

			print(Fore.GREEN + '[-] POST environment is ready' + Style.RESET_ALL)
			forms = soupParser.find_all('form')
			fcnt = 0
			fields= []
			formdata = []
			ptrForms = []
			if r.text:
				print(Fore.GREEN + "[-] The site is Live!" + Style.RESET_ALL)
			for form in forms:
				fcnt += 1
				inputs = form.find_all('input')
				textareas = form.find_all('textarea')
				fields.append(inputs)
				fields.append(textareas)
				
				if len(inputs) > 1 or len(textareas) >= 1:
					tocnt = fcnt
					ptrForms.append(form)
					
			if len(fields) > 1:
				for field in fields:
					for i in field:
						if "submit" not in str(i) and "hidden" not in str(i) and "action" not in str(i):
							#inputName = i.get('name')
							formdata.append((i.get('name'), i.get('value')))
				print(Fore.GREEN + "[-] Found data fields to work with" + Style.RESET_ALL)
				print("[-] Launching Selenium")
				seleniumBrowser = webdriver.Firefox(options=options)
				seleniumBrowser.get(r.url)
				print("[-] Selenium Launched !")
				
			else: 
				print(Fore.RED + "[-] No data fields found could not execute program will exit!" + Style.RESET_ALL)	
				seleniumBrowser.quit()		
				Deep.CloseProgram()

		
				
			formdata = dict(formdata)
		except Exception as e:
			print(e)
			print(Fore.RED + "[-] No response from website" + Style.RESET_ALL)
			#try another thing here before exit
			if seleniumBrowser:
				seleniumBrowser.quit()	
			Deep.CloseProgram()

		print()
		try:
			payloads = open(file, "r")

		except FileNotFoundError:
			print(Fore.RED + "[-] The file " + file + " doesn't exist in specified location!" + Style.RESET_ALL)
			seleniumBrowser.quit()	
			Deep.CloseProgram()

		print(Fore.GREEN + "[-] Testing.... \n" + Style.RESET_ALL)
		for line in payloads:
			time.sleep(1)
			Deep.counter += 1
			print("[-] Testing payload: F(" + str(Deep.found)+") C("+ str(Deep.counter) + ")"  + str(line.rstrip()))
			print(formdata)
			for fd in formdata:
				if str(fd) != "None" and str(fd) != "action" and str(fd) != "hidden":
					time.sleep(1)
					selector = seleniumBrowser.find_element_by_name(fd)
					selector.clear()
					selector.send_keys(line)
			try: 
				for f in ptrForms:
					inputs = f.find_all("input")
					for i in inputs:
						if "submit" in str(i):
							identifier = i.get("id")
							attrib = "id"
							if identifier == None:
								attrib = "class"
								identifier = i.get("class")[0]
							

				try:
					if attrib == "class":
						submit = seleniumBrowser.find_element_by_class_name(identifier)
						submit.click()
					elif attrib == "id":
						submit = seleniumBrowser.find_element_by_id(identifier)
						submit.click()
				except:
					pass
				WebDriverWait(seleniumBrowser, 1).until(EC.alert_is_present(), Fore.RED + "[-] No XSS" + Style.RESET_ALL)
				try:
					if seleniumBrowser:
						alert = seleniumBrowser.switch_to.alert
						time.sleep(1)
						alert.accept()
				except:
					if seleniumBrowser:
						if alert:
								alert.dismiss()
				print(Fore.BLUE + "[-] Alert Accepted" + Style.RESET_ALL)
				if alert:
					Deep.found+=1
					print(Fore.GREEN + "[-] XSS FOUND !" + Style.RESET_ALL)
					print(Fore.GREEN + "[-] Payload: "+ str(line) + Style.RESET_ALL)
					print(Fore.BLUE + "[-] Number of available payloads until now: " + str(Deep.found) + "\n"  + Style.RESET_ALL)
					seleniumBrowser.get(r.url)
					seleniumBrowser.refresh()
					if Deep.found >= 2:
						print("[-] 2 XSS Payloads have been found, time to stop now :)")
						seleniumBrowser.quit()	
						Deep.CloseProgram()
						break

			except Exception as e:
				seleniumBrowser.get(r.url)
				seleniumBrowser.refresh()
				print(e)
				continue


	@staticmethod
	def Automated_Function(site, Wfile, mode):
		if Deep.seleniumBrowser != '':
			Deep.Fuzz_On_Thread()
		if (Deep.site not in Deep.form_links_tested) and (Deep.site not in Deep.form_links_testing) and (Deep.site not in Deep.form_links_tested) and (Deep.seleniumBrowser == ''):
			print(f"[-] Queue ({str(len(Deep.form_links))}) | Tested  ({str(len(Deep.form_links_tested))})")
			try:
				
				print("[-] [{}] Testing URL: ".format(Deep.ThreadName) + Deep.site)
				Deep.form_links.remove(Deep.site)	
				Deep.form_links_testing.add(Deep.site)
				Deep.form_links_tested.add(Deep.site)
				r = requests.get(Deep.site, headers=Deep.header)
				html_text = r.text
				soupParser = BeautifulSoup(html_text, 'html.parser')
				print("[-] [{}] Selenium settings set...".format(Deep.ThreadName))
				options = FirefoxOptions()
				browserHeadOp = mode
				if browserHeadOp:
					if(browserHeadOp.lower() == "h"):
						pass
						#doNothing because it launched head by default
					elif browserHeadOp.lower() == "hl":
						options.add_argument("--headless")
					else:
						print("[-] Not a valid input lanching headless")
						browserHeadOp = ("--headless")
				else:
					options.add_argument("--headless")
				print("[-] Launching Selenium..." )
				Deep.seleniumBrowser = webdriver.Firefox(options=options)
				print("[-] Website State: " + Fore.GREEN +  "Live!" + Style.RESET_ALL)
				print(Fore.GREEN + "[-] Selenium Successfully launched!" + Style.RESET_ALL)
				
				print(Fore.GREEN + f"[-] [{Deep.ThreadName}] POST environment is ready" + Style.RESET_ALL)
				forms = soupParser.find_all('form')
				fcnt = 0
				fields= []
				formdata = []
				ptrForms = []
				# if r.text:
				# 	print(Fore.GREEN + "[-] [{}] The site is Live!".format(Deep.ThreadName) + Style.RESET_ALL)
				for form in forms:
					fcnt += 1
					inputs = form.find_all('input')
					textareas = form.find_all('textarea')
					fields.append(inputs)
					fields.append(textareas)
					
					if len(inputs) > 1 or len(textareas) >= 1:
						tocnt = fcnt
						Deep.ptrForms.append(form)

				if len(fields) > 1:
					try:
						Deep.seleniumBrowser.get(r.url)
					except Exception as e:
						print(e)
					print(Fore.GREEN + f"[-] [{Deep.ThreadName}] Found data fields to work with"+ Style.RESET_ALL)
					for field in fields:
						for i in field:
							if "submit" not in str(i) and "hidden" not in str(i) and "action" not in str(i):
    						# 		inputName = i.get("name")
							# 	if inputName == "None":
							# 		inputName = i.get("id")
							#check here for the none type
								formdata.append((i.get('name'), i.get('value')))
				else:
					print(Fore.RED + f"[-] [{Deep.ThreadName}] No data fields found could not execute Thread will exit!" + Style.RESET_ALL)			
					Deep.form_links.remove(Deep.site)
					Deep.CloseProgram()
					
					
				Deep.formdata = dict(formdata)
			except Exception as e:
				if "Failed to establish a new connection" in str(e):
					print(e)
					print(Fore.RED + f"[-] [{Deep.ThreadName}] Check Internet Connection!" + Style.RESET_ALL)
					Deep.CloseProgram()
				else:	
					print(Fore.RED + f"[-] [{Deep.ThreadName}] No response from url {Deep.site}" + Style.RESET_ALL)
				#try another thing here before exit
				if Deep.current_executor:
					Deep.current_executor.shutdown()
				Deep.CloseProgram()
			
			print()
			try:
				if not Deep.payloads:
					Deep.payloads = list(file_to_set(Deep.Wfile))
					Deep.payloads.reverse()
			except FileNotFoundError:
				print(Fore.RED + "[-] The file " + Wfile + " doesn't exist in specified location!" + Style.RESET_ALL)
				Deep.CloseProgram()

			print(Fore.GREEN + f"[-] [{Deep.ThreadName}] Testing with {len(Deep.payloads)} payloads.... \n"+ Style.RESET_ALL)
			
			Deep.working_payloads = Deep.Fuzz_On_Thread()
			

	


	@staticmethod
	def Fuzz_Inputs():
		if Deep.seleniumBrowser:
			# Deep.payloads = ''
			# Deep.payloads = open(Deep.Wfile, "r")
			for line in Deep.payloads:
				time.sleep(1)
				Deep.counter += 1
				if Deep.Check_If_Found(5):
					break
				print(Fore.CYAN +  f"[-] [{Deep.site}] [{Deep.ThreadName}] Instance Info: F({str(Deep.found)}) C({str(Deep.counter)})" + Fore.GREEN + " Testing Payload: " + Fore.MAGENTA + f" {str(line.rstrip())} " + Style.RESET_ALL)
				#print(Deep.formdata)
				for fd in Deep.formdata:
						if str(fd) != "None" and str(fd) != "action" and str(fd) != "hidden":
							try:
								WebDriverWait(Deep.seleniumBrowser, 3).until(EC.element_to_be_clickable((By.NAME, fd)))
								selector = Deep.seleniumBrowser.find_element_by_name(fd)
								selector.clear()
								selector.send_keys(line)
							except Exception as e:
								if "dialog" in str(e): 	#This checks for when multiple alerts are triggered the firefox sends another type of alert
														#The other alert has a check box if you want to disable alerts from this website
									print(Fore.LIGHTRED_EX +  f"[-] Probably Reflected XSS is present on this current URL {Deep.site}" +Style.RESET_ALL)
									if Deep.Check_If_Found(5):
										break
								else:
									print("[Error]: Problem with sending input  " + str(e))
									
								continue
														
				try: 
					for f in Deep.ptrForms:
						inputs = f.find_all("input")
						for i in inputs:
							if "submit" in str(i):
								attrib = "id"
								identifier = i.get("id")
								if identifier == None:
									attrib = "class"
									identifier = i.get("class")[0]
									if identifier == None:
										attrib = "name"
										identifier = i.get("name")[0]
										if identifier == None:
											attrib = "type"
											identifier = i.get("type")[0]
								

					try:
						if attrib == "class":
							submit = Deep.seleniumBrowser.find_element_by_class_name(identifier)
							submit.click()
						elif attrib == "id":
							submit = Deep.seleniumBrowser.find_element_by_id(identifier)
							submit.click()
						elif attrib == "name":
							submit = Deep.seleniumBrowser.find_element_by_name(identifier)
							submit.click()
						# elif attrib == "typ":
						# 		submit = Deep.seleniumBrowser.find_element_by_id(identifier)
						# 	submit.click()
					except Exception as e:
						if "dialog" in str(e):
							print(Fore.LIGHTRED_EX +  f"[-] Probably Reflected XSS is present on this current URL {Deep.site}" +Style.RESET_ALL)
							if Deep.Check_If_Found(5):
								break
						else:
							print("[Error]: Problem with submitting  " + str(e))
						continue
					noxx = print(Fore.RED + "\r[-] No XSS " + Style.RESET_ALL)
					WebDriverWait(Deep.seleniumBrowser, 1).until(EC.alert_is_present(),noxx)
					
					try:
						if Deep.seleniumBrowser:
							alert = Deep.seleniumBrowser.switch_to.alert
							time.sleep(1)
							alert.accept()
						if alert:
							Deep.found += 1
							Deep.Wpayloads.append(line)
							print(Fore.BLUE + f"[-] [{Deep.site}] Alert Accepted" + Style.RESET_ALL)
							print(Fore.GREEN + Style.BRIGHT + f"[-] [{Deep.ThreadName}] XSS FOUND in url [- {Deep.site} -]!"+ Style.RESET_ALL)
							print(Fore.GREEN + Style.BRIGHT + f"[-] [{Deep.ThreadName}] Payload: {str(line)} + URL: {Deep.site}" + Style.RESET_ALL)
							print(Fore.LIGHTCYAN_EX + Style.BRIGHT  + f"[-] [{Deep.site}] Number of available payloads until now: {str(Deep.found)}"  + "\n"  + Style.RESET_ALL)
							if Deep.Check_If_Found(5):
								break
							Deep.seleniumBrowser.get(Deep.site)
							Deep.seleniumBrowser.refresh()
					except Exception as e:
						
						if Deep.seleniumBrowser:		
							if alert:
								alert.dismiss()
								print(Fore.BLUE + Style.BRIGHT + f"[-] [{Deep.site}] Alert Dismissed" + Style.RESET_ALL)
								if Deep.Check_If_Found(5):
									break
							else:
								print("[Error]: Problem with the alert" + str(e))
								
							continue
					
							
				except Exception as e:
					if "Error" in str(e):
						print(str(e))
						print("PUT A SHUTDOWN HERE")
						Deep.CloseProgram()
						break
						# Deep.Update_Files()
						# # Deep.current_executor.shutdown()
						# # break
						# # return(Deep.Wpayloads)
					
					Deep.seleniumBrowser.get(Deep.site)
					Deep.seleniumBrowser.refresh()
					continue
					
					
		else:
			Deep.CloseProgram()

			
	@staticmethod
	def Fuzz_On_Thread():
		with concurrent.futures.ThreadPoolExecutor() as executor:
			Deep.current_executor = executor		
			Deep.current_executor.submit(Deep.Fuzz_Inputs)
					
	@staticmethod
	def Update_Files():
		set_to_file(Deep.form_links, Deep.form_links_file)
		set_to_file(Deep.form_links_tested, Deep.form_links_tested_file)

	@staticmethod
	def CloseProgram():
		if str(Deep.choice.lower) == '3':
			Deep.form_links_tested.add(Deep.site)
			Deep.form_links_testing.remove(Deep.site)	
			Deep.form_links.remove(Deep.site)	
			Deep.Update_Files()
		if Deep.seleniumBrowser:
			Deep.seleniumBrowser.close()
			Deep.seleniumBrowser.quit()
		sys.exit(0)

	@staticmethod
	def Check_If_Found(number_of_found):
		if Deep.found >= number_of_found:
			print(f"[-EX-] [{Deep.site}] Multiple XSS Payloads have been found, time to stop this thread now :)")
			#Deep.Print_Results()
			# raise Exception("[-] [{Deep.site}] 2 XSS Payloads have been found, time to stop this thread now :)")
			#Deep.CloseProgram()
			Deep.Update_Files()
			Deep.current_executor.shutdown()
			Deep.CloseProgram()
			return(Deep.Wpayloads)
		else:
			return(False)
	@staticmethod
	def Print_Results():
		result = (f""" 
			~~~~~~~~~~~~~~~~~~~~~~~~.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			|    Number Available   |     {Deep.found} Payloads		|
			~~~~~~~~~~~~~~~~~~~~~~~~.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			"""+ Fore.LIGHTBLUE_EX + f"""Site URL: {Deep.site} \n"""+ Fore.GREEN + Style.BRIGHT)
		print(result)
		x = 0
		for payload in Deep.Wpayloads:
			x += 1
			print( f"[{x}] " + payload)	
		print('\n' + Style.RESET_ALL)
		return (Deep.Wpayloads)