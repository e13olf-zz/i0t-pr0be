# i0t-pr0be
IoT device search and default credential scanner.

# Requirements
1. Python 3
2. Selenium Python
3. Shodan library + api-key
4. Linux (Tested on Arch & Kali Linux)

# Installation
Download the WebDriver for Firefox  
`` wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz``
Exract the binary to /usr/bin



# Usage Examples
List of all iot devices tested by the script.  
``./i0t-pr0be.py -l``

Simple Search  
``./i0t-pr0be.py -s -a <api-key>``

Search & save to the third page of the results search.  
``./i0t-pr0be.py -s -a <api-key> -n 3``

