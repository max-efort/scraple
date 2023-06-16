flags = "parsed", "local", "html"


class ParsingError(Exception):
    def __init__(self):
        message = f"Can't parse the passed reference. Make sure you pass " \
                  f"the right argument with the right flag {flags.__str__()}."
        super().__init__(message)


class SearchError(Exception):
    def __init__(self, string: str, nth: int):
        rank_msg = "the"
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
        msg = "There is no element with selector provided from the rule, either " \
              "the DOM change or you provide an object with body which is not " \
              "compatible with the rule provided."
        super().__init__(msg)
