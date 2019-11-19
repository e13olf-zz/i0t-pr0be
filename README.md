# i0t-pr0be
IoT device search via Shodan and default credential scanner. 

More information about development and the libraries used: https://e13olf.me

# Requirements
1. Python 3
2. Selenium Python
3. Shodan library + api-key
4. Linux (Tested on Arch & Kali Linux)

# Installation
Download WebDriver for Firefox for your linux architecture  
``https://github.com/mozilla/geckodriver/releases``  

Exract binary and copy it to /usr/bin/  

``git clone https://github.com/e13olf/i0t-pr0be.git``  
``pip3 install -r requirements.txt``  

# Usage Examples
List of all iot devices tested by the script.  
``./i0t-pr0be.py -l``

Simple Shodan search  
``./i0t-pr0be.py -s -a <api-key>``

Search & save results of the first three pages with default as 100 results per page.  
``./i0t-pr0be.py -s -a <api-key> -p 3``

