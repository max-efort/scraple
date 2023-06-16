# Scraple

Scraple is a Python library designed to simplify the process of web scraping, 
providing easy scraping and easy searching for selectors.

## Installation
[Pypi page](https://pypi.org/project/scraple/)

You can install the package using pip:

```shell
pip install scraple
```

## Main API
The package provides two main classes: Rules and SimpleExtractor.

#### 1. Rules
The Rules class allows you to define rules for extracting elements from a web page. 
You can add field rules using the add_field_rule method, which has the capability to 
automatically pick selectors based on a provided string. Also, support for regex 
matching.

```python
from scraple import Rules

some_rules = Rules("reference in the form of beautifulSoup4 object, html code or string path to local html file")
some_rules.add_field_rule("a sentence or word exist in reference page", "field name 1")
some_rules.add_field_rule("some othe.*?sentences", "field name 2", re_flag=True)
# Add more field rules...

# It automatically search for the selector, to see it you can see the rule in console
# or by printing it
# print(rules)
```

#### 2. SimpleExtractor
The SimpleExtractor class performs the actual scraping based on the defined rules. 
You provide the Rules object to the SimpleExtractor constructor and use the 
perform_extraction method to create a generator object that iterate dictionary of
element or text information.

```python
from scraple import SimpleExtractor

extractor = SimpleExtractor(some_rules)
result = extractor.rule(
    "web page object in the form of beautifulSoup4 object, html code or string path to local html file")

# print(next(result))
# {"field name 1": element or text information (if you provide pipeline func.),
# print(next(result))
#  "field name 2": ..., ...}
```
For more detail, see the [repository](https://github.com/max-efort/scraple) 
