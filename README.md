# i0t-pr0be
IoT device search via Shodan and default credential scanner. 

More information about development and the libraries used: https://www.e13olf.me/2019/11/i0t-pr0be-iot-device-search-default.html  

# Requirements
1. Python 3
2. Selenium Python Libary
3. Shodan Library
4. Linux (Tested on Arch & Kali Linux)

# Installation
Download WebDriver from https://github.com/mozilla/geckodriver/releases depending on Linux architecture then extract the file to the /usr/bin/ directory.  
``git clone https://github.com/e13olf/i0t-pr0be.git``  
``pip3 install -r requirements.txt``  

# Usage Examples  
```usage: i0t-pr0be.py [-h] [-a APIKEY] [-p PAGES] [-l] [-s SHODANSEARCH] [-v] [-t TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -a APIKEY, --apikey APIKEY
                        Your api key.
  -p PAGES, --pages PAGES
                        Number of pages deep to go into Shodan page_results with 100 results per page; default is 1.
  -l, --list            List the number of IoT device types tested by the script.
  -s SHODANSEARCH, --shodansearch SHODANSEARCH
                        Your Shodan search query. Use quotes when using filters.
  -v, --verbose         Output verbose statements.
  -t TIMEOUT, --timeout TIMEOUT
                        Set timeout value for each request; default is 13

Usage example: Search Shodan for "Hikvision Cameras" using your API key.
./i0t-pr0be.py -s "DNVRS-Webs" -a abcdefghijklmnopqrstuvwxyz123456  
Search & save results of the first three pages with default as 100 results per page.  
./i0t-pr0be.py -s -a <api-key> -p 3 

