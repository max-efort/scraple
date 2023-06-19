# Scraple

Scraple is a Python library designed to simplify the process of web scraping, 
providing easy scraping and easy searching for selectors.

## Installation
The package is hosted in [Pypi](https://pypi.org/project/scraple/) and can be 
installed using pip:

```shell
pip install scraple
```

## Main API
The package provides two main classes: Rules and SimpleExtractor.

#### 1. Rules
The Rules class allows you to define rules of extraction. 
You can pick selector just by knowing what string present in that page using the `add_field_rule` method. 
This method automatically searches for selector of element which text content match the string. 
Additionally, the `add_field_rule` method supports regular expression matching.

```python
from scraple import Rules

#To instantiate Rules object you need to have the reference page.
some_rules = Rules("reference in the form of string path to local html file", "local")
some_rules.add_field_rule("a sentence or word exist in reference page", "field name 1")
some_rules.add_field_rule("some othe.*?text", "field name 2", re_flag=True)
# Add more field rules...

# It automatically search for the selector, to see it you can see the rule in console
# or by printing it
# print(rules)
```

#### 2. SimpleExtractor
The SimpleExtractor class performs the actual scraping based on a defined rule.
A Rules object act as the "which to extract" and the SimpleExtractor do the "extract" or 
scraping. First, pass a Rules object
to SimpleExtractor constructor and use the 
`perform_extraction` method to create a generator object that iterate dictionary of
elements extracted.

```python
from scraple import SimpleExtractor

extractor = SimpleExtractor(some_rules)  # some_rules from above code snippet
result = extractor.perform_extraction(
    "web page in the form of beautifulSoup4 object",
    "parsed"
)

# print(next(result))
# {
#   "field name 1": [element, ...],
#   "field name 2": ...,
#   ...
# }
```
For more information and tutorial, see the [documentation](https://github.com/max-efort/scraple/doc) or 
visit the main [repository](https://github.com/max-efort/scraple)
