"""
Contain simple generic function as pipeline to process elements extracted.

The library utilize mostly beautifulsoup.select() method to retrieve elements which is why all the
function in this module take a list of element object. You shall abide to this rule if you want to
pass custom pipeline processor when defining Rules.
"""
from typing import Union, TypeAlias
List_of_Elements: TypeAlias = list


def text(elements: List_of_Elements) -> str:
    strings = " ".join([element.text.strip() for element in elements]) if len(elements) > 0 else ""
    return strings


def tags(elements: List_of_Elements, return_str=False) -> Union[str, list]:
    tag = ""
    if len(elements) > 0:
        tag = [element.text.strip() for element in elements]
        tag = ", ".join(tag) if return_str else tag
    return tag


def link(elements: List_of_Elements) -> str:
    for element in elements:
        link_ = element.get('href')
        if link_ is not None:
            return link_
    return ""
