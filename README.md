# i0t-pr0be
IoT device search and default credential scanner.

# Requirements
1. Python 3
2. Selenium Python
3. Shodan library + api-key
4. Linux (Tested on Arch & Kali Linux)

# Installation

# Usage Examples
List iot devices tested by the script
``./i0t-pr0be.py -l``

Simple Search
``./i0t-pr0be.py -s -a <api-key>``

Search & save to the third page of the results search.
``./i0t-pr0be.py -s -a <api-key> -n 3``

