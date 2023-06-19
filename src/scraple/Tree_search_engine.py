"""
Contain the core function to traverse the "custom tree structure".
"""
from bs4 import BeautifulSoup as Bs

from typing import Sequence
from re import search

from TreeCore import appender, identity_to_branch
from error import SearchError


def find_identity_by_string(body, string, string_nth, parent_jump, regex=False):
    string_nth = [1] if string_nth < 1 else [string_nth]
    parent_jump = 0 if parent_jump < 0 else parent_jump
    identity = search_string(body, string, string_nth, regex=regex)
    if identity is None:
        raise SearchError(string, string_nth[0])
    else:
        identity = tuple(identity)
        return identity if parent_jump == 0 else identity[:-parent_jump]


def search_string(body, string, attempt_remain, regex=False, level=0, id_f=None, idf_temp=None,
                  level_where_attempt_success=None,
                  end_search=None):
    if level == 0:
        id_f = [None]
        idf_temp = []
        level_where_attempt_success = [None]
        end_search = [False]
    count = 1
    for element in body:
        if element.name is not None:
            appender(count, idf_temp)
            count += 1
            condition_met = search(string, element.text) if regex else string in element.text
            if condition_met:
                id_f[0] = idf_temp
                level_where_attempt_success[0] = level + 1
            search_string(element, string, attempt_remain, regex, level + 1, id_f, idf_temp.copy(),
                          level_where_attempt_success, end_search)
            if end_search[0]:
                break
    if level_where_attempt_success[0] is not None:
        if level_where_attempt_success[0] == level:
            attempt_remain[0] -= 1
            if attempt_remain[0] <= 0:
                end_search[0] = True
            else:
                id_f[0] = None
            level_where_attempt_success[0] = None
    if level == 0:
        return id_f[0]


def find_parent_identity(existing, added_idx):
    if existing is None:
        return added_idx
    parent_temp = []
    zip_ = zip(existing, added_idx)
    for p, a in zip_:
        if p == a:
            parent_temp.append(p)
        else:
            break
    return tuple(parent_temp)


def parent_elements(soup: Bs, node) -> Sequence:
    return soup.select(node)


def find_follow_path(body, identity, tree):
    path = None
    id_cutter = 0
    cutter_limit = int(len(identity) / 2)
    while path is None and len(identity) >= cutter_limit:
        identity = identity[:-id_cutter] if id_cutter > 0 else identity
        branch = identity_to_branch(identity, tree)
        elements = body.select(branch)
        if len(elements) > 0:
            element = elements[0]
            href = element.find(has_href)
            if href is not None:
                path = href['href']
                break
        else:
            id_cutter += 1

    return path


def has_href(element):
    return element.has_attr('href')
