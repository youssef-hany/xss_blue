#!/usr/bin/python
from bs4 import BeautifulSoup
from urllib.parse import urljoin
#from xpathIter import xpath_soup
import concurrent.futures
import requests
import time
import sys
import signal
import json
from stem import Signal
from stem.control import Controller
import colorama
from colorama import Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from base_functions import *
from requests_html import HTMLSession
colorama.init()

class Deep():
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
	formdata = dict()
	Wpayloads = []
	working_payloads = ''
	session = ''
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
	globalLine = ''
	html_element = ''
	attrib = ''
	identifier = ''
	learn_data = []
	interrupted = False

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
	def signal_handler(sig, frame):
		Deep.interrupted = True
		print('You pressed Ctrl+C!')
		try:
			userInput = input("\r\nReally quit? (y/n)>")
			if userInput.lower().startswith('y'):
				print('Closing the browser drivers and cleaning up the application!')
				Deep.CloseProgram()
				sys.exit(1)
			pass	
				

		except KeyboardInterrupt:
			print("Ok ok, quitting")
			print('Closing the browser drivers and cleaning up the application!')		
			Deep.CloseProgram()
			sys.exit(1)
		
		

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
			if not Deep.payloads:
				Deep.payloads = list(file_to_set(Deep.Wfile))
				Deep.payloads.reverse()

		except FileNotFoundError:
			print(Fore.RED + "[-] The file " + file + " doesn't exist in specified location!" + Style.RESET_ALL)
			Deep.CloseProgram()

		print(Fore.GREEN + f"[-] [{Deep.ThreadName}] Testing with {len(Deep.payloads)} payloads.... \n"+ Style.RESET_ALL)
		Deep.Fuzz_URL_On_Thread()

		print("[-] Finished fuzzing the input...")
		#print(Deep.learn_data)
		list_to_file(Deep.learn_data, "learn_data.csv")
		# if Deep.found > 0:

		# 	print(Fore.GREEN + """ 
		# 	 _______________________________
		# 	|Number Available|	{}	|
		# 	|----------------|--------------|
		# 	| Available XSS	 |	here	|
		# 	|________________|______________|
		# 	""".format(Deep.found))
		# else:
		# 	print(Fore.RED + """
		# 			 _________________________________________________
		# 			|		Website Seems Secure		  |
		# 			|No XSS was found in the website, try another file|
		# 			|_________________________________________________|
		# 			""")


	@staticmethod
	def Post_Function(site, file, mode):
		seleniumBrowser = '' # TO AVOID CRASHING WHEN CALLED BUT NOT INITIALIZED

		try:
			print("[-] Testing URL: " + site)
			Deep.session = requests.session()
			Deep.session.proxies = {'http':'socks5://127.0.0.1:9050',
								'https': 'socks5://127.0.0.1:9050'}
			r = Deep.session.get(site, headers=Deep.header)
			html_text = r.text
			#Deep.session.close()
			html_session = HTMLSession()
			resp = html_session.get(Deep.site)
			resp.html.render(timeout=30) #loading js in website before taking html for dynamic rendering purposes
			soupParser = BeautifulSoup(resp.html.html, 'html.parser') # dynamic rendering loaded
			resp.session.close()
			tor_ip = json.loads(Deep.session.get("http://httpbin.org/ip").text)
			real_ip = json.loads(requests.get("http://httpbin.org/ip").text)
			print(Fore.BLUE + Style.BRIGHT + "[INFO] TOR IP(Anonymous): " + tor_ip["origin"] + Style.RESET_ALL)
			print(Fore.RED + "[INFO] Real IP: " + real_ip["origin"] + Style.RESET_ALL)
			print("[-] Selenium settings set...")
			options = FirefoxOptions()
			browserHeadOp = mode
			#options.add_argument("--disable-notifications")
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
			Deep.html_element = soupParser.find_all('html')
			fcnt = 0
			fields= []
			formdata = set()
			ptrForms = []
			if r.text:
				print("[-] Website State: " + Fore.GREEN +  "Live!" + Style.RESET_ALL)
			#Deep.renew_tor_ip() #renewing the ip
			for form in Deep.html_element:
				fcnt += 1
				inputs = form.find_all('input')
				textareas = form.find_all('textarea')
				fields.append(inputs)
				fields.append(textareas)
				
				if len(inputs) > 1 or len(textareas) >= 1:
					Deep.ptrForms.append(form)
					
			if len(fields) > 1:
				for field in fields:
					for i in field:
						#print(i)
						if "submit" not in str(i) and "hidden" not in str(i) and "action" not in str(i):
							#inputName = i.get('name')
							formdata.add((i.get('name'), i.get('value')))
				
				print(Fore.GREEN + "[-] Found data fields to work with" + Style.RESET_ALL)
				print(Fore.CYAN + f"[INFO] Fields to be populated --> {formdata}" + Style.RESET_ALL)
				print("[-] Launching Selenium")
				Deep.seleniumBrowser = webdriver.Firefox(options=options)
			
				print("[-] Selenium Launched !")
			
				
			else: 
				print(Fore.RED + "[-] No data fields found could not execute program will exit!" + Style.RESET_ALL)	
				Deep.seleniumBrowser.quit()		
				Deep.CloseProgram()

		
				
			Deep.formdata = dict(formdata)
		except Exception as e:
			if "Network is unreachable" in str(e):
				print(Fore.RED + f"[-] [{Deep.ThreadName}] Website Is Unreachable O.O!" + Style.RESET_ALL)
				Deep.CloseProgram()
			if "Failed to establish a new connection" in str(e):
				#print(e)
				print(Fore.RED + f"[-] [{Deep.ThreadName}] Check Internet Connection!" + Style.RESET_ALL)
				Deep.CloseProgram()
			else:	
				print(e)
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
			# if not Deep.payloads:
			# 	Deep.payloads = open(Deep.Wfile, 'rt')
			# 	Deep.payloads = list(Deep.payloads)
		

		except FileNotFoundError:
			print(Fore.RED + "[-] The file " + file + " doesn't exist in specified location!" + Style.RESET_ALL)
			Deep.seleniumBrowser.quit()	
			Deep.CloseProgram()

		print(Fore.GREEN + f"[-] [{Deep.ThreadName}] Testing with {len(Deep.payloads)} payloads.... \n"+ Style.RESET_ALL)
		try:
			Deep.seleniumBrowser.get(Deep.site)
			Deep.working_payloads = Deep.Fuzz_On_Thread()
			Deep.Print_Results()
			#print(Deep.learn_data)
			list_to_file(Deep.learn_data, "learn_data.csv")
			Deep.CloseProgram()
		except Exception as e:
			#print(e)
			Deep.CloseProgram()
			

	


	@staticmethod
	def Automated_Function(site, Wfile, mode):
		if Deep.seleniumBrowser != '':
			Deep.Fuzz_On_Thread()
		if (Deep.site not in Deep.form_links_tested) and (Deep.site not in Deep.form_links_testing) and (Deep.site not in Deep.form_links_tested) and (Deep.seleniumBrowser == ''):
			print(f"[-] Queue ({str(len(Deep.form_links))}) | Tested  ({str(len(Deep.form_links_tested))})")
			try:
				
				print("[-] [{}] Testing URL: ".format(Deep.ThreadName) + Deep.site)
				
				#Deep.form_links.remove(Deep.site)	
				Deep.form_links_testing.add(Deep.site)
				Deep.form_links_tested.add(Deep.site)	
				Deep.session = requests.session()
				Deep.session.proxies = {'http':'socks5://127.0.0.1:9050',
									'https': 'socks5://127.0.0.1:9050'}
				r = Deep.session.get(Deep.site, headers=Deep.header)
				html_text = r.text
				#Deep.session.close()
				html_session = HTMLSession()
				resp = html_session.get(Deep.site)
				resp.html.render(timeout=30) #loading js in website before taking html for dynamic rendering purposes
				soupParser = BeautifulSoup(resp.html.html, 'html.parser') # dynamic rendering loaded
				resp.session.close()
				tor_ip = json.loads(Deep.session.get("http://httpbin.org/ip").text)
				real_ip = json.loads(requests.get("http://httpbin.org/ip").text)
				print(Fore.BLUE + Style.BRIGHT + "[INFO] TOR IP(Anonymous): " + tor_ip["origin"] + Style.RESET_ALL)
				print(Fore.RED + "[INFO] Real IP: " + real_ip["origin"] + Style.RESET_ALL)
				#ip stuff should be here but instead it is in main to be run only once before all Processes
				print("[-] Selenium settings set...")
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

				if r.text:
					print("[-] Website State: " + Fore.GREEN +  "Live!" + Style.RESET_ALL)
				print(Fore.GREEN + f"[-] [{Deep.ThreadName}] POST environment is ready" + Style.RESET_ALL)
				forms = soupParser.find_all('html')
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
					for field in fields:
						for i in field:
							#print(i)
							if "submit" not in str(i) and "hidden" not in str(i) and "action" not in str(i):
								#inputName = i.get('name')
								formdata.append((i.get('name'), i.get('value')))

					print(Fore.GREEN + "[-] Found data fields to work with" + Style.RESET_ALL)
					print(Fore.CYAN + f"[INFO] Fields to be populated --> {formdata}" + Style.RESET_ALL)
					print("[-] Launching Selenium")
					Deep.seleniumBrowser = webdriver.Firefox(options=options)
				
					print(Fore.GREEN + "[-] Selenium Successfully launched!" + Style.RESET_ALL)
				else:
					print(Fore.RED + f"[-] [{Deep.ThreadName}] No data fields found could not execute Thread will exit!" + Style.RESET_ALL)			
					Deep.form_links.remove(Deep.site)
					Deep.CloseProgram()
					
					
				Deep.formdata = dict(formdata)
			except Exception as e:
				print(e)
				if "Network is unreachable" in str(e):
					print(Fore.RED + f"[-] [{Deep.ThreadName}] Website Is Unreachable O.O!" + Style.RESET_ALL)
					Deep.CloseProgram()
				if "Failed to establish a new connection" in str(e):
					#print(e)
					print(Fore.RED + f"[-] [{Deep.ThreadName}] Check Internet Connection!" + Style.RESET_ALL)
					Deep.CloseProgram()
				else:	
					print(e)
					print(Fore.RED + f"[-] [{Deep.ThreadName}] No response from url {Deep.site}" + Style.RESET_ALL)
				#try another thing here before exit
				if Deep.current_executor:
					Deep.current_executor.shutdown()
				Deep.CloseProgram()
			
			try:
				if not Deep.payloads:
					Deep.payloads = list(file_to_set(Deep.Wfile))
					Deep.payloads.reverse()
			except FileNotFoundError:
				print(Fore.RED + "[-] The file " + Wfile + " doesn't exist in specified location!" + Style.RESET_ALL)
				Deep.CloseProgram()

			print(Fore.GREEN + f"[-] [{Deep.ThreadName}] Testing with {len(Deep.payloads)} payloads.... \n"+ Style.RESET_ALL)
			
			Deep.working_payloads = Deep.Fuzz_On_Thread()
			#print(Deep.learn_data)
			list_to_file(Deep.learn_data, "learn_data.csv")
			

	@staticmethod
	def Fuzz_URL():
		resume = False
		for line in Deep.payloads:
			time.sleep(.5)
			Deep.counter += 1
			
			print(Fore.CYAN +  f"[Info]: F({str(Deep.found)}) C({str(Deep.counter)})/({len(Deep.payloads)})" + Fore.GREEN + " Testing Payload: " + Fore.MAGENTA + f" {str(line.rstrip())} " + Style.RESET_ALL)
			if Deep.found >= 1 and not resume: #can make user decide that number later
				print(f"[-] Found {Deep.found} working payloads still want to continue fuzzing?")
				response = input("[-] Y/N [Default:N]: ")
				if response.lower().startswith("y"):
					resume = True
					print("[-] Continuing...")
					pass
				else:
					Deep.CloseProgram()
					break
			try:
				text = requests.get(Deep.site + line, headers=Deep.header).text
			except:
				print("[-] Could not get website text after Testing")
				Deep.seleniumBrowser.refresh()
				continue
			if line in text:
				#up until here it will be found in the page text but this gives false positives
				print(Fore.YELLOW + "[-] Possible XSS Vector!" + Style.RESET_ALL)	
				try:
					Deep.seleniumBrowser.get(requests.get(Deep.site + line, headers=Deep.header).url)
					WebDriverWait(Deep.seleniumBrowser, 3).until(EC.alert_is_present(), Fore.MAGENTA + "[-] Nope, it's a false positive don't bother" + Style.RESET_ALL)
					alert = Deep.seleniumBrowser.switch_to.alert
					alert.accept()
					print(Fore.BLUE + "[-] Alert Accepted" + Style.RESET_ALL)
					if alert:
						Deep.found += 1
						Deep.Wpayloads.append(line)
						Deep.learn_data.append((line, text.replace("\n", "").rstrip("\n"), 2))
						print(Fore.GREEN + f"[-] XSS FOUND: {Deep.site}{line}" + Style.RESET_ALL)
						print(Fore.BLUE + f"[-] Number of available payloads until now: {Deep.found} \n"  + Style.RESET_ALL)
						
				except Exception as e:
					print(e)
					Deep.learn_data.append((line, text.replace("\n", "").rstrip("\n"), 1))
					continue
			else:
				#this also could be a false positive in some cases so should be resolved
				print(Fore.RED + "[-] NO XSS" + Style.RESET_ALL)
				Deep.learn_data.append((line, text.replace("\n", "").rstrip("\n"), 0))

	@staticmethod
	def Fuzz_Inputs():
		try:
			if Deep.seleniumBrowser:
				# Deep.payloads = ''
				# Deep.payloads = open(Deep.Wfile, "r")
				for line in Deep.payloads:
					Deep.globalLine = line
					try:
						Deep.text = requests.get(Deep.site, headers=Deep.header).text
						Deep.text = Deep.text.replace("\n", "")
						Deep.seleniumBrowser.get(Deep.site)
					except:
						print(f"[-] [{Deep.site}] [{Deep.ThreadName}] Could not get website text after Testing")
						continue
					
					#time.sleep(1) was here to prevent site from blocking or crashing
					Deep.counter += 1
					if Deep.counter % 15 == 0:
						Deep.renew_tor_ip()
					
					
					if Deep.Check_If_Found(5):
						Deep.CloseProgram()
						break
					print(Fore.CYAN +  f"[-] [{Deep.site}] [{Deep.ThreadName}] Instance Info: F({str(Deep.found)}) C({str(Deep.counter)})/({len(Deep.payloads)})" + Fore.GREEN + " Testing Payload: " + Fore.MAGENTA + f" {str(line.rstrip())} " + Style.RESET_ALL)
					try:
						alert = Deep.seleniumBrowser.switch_to.alert
						if alert:
							alert.accept()
							print(Fore.RED + Style.BRIGHT + f"[-] [{Deep.site}] Alert accepted on page load/reload. This indicates signs of Stored XSS check manually! is it a comment section?" + Style.RESET_ALL)
							Deep.CloseProgram()
							break
					except Exception as e:
						try:
							alert = Deep.seleniumBrowser.switch_to.alert
							if alert:
								alert.dismiss()
								print(Fore.RED + "[-] [{Deep.site}] [{Deep.ThreadName}] There is a persistent alert in the page. may be because of Stored XSS !" + Style.RESET_ALL)
								Deep.CloseProgram()
								break
						except:
							pass
					print(Fore.CYAN + "[INFO] Populating data fields..." + Style.RESET_ALL)
					for fd in list(Deep.formdata):
						if Deep.seleniumBrowser:
							try:
								if str(fd) != "None" and str(fd) != "action" and str(fd) != "hidden":
									selector = Deep.seleniumBrowser.find_element_by_name(fd)
									selector.send_keys(line)
									time.sleep(.5)																		
									reselector = Deep.seleniumBrowser.find_element_by_name(fd)
									page_source = Deep.seleniumBrowser.page_source
									if line in str(page_source):
										print(Fore.YELLOW + f"[-] [{Deep.site}] [{Deep.ThreadName}] Payload reflects Dynamically(Directly on typing) in the page without being filered {line}" + Style.RESET_ALL)		
										Deep.learn_data.append((line, page_source.replace("\n", "").rstrip("\n"), 1))

							except Exception as e:
								if "Unable to locate element" in str(e):
									print(Fore.BLUE + f"[-] [{Deep.site}] [{Deep.ThreadName}] Could not Reselect element after adding input, maybe injectable element with Name={fd} with payload: {line}" + Style.RESET_ALL)
									pass
								elif "alert" in str(e).lower():
									try:
										print(Fore.GREEN + f"[-] [{Deep.site}] [{Deep.ThreadName}] Probable Stored/Dynamic XSS in the page. check {line} !" + Style.RESET_ALL)
										Deep.learn_data.append((line, Deep.text.replace("\n", "").rstrip("\n"), 2))
										# noxx = print(Fore.RED + "\r[-] No Dynamic XSS " + Style.RESET_ALL)
										# WebDriverWait(Deep.seleniumBrowser, 1).until(EC.alert_is_present(),noxx)
										if Deep.accept_alert():
											continue
									except Exception as e:
										print("[-] Could not Accept alert" + str(e))
										Deep.seleniumBrowser.get(Deep.site)
										Deep.seleniumBrowser.refresh()
										continue

										

								

						else:
							print("[-] No selenium Browser operating")
					try: 
						try:
							Deep.get_submit_input_tag()
							
						except Exception as e:
							print(e)

						try:
							if Deep.submit() == False:
								raise Exception("No input tag, trying button")
								
											
						except Exception as e:
			
							if "dialog" in str(e):
								print(Fore.GREEN + Style.BRIGHT + f"[-] [{Deep.site}] [{Deep.ThreadName}] Probably Dynamic/Stored XSS is present on this URL {Deep.site}. Payload: {line}" +Style.RESET_ALL)
								Deep.learn_data.append((line, Deep.text.replace("\n", "").rstrip("\n"), 2))
								if Deep.accept_alert():
									continue
								if Deep.Check_If_Found(5):
									Deep.current_executor.shutdown()
									break
							try:
								Deep.get_submit_button_tag()
								if Deep.submit() == False:
									break
								pass

							except Exception as e:
								if "element" in str(e).lower():
									continue
								print("[Error]: Problem with submitting  " + str(e))
								try:
									alert = Deep.seleniumBrowser.switch_to.alert
									if alert:
										alert.accept()
										print(Fore.RED + Style.BRIGHT + f"[-] [{Deep.site}] Alert accepted before load. This indicates signs of Stored XSS check manually! is it a comment section?" + Style.RESET_ALL)
										continue
								except Exception as e:
									print("[Index1]" + str(e))
									if "Failed to establish a new connection" in str(e):
										Deep.CloseProgram()
										break
									try:
										alert = Deep.seleniumBrowser.switch_to.alert
										if alert:
											alert.dismiss()
											print(Fore.RED + "[-] [{Deep.site}] [{Deep.ThreadName}] There is a persistent alert in the page. May be because of Stored XSS !" + Style.RESET_ALL)
											continue
									except:
											print("err2" + str(e))
											Deep.CloseProgram()
											break
										
								break

						noxx = print(Fore.RED + f"[-] [{Deep.site}] [{Deep.ThreadName}] No XSS " + Style.RESET_ALL)
						WebDriverWait(Deep.seleniumBrowser, 1).until(EC.alert_is_present(),noxx)
						if Deep.accept_alert():
							continue
						
								
					except Exception as e:
						if "dialog" in str(e):
							continue
						Deep.learn_data.append((line, Deep.text.replace("\n", "").rstrip("\n"), 0))

						if "[Error]" in str(e):
							print("Something wrong happened! " + str(e))
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
		except Exception as e:
			Deep.learn_data.append((Deep.globalLine, Deep.text.replace("\n", "").rstrip("\n"), 0))
			if "Reached error page" in str(e):
				print("[Error] [{Deep.site}] [{Deep.ThreadName}] Could not complete excecution the page went down " + str(e))
				Deep.CloseProgram()
			elif "alert" in str(e).lower():
				pass
			else:
				pass
				#print("[testing] error is: " + str(e))
			Deep.seleniumBrowser.get(Deep.site)
			Deep.seleniumBrowser.refresh()

	
	@staticmethod
	def get_submit_button_tag():
		for htm in Deep.html_element:
			buttons = htm.find_all("button")
			for button in buttons:
				if "submit" in str(button):
					Deep.attrib = "id"
					Deep.identifier = button.get("id")
					if Deep.identifier != None:
						pass
						#print(f"Submit id={Deep.identifier}")
					if Deep.identifier == None:	
						Deep.attrib = "class"
						try:
							Deep.identifier, *_ = button.get("class")
							#print(f"Submit Class={Deep.identifier}")
						except:
							Deep.attrib = "name"
							try:	
								Deep.identifier, *_ = button.get("name")
								#print(f"Submit name={Deep.identifier}")
							except:
								Deep.attrib = "value"
								Deep.identifier = button.get("value")
								#print(f"Submit value={Deep.identifier}")
						
	@staticmethod
	def get_submit_input_tag():
		attrib = ''
		for f in Deep.ptrForms:
			inputs = f.find_all("input")
			for i in inputs:
				if "submit" in str(i):
					Deep.attrib = "id"
					Deep.identifier = i.get("id")
					if Deep.identifier != None:
						pass
    					#print(f"Submit id={Deep.identifier}")
					if Deep.identifier == None:	
						Deep.attrib = "class"
						try:
							Deep.identifier, *_ = i.get("class")
							#print(f"Submit Class={Deep.identifier}")
						except:
							Deep.attrib = "name"
							try:	
								Deep.identifier, *_ = i.get("name")
								#print(f"Submit name={Deep.identifier}")
							except:
								Deep.attrib = "value"
								Deep.identifier = i.get("value")
								#print(f"Submit value={Deep.identifier}")
							
									
	@staticmethod
	def submit():
		if Deep.attrib == "class":
			# print("clicking in class")
			submit = Deep.seleniumBrowser.find_element_by_class_name(Deep.identifier)
			submit.click()
		
		elif Deep.attrib == "id":
			# print("clicking in id")
			submit = Deep.seleniumBrowser.find_element_by_id(Deep.identifier)
			submit.click()
		elif Deep.attrib == "name":
			# print("clicking in name")
			submit = Deep.seleniumBrowser.find_element_by_name(Deep.identifier)
			submit.click()
		elif Deep.attrib == "value":
			# print("clicking in value")
			submit = Deep.seleniumBrowser.find_element_by_css_selector(f"input[value*='{Deep.identifier}']")
			submit.click()
		else:
			return(False)
	
	@staticmethod
	def accept_alert():
		try:
			if Deep.seleniumBrowser:
				alert = Deep.seleniumBrowser.switch_to.alert
				alert.accept()
			if alert:
				Deep.found += 1
				Deep.Wpayloads.append(Deep.globalLine)
				print(Fore.BLUE + f"[-] [{Deep.site}] Alert Accepted" + Style.RESET_ALL)
				print(Fore.GREEN + Style.BRIGHT + f"[-] [{Deep.ThreadName}] XSS FOUND in url [- {Deep.site} -]!"+ Style.RESET_ALL)
				print(Fore.GREEN + Style.BRIGHT + f"[-] [{Deep.ThreadName}] Payload: {Deep.globalLine} + URL: {Deep.site}" + Style.RESET_ALL)
				print(Fore.LIGHTCYAN_EX + Style.BRIGHT  + f"[-] [{Deep.site}] Number of available payloads until now: {str(Deep.found)}"  + "\n"  + Style.RESET_ALL)
				Deep.learn_data.append((Deep.globalLine, Deep.text.replace("\n", "").rstrip("\n"), 1))
				if Deep.Check_If_Found(5):
					Deep.CloseProgram()
				Deep.seleniumBrowser.get(Deep.site)
				Deep.seleniumBrowser.refresh()
				return(True)
		except Exception as e:
			print("Err3: Maybe alert was already accepted continuing...")
			if Deep.seleniumBrowser:
				try:	
					alert = Deep.seleniumBrowser.switch_to.alert
					if alert:
						alert.dismiss()
						print(Fore.BLUE + Style.BRIGHT + f"[-] [{Deep.site}] Alert Dismissed" + Style.RESET_ALL)
						if Deep.Check_If_Found(5):
							Deep.CloseProgram()
						Deep.seleniumBrowser.get(Deep.site)
						Deep.seleniumBrowser.refresh()
						return(True)
					else:
						print("[Error]: Problem with the alert" + str(e))
						Deep.CloseProgram()
						return(False)
				except Exception as err:
					print("Could not dismiss alert" + str(err))
					return(True)
	@staticmethod
	def renew_tor_ip():
		with Controller.from_port(port=9051) as controller:
			controller.authenticate(password="Od1n1")
			controller.signal(Signal.NEWNYM)
		nTOR_IP = json.loads(Deep.session.get("http://httpbin.org/ip").text)
		print(Fore.CYAN + "[-] Sloppy, I am covering your back :). New IP" + Fore.BLUE + Style.BRIGHT + f" --> {nTOR_IP['origin']}" + Style.RESET_ALL)
	
	@staticmethod
	def Fuzz_URL_On_Thread():

			with concurrent.futures.ThreadPoolExecutor() as executor:
				signal.signal(signal.SIGINT, Deep.signal_handler)
				Deep.current_executor = executor		
				Deep.current_executor.submit(Deep.Fuzz_URL)

	@staticmethod
	def Fuzz_On_Thread():
		try:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				signal.signal(signal.SIGINT, Deep.signal_handler)
				Deep.current_executor = executor		
				Deep.current_executor.submit(Deep.Fuzz_Inputs)
		except Exception as e:
			print("[-] Error from Thread" + str(e))
					
	@staticmethod
	def Update_Files():
		if Deep.choice == "3":
			set_to_file(Deep.form_links, Deep.form_links_file)
			set_to_file(Deep.form_links_tested, Deep.form_links_tested_file)

	@staticmethod
	def CloseProgram():
		if str(Deep.choice.lower) == '3':
			Deep.form_links_tested.add(Deep.site)
			Deep.form_links_testing.remove(Deep.site)	
			Deep.form_links.remove(Deep.site)	
			Deep.Update_Files()
		if Deep.seleniumBrowser != '':
			Deep.seleniumBrowser.close()
			Deep.seleniumBrowser.quit()
		if Deep.current_executor != '':
			Deep.current_executor.shutdown()
		if Deep.session != '':
			Deep.session.close()
		sys.exit(0)

	@staticmethod
	def Check_If_Found(number_of_found):
		if Deep.found >= number_of_found:
			print(f"[-EX-] [{Deep.site}] Multiple XSS Payloads have been found, time to stop this thread now :)")
			#Deep.Print_Results()
			# raise Exception("[-] [{Deep.site}] 2 XSS Payloads have been found, time to stop this thread now :)")
			#Deep.CloseProgram()
			Deep.Update_Files()
			if Deep.current_executor != '':
				Deep.current_executor.shutdown()
			Deep.CloseProgram()
			return(Deep.Wpayloads)
		else:
			return(False)
	
	@staticmethod
	def Print_Results():
		result = (Fore.BLUE + Style.BRIGHT +
			"""    
				-	Deep Blue	- 
			""" + Style.RESET_ALL + "     Coded By: "+ Fore.LIGHTRED_EX + Style.BRIGHT + " Youssef Hany (J-0d1N) \n" + Style.RESET_ALL + f""" 
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