"""
=============================
scraple - Simple Scraping Library
=============================

Scraple is a Python library designed to simplify the process of web scraping.
This library provide easy searching for selectors and easy scraping.

Overview
---------

Scraple provides a simple way to extract data from web pages by defining simple rules
for extraction. It also offers a convenient mechanism for automatically finding
selectors using only string present in the page.

Main Features
---------
- **SimpleExtractor**: A class that enables rule-based extraction of data from web pages,
  making the actual scraping easy.

- **Rules**: A class that allows the automatic discovery of selectors using string.
  It simplifies the process of defining and applying extraction rules.

Exception
--------------
Scraple includes the following error classes:

- **ParsingError**: Raised when an unexpected error occurs during page parsing.
- **SearchError**: Raised when an unexpected error occurs while searching
  for a string in a page.
- **ExtractError**: Raised when an unexpected error occurs during data extraction
  from a page.

Dependencies
------------
- **beautifulsoup4** (version 4.x.x): A library for parsing HTML and XML documents.


For more information visit https://github.com/max-efort/.

"""

from extract import SimpleExtractor, Rules
from error import *
