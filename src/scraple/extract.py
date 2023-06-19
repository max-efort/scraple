"""
Contain the core API class of scraping and defining rules.
"""
from typing import Union, Optional, Callable, Generator, TypeAlias

from TreeCore import create_Tree, identity_to_branch
from Tree_search_engine import find_identity_by_string, find_parent_identity, parent_elements, Bs
from error import *
from pipeline import text, tags, link

pipelines = {"text": text, "tags": tags, "link": link}
selector: TypeAlias = str


def refine_body(obj, flag):
    obj = open(obj, encoding="utf8") if flag.lower() == 'local' else obj
    try:
        obj = Bs(obj, features="html.parser") if flag.lower() != 'parsed' else obj
        return obj.body if obj.body is not None else obj
    except:
        raise ParsingError(flag)


class RulIn:
    """
    Intermediate object as an interface between Rules and SimpleExtractor class
    """
    def __init__(self, rule):
        self.parent = rule[0]
        self.fields = rule[1]

    def __str__(self):
        return f'Parent Selector:\n\t{self.parent.__str__()}\n' \
               f'Field Rule:\n\t{self.fields.__str__()}\n'


class Rules:
    """
    Define rules of what to extract of a web page. Use this defined rule if you plan to use
    SimpleExtractor class.

    You can retrieve the defined rules selector if you fancy to use it in other scraping method.
    """
    def __init__(
            self,
            reference: Union[Bs, str, bytes],
            page_flag: str
    ):
        """
        :param reference: An object used as reference, either a BeautifulSoup object,
            a string of local path of html file, or a string of html code.
        :param page_flag: Flag of the reference, determine how the reference
            will be preprocessed.

        flag:
            - "parsed": use it for beautifulSoup object.
            - "local" : use it for string of local path.
            - "html"  : use it for byte or string of html code.

        :raise ParsingError: If parsing of reference encounter unexpected error.
        :raise FileNotFoundError: If the reference_flag is "local" and the file was not found.
        """
        self._count = 0
        self._reference = refine_body(reference, page_flag)
        self._tree = create_Tree(self._reference)

        self._fields = {}  # entry_num : ["The field name", "branch_id", pipeline]
        self._parent = None  # the value is a idx (tuple)

    def add_field_rule(
            self,
            string: str,
            field_name: Optional[str] = None,
            re_flag: bool = False,
            climb: int = 0,
            find_string_of_nth: int = 1,
            pipeline: Optional[Union[Callable, str]] = None
    ) -> None:
        """
        Adding a rule to locate an element inside the DOM using string.

        :param string: The string used to locate an element.
        :param field_name: Name to identify the rule name or field name.
        :param re_flag: Flag to use regex in the search.
        :param climb: Number indicating to search for the parent of n-th relative
            to the lowest element containing the string.
        :param find_string_of_nth: Number indicating to find for n-th string.
        :param pipeline: A function object to process the intended elements. The function
            must take 1 argument which is a list of elements. This library provide three
            generic function (in which case you must pass a string name of the function).
            The function in question is "text", "tags" or "link" which in order do the
            following: extract plain text, extract text in the form of tags, extract link.

        :return: None

        :raise SearchError: If the string used to identify an element is not found.
        """
        self._count += 1
        field_name = self._count if field_name is None else field_name

        self._fields[self._count] = [
            field_name,
            find_identity_by_string(
                self._reference,
                string,
                parent_jump=climb,
                string_nth=find_string_of_nth,
                regex=re_flag
            )
        ]
        if pipeline is not None:  # adding pipeline for field
            if isinstance(pipeline, type(text)):
                self._fields[self._count].append(pipeline)
            elif isinstance(pipeline, str):
                pipeline = pipeline.lower()
                self._fields[self._count].append(
                    pipelines[pipeline]) if pipeline in pipelines else self._fields[
                    self._count].append(None)
            else:
                self._fields[self._count].append(None)
        else:
            self._fields[self._count].append(None)

        self._parent = find_parent_identity(self._parent, self._fields[self._count][1])

    def get_extract_rule(self) -> RulIn:
        """
        Get the RulIn object contain the parent selector and a dictionary of
        field selector.

        A RulIn object can be passed to the SimpleExtractor constructor instead
        of the "raw" Rules object.
        """
        parent = identity_to_branch(self._parent, self._tree)
        rule = [parent, {}]
        for key in self._fields:
            full_branch = identity_to_branch(self._fields[key][1], self._tree)

            full_branch = full_branch.split(parent)[1]
            rule[1][self._fields[key][0]] = full_branch, self._fields[key][2]
        return RulIn(rule)

    def get_parent_selector(self) -> selector:
        """Get the CSS selector of the lowest parent element where,
        all the referred element when adding rule, is contained.
        """
        return identity_to_branch(self._parent, self._tree)

    def get_reference_soup(self) -> Bs:
        """Get the beautifulsoup object of the reference page."""
        return self._reference

    def __str__(self):
        return self.get_extract_rule().__str__()


class SimpleExtractor:
    """A class that capable of extracting item from a page based on the rule provided"""
    def __init__(
            self,
            rule: Union[Rules, RulIn]
    ):
        """
        Instantiate the object with its extract rule.

        :param rule: A Rules or RulIn object as rule to extract element from web page.
        """
        rule = rule.get_extract_rule() if isinstance(rule, Rules) else rule
        self.parent = rule.parent
        self.fields = rule.fields

    def perform_extraction(
            self,
            body: Union[Bs, str, bytes],
            page_flag: str,
            iterate_parent_element_instead: bool = False
    ) -> Generator[dict, None, None]:
        """
        Perform  extraction using the rule provided.

        flag:
            - "parsed": use it for beautifulSoup object.
            - "local" : use it for string of local path.
            - "html"  : use it for byte or string of html code.

        :param body: An object of either a BeautifulSoup object,
            a string of local path or a string of html code.
        :param page_flag: Flag of the "body" object, determine how the object
            will be preprocessed.
        :param iterate_parent_element_instead: A flag, if you want to iterate the parent
            element (lowest element where all the CSS selector from the rule met).

        :return: Generator object which iterate dictionary:
            {
                "field name": [element, ...] or object returned by pipeline function
            }.

        :raise ExtractError: If during execution it did not find any element that match
            selector provided from the rule object.
        :raise ParsingError: If parsing of scraping subject encounter unexpected error.
        :raise FileNotFoundError: If the page_flag is "local" and the file was not found.
        """
        body = refine_body(body, page_flag)
        parents = parent_elements(body, self.parent)
        if len(parents) < 1:
            raise ExtractError()
        for item in parents:
            if iterate_parent_element_instead:
                yield item
            else:
                extracted = {}
                for key in self.fields:
                    selector_ = self.fields[key][0]
                    child = item.select(selector_) if selector_ != "" else [item]
                    extracted[key] = child if self.fields[key][1] is None \
                        else self.fields[key][1](child)
                yield extracted
