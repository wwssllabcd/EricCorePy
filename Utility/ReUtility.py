
import re


class ReUtility:
    def re(self, str):
        prog = re.compile("<td>")
        result = prog.match(str)
        return result