"""
Contain simple function as pipeline processor to process an element extracted
"""
from typing import Iterable, TypeAlias
List_of_Elements: TypeAlias = Iterable


def text(elements: List_of_Elements):
    strings = None
    for element in elements:
        strings = element.text.strip() if strings is None else strings + " " + element.text.strip()
    return strings


def tags(elements: List_of_Elements, return_str=False):
    tag = [element.text.strip() for element in elements]
    return ", ".join(tag) if return_str else tag


def link(elements: List_of_Elements):
    for element in elements:
        link_ = element.get('href')
        if link_ is not None:
            return link_
