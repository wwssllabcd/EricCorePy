
import re


class ReUtility:
    def re(self, pattern, data):
        return re.findall(pattern, data)