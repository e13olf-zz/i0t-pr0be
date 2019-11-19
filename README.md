# i0t-pr0be
IoT device search via Shodan and default credential scanner. 

More information about development and the libraries used: https://e13olf.me

# Requirements
1. Python 3
2. Selenium Python Libary
3. Shodan Library
4. Linux (Tested on Arch & Kali Linux)

# Installation
Download WebDriver from https://github.com/mozilla/geckodriver/releases depending on Linux architecture then extract and copy the file to the /usr/bin/ directory.  
``git clone https://github.com/e13olf/i0t-pr0be.git``  
``pip3 install -r requirements.txt``  

# Usage Examples
List of all iot devices tested by the script.  
``./i0t-pr0be.py -l``

Simple Shodan search and save  
``./i0t-pr0be.py -s -a <api-key>``

Search & save results of the first three pages with default as 100 results per page.  
``./i0t-pr0be.py -s -a <api-key> -p 3``

