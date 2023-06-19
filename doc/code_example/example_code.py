from scraple import Rules, SimpleExtractor
# to displaying the end result in tabular manner we use pandas
from pandas import concat, DataFrame as Df
# ----------------------------------------------------------------------------------------------------------------------
# End Section
# ----------------------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------------------
# End Section
print("# --------------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------------------------------

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
# ----------------------------------------------------------------------------------------------------------------------
# End Section
print("# --------------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------
# End Section
print("# --------------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------------------------------

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
# ----------------------------------------------------------------------------------------------------------------------
# End Section
print("# --------------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------------------------------
