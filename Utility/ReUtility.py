
import re


class ReUtility:
    def re(self, pattern, data):
        return re.findall(pattern, data)
    def searchPattern(self, stringData, pattern):
        return re.search(pattern, stringData)

    def between(self, data, startPattern, endPattern):
        startIdx = data.find(startPattern)
        data = data[startIdx:]
        endIdx = data.find(endPattern)
        data = data[:endIdx]
        return data