# Scraple Documentation
## 1. Introduction
Scraple is designed to simplify the tedious task of manually picking selectors 
from web pages. In addition to that, it also offers a convenient solution for 
extracting information from web pages by providing a defined rule.

At the core of the engine, Scraple utilizes the power of beautifulsoup4, a popular 
Python library for parsing HTML and XML documents. By leveraging the capabilities 
of beautifulsoup4 coupled with custom implementation of tree structure of DOM, this 
library offer higher level interface for writing web scraping code.

In summary, Scraple offers a comprehensive solution for simplifying web scraping 
tasks makes it a good substitute tool for scraping.

## 2. Installation
Install scraple from Pypi using pip:
```shell
pip install scraple
```

## 3. Tutorial
For this tutorial, file example of web page used is "Modified Quotes to Scrape.html" 
provided in the code_example directory. It is a modified version from 
pages of [quotes.toscrape.com](https://quotes.toscrape.com).

Before showcasing the capability of this library, you need to know two main feature
provided in this library, that two main features is provided in the form of classes. 
More info for this is in the API section

### 3.1. Rules
The first one is the Rules class, which allows users to define rules for extracting 
elements from a web page. With the Rules class, you can pick selector just by knowing
what string present in that page using the `add_field_rule` method. This method 
automatically searches for selector of element which text content match the string. 
Additionally, the method supports regular expression matching.

```python
from scraple import Rules, SimpleExtractor
# to displaying the end result in tabular manner we use pandas
from pandas import concat, DataFrame as Df

# suppose we want to scrap just the Quote
quote_rule = Rules(r"Modified Quotes to Scrape.html", "local")
quote_rule.add_field_rule(
    "It is our choices, Harry, that show what we truly are, far more than our abilities.",
    "Quotes",
)
print(quote_rule)
# >>>
# Parent Selector:
# 	div.container div.row div.col-md-8 div.quote span.text,
# Field Rule:
# 	{'Quotes': ('', None)}

# create DataFrame object to accumulate the iterated item
result_panda = Df()

# scrape using SimpleExtractor, for now we just gonna scrape the reference page
extract = SimpleExtractor(quote_rule)
extracting = extract.perform_extraction(r"Modified Quotes to Scrape.html", "local")

for index, dictionary in enumerate(extracting, 1):  # iterate dictionary of scraping result
    result_panda = concat([result_panda, Df(dictionary, index=[index])])

print(result_panda)
# >>>
#                                              Quotes
# 1  [“The world as we have created it is a process...
# 2  [“It is our choices, Harry, that show what we ...
# 3  [“The person, be it gentleman or lady, who has...
# 4  [“Try not to become a man of success. Rather b...
```

### 3.2. SimpleExtractor
The second main feature is the SimpleExtractor class. This class performs the actual 
scraping based on the defined rules. 

To use it, you provide a Rules object that act as "answer to: which one to get?" 
to the SimpleExtractor constructor. Then, 
you can call the `perform_extraction` method to "get" the element (scraping) by providing 
the page you want to extract and create a generator object. 

The generator iterates over dictionaries containing the extracted element or 
any object returned by the pipeline function provided 
when defining rules.


Let's see an example of extracting Quote, Author and Tags from the example page.
```python
from scraple import Rules, SimpleExtractor
# to displaying the end result in tabular manner we use panda
from pandas import concat, DataFrame as Df

rules = Rules(r"Modified Quotes to Scrape.html", "local")
# To make defining rule more easier we iterate list of defined field name, string identifier and
# additionally finding the string of n-th and we will provide pipeline to process the extracted
# element internally.
#
# If there is confusing piece of code, there is more info in the API section.

field_name = [
    "Quote",
    "Author",
    "Tags"
]
# Using part of the string in this case is valid because all the string contained in a
# single element which selector we want to pick.
string_identifier = [
    "It cannot be changed",   
    "Einstein",
    "change"
]
find_string_of_nth = [
    1,
    1,
    2  # note that if you look at the page element, the string "change" occurred in the Quote string 
       # first so we need to find the 2nd for the element that contain the tag.
]
processor_function = [
    "text",
    "text",
    "tags"
]

change_iterate_queue = [1, 2, 0]  # to show the Author first and Quote last in the columned data
for i in change_iterate_queue:
    rules.add_field_rule(
        string=string_identifier[i],
        field_name=field_name[i],
        find_string_of_nth=find_string_of_nth[i],
        pipeline=processor_function[i]
    )
print(rules)
# >>>
# Parent Selector:
# 	div.container div.row div.col-md-8 div.quote,
# Field Rule:
# 	{'Author': (' span small.author', <function text at 0x0000017CB4FA9A20>), 'Tags': (' div.tags...


# Scraping using SimpleExtractor class.
extract = SimpleExtractor(rules)

# For this tutorial, we will just use the reference page as the source
# In the previous example we use:
# extracting = extract.perform_extraction(r"Modified Quotes to Scrape.html", "local")
# Rules class provide a methode that retrieve beautifulsoup object of the reference, so we can also use:
extracting = extract.perform_extraction(rules.get_reference_soup(), "parsed")

# create DataFrame object to accumulate the iterated item
result_panda = Df()

for index, dictionary in enumerate(extracting, 1):  # iterate dictionary of scraping result
    # because one of value inside the "item" is an array (a list, product of the "tags" pipeline function),
    # we convert it to string so the DataFrame treated it as one (scalar) value.
    dictionary["Tags"] = ", ".join(dictionary["Tags"])
    result_panda = concat([result_panda, Df(dictionary, index=[index])])

print(result_panda)
# >>>
#             Author  ...                                              Quote
# 1  Albert Einstein  ...  “The world as we have created it is a process ...
# 2                   ...  “It is our choices, Harry, that show what we t...
# 3      Jane Austen  ...  “The person, be it gentleman or lady, who has ...
# 4  Albert Einstein  ...  “Try not to become a man of success. Rather be...

# [4 rows x 3 columns]
```
By iterating over the generator object, you can retrieve the desired data in a 
structured manner.
For each iteration, the SimpleExtractor returns a dictionary where the keys 
correspond to the field names defined in the Rules object and the values is 
the extracted
element (or object based on product of the provided pipeline function). 

This approach deal pretty well for parent element that missing some field as what 
shown on entry
number 2 on above example (the parent element missing the Author field).

## 4. Main Classes API
### 4.1. Rules
```python
from scraple import Rules
rules = Rules("reference.html", "local")
```
To instantiate a Rules object you need to pass two argument, reference and flag. List of
flag corresponding to its object type of reference are:
- "parsed" : for beautifulsoup object.
- "local" : for string path of local html file.
- "html" : for byte or string of html code.

##### 4.1.1 `add_field_rule` Method
Use this methode to define rule. It takes six parameters, which, one are mandatory and 
the other 5 is optional:
- **_string_**: The string used to locate an element. Mind the case sensitivity of the string. 
- **_field_name_**: Name to identify the rule name or field name, default to `None` (use the
  entry number if not specified).
- **_re_flag_**: Flag to use regex in the search, default to `False`
- **_climb_**: Number indicating to search for the parent element of n-th relative
            to the lowest element containing the string, default to `0`
- **_find_string_of_nth_**: Number indicating to find for n-th string, default to `1`
- **_pipeline_**: A function object to process the intended elements. The function
            must take 1 argument which is a list of elements. This library provide three
            generic function (in which case you must pass a string name of the function).
            The function in question is "text", "tags" or "link" which in order do the
            following: extract plain text, extract text in the form of tags, extract link. 
Default to `None`

If you define multiple rule in a one Rules object, 
the _method_ compute and determine the parent element of them (where their selector met). 
If you do these, all the rule definition must be "_relevant_" to each other. 

"_Relevant_" in this context mean, in some sense that they share similar pattern. 
For example, if you define 
**Pager** (page navigation) rule in Rules object that contain rules for 
**Author**, **Quote** and **Tags**, you will only get 1 parent selector 
that match this definition instead of the intended 4 (It does not rhyme and 
does not make any sense).
```python
# continuation from the previous example of extraction
rules.add_field_rule(
    string="Next",
    field_name="Pager",
    pipeline="link"
)

extract = SimpleExtractor(rules)
extracting = extract.perform_extraction(rules.get_reference_soup(), "parsed")

result_panda = Df()

for index, dictionary in enumerate(extracting, 1):
    dictionary["Tags"] = ", ".join(dictionary["Tags"])
    result_panda = concat([result_panda, Df(dictionary, index=[index])])

print(result_panda)
#                                         Author  ...                                Pager
# 1  Albert Einstein Jane Austen Albert Einstein  ...  https://quotes.toscrape.com/page/2/
#
# [1 rows x 4 columns]
```
**So, should I define just one rule per Rules?**

No, there is a benefit in defining multiple rule
in one Rules object as the example has shown. Its deal for parent element 
that has missing field element which in the example case, missing Author field. 
If you use one rule per Rules,
for a large scraping, you will only know the fact that some extracted value is missing.

**Another Note when defining rules:**

- To ensure a more precise rule definition like what intended, it is not hurt to inspect
the element of the page in your browser. 
- Sometimes some string that need to be 
found embed in an element that is not shown in the displayed page, if so you need to 
adjust the `find_string_of_nth` argument accordingly.
- It is fine to just using part of the whole sentence to find the selector we want
if the whole part contained in a single element otherwise it is recommended to include 
all the text.
- The `pipeline` argument will be explained more in section 5.

##### 4.1.2 `get_parent_selector` Method
Use this method to retrieve the selector of the parent element if you define multiple rule,
or if you just define one rule it will retrieve that single selector.
```python
navigation_rules = Rules(r"Modified Quotes to Scrape.html", "local")
navigation_rules.add_field_rule(
    string="Next",
    field_name="Navigation",
    pipeline="link"
)
nav_selector = navigation_rules.get_parent_selector()
print(nav_selector)
# >>> div.container div.row div.col-md-8 nav ul.pager li.next a

scrap_page = rules.get_reference_soup()
next_link_dict = next(SimpleExtractor(navigation_rules).perform_extraction(scrap_page, "parsed"))
print(next_link_dict["Navigation"])
# >>> https://quotes.toscrape.com/page/2/
```

##### 4.1.3 `get_reference_soup` Method
This methode retrieve the _beautifulsoup_ object of the _reference_ page used to
instantiate Rules object (as you can see in the above example).

##### 4.1.4 `get_extract_rule` Method
This methode return a RulIn object, an instance of the RulIn class which act as a bridge
(an intermediate) between Rules object and SimpleExtractor object. 

You can use the value as rules to be used directly in SimpleExtractor,
in fact SimpleExtractor constructor perform `Rules.get_extract_rule()` to retrieve
the final rules used for scraping if you pass Rules object to the constructor.

You also can access the parent selector and fields selector.

### 4.2. SimpleExtractor
This class only task is just doing extraction, and "which to extract" logic is provided by 
the Rules object.
To instantiate a SimpleExtractor object, you need to provide a rule as the argument.
rule can be either Rules or RulIn object.
The only methode of this class is `perform_extraction` which the method to call to perform
the extraction and return a Generator object.

The generator iterates dictionaries, where the keys correspond to the field names defined 
in the rules and the values is the extracted object.

The extracted object can be either of two type, an element if 
**no** pipeline function provided or
an object courtesy of product by the provided pipeline function.

The `perform_extraction` method takes three argument,
- **body**: An object of either a BeautifulSoup object, a string of local path or a string of html code.
- **page_flag**: Flag of the "body" object, determine how the object
            will be preprocessed.
- **iterate_parent_element_instead**: A flag, if you want to iterate the parent
            element instead of dictionary, default to `False`.

Flag corresponding to its object type of reference are:
- "parsed" : for beautifulSoup object.
- "local" : for string path of local html file.
- "html" : for byte or string of html code.

## 5. Other Info
### 5.1. Exception
There is three custom Exception class bundled with this library.

##### 5.1.1 `SearchError` Class
This exception is raised when the specified string used when defining rule is not found.
The method which would raise this exception is `Rules.add_field_rule()`.

Some known cause is the DOM contain some dummy string and argument for `string_nth` 
exceed the
number of the searched string present in the DOM. A DOM with too complicated structure
may be parsed improperly by beautifulsoup leading to this exception.

##### 5.1.2 `ParsingError` Class
This exception is raised when execution that involve parsing encountered an unexpected 
behavior. The `SimpleExtractor.perform_extraction()` may raise this exception and an 
initialization of Rules() object may to.

Some known cause is there is typo in _flag_ passed.

##### 5.1.3 `ExtractError` Class
This exception is raised when there is unexpected behavior during scraping.
The method which would raise this exception is `SimpleExtractor.perform_extraction()`.

### 5.2. Other Error
Other error that might be encountered is associated if you pass _"local"_ as `page_flag`.
Internally builtin `open()` used to open a local file, so it might raise `FileNotFoundError` and
`TypeError`.

### 5.3. Pipeline Processor
_Pipeline Processor_ refer to a function that passed to `pipeline` parameter when defining
rules. It used to process the elements extracted internally. This library provide three
generic function for this:
- `text`
A function to process the extracted elements and produced result in the form of text.
- `tags`
A function that have the same functionality as `text` but return accumulated text 
in the form of `list` object.
- `link`
A function that retrieve a link (`href` attribute) out of an element.

To use this generic function, you just need to pass the name of the function (string)
when defining a rule instead as _callable_ object by manually importing it.

If you want to make your own, it has to take 1 argument and this argument is a list of element.
If you don't pass any function when defining rule, you can always process the extracted 
element later. 
