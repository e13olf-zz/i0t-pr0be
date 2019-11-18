# i0t-pr0be
IoT device search and default credential scanner. 

More information about development and the libraries used: https://e13olf.me

# Requirements
1. Python 3
2. Selenium Python
3. Shodan library + api-key
4. Linux (Tested on Arch & Kali Linux)

# Installation
Download the WebDriver for Firefox for your linux architecture  
``https://github.com/mozilla/geckodriver/releases``  

Exract the binary and copy it to /usr/bin/  

``git clone ``  
``pip3 install -r requirements.txt``  

# Usage Examples
List of all iot devices tested by the script.  
``./i0t-pr0be.py -l``

Simple Search  
``./i0t-pr0be.py -s -a <api-key>``

Search & save to the third page of the results search.  
``./i0t-pr0be.py -s -a <api-key> -n 3``

