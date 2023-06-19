flags = "parsed", "local", "html"


class ParsingError(Exception):
    def __init__(self, flag: str):
        message = f"Can't parse the passed object. Make sure you pass " \
                  f"the right argument with the right flag {flags.__str__()}, " \
                  f"the flag you passed was '{flag}'."
        super().__init__(message)


class SearchError(Exception):
    def __init__(self, string: str, nth: int):
        rank_msg = ""
        msg2 = " "
        msg3 = "."
        if nth > 1:
            rank_msg = f"the {nth}-th string of"
            msg2 = ", "
            msg3 = f", or {rank_msg} '{string}' does not exist."

        message = f"Can't find {rank_msg} '{string}' in the object, " \
                  f"either there is dummy text present{msg2}or the DOM is " \
                  f"too sophisticated to parse{msg3}"
        super().__init__(message)


class ExtractError(Exception):
    def __init__(self):
        msg = "There is no element match that match the selector provided from the rule, " \
              "either the DOM change by sophisticated anti-scrap method or you provide an " \
              "incompatible web page with the rule."
        super().__init__(msg)
