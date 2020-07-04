
import re


class ReUtility:
    def get_re(self):
        return re

    def findall(self, pattern, data):
        return re.findall(pattern, data)
    def searchPattern(self, stringData, pattern):
        return re.search(pattern, stringData)

    def between(self, data, startPattern, endPattern):
        startIdx = data.find(startPattern)
        data = data[startIdx:]
        endIdx = data.find(endPattern)
        data = data[:endIdx]
        return data

    def get_between_string(self, data, targetPattern, startPattern, endPattern):
        data = data.lower()
        targetIdx = data.find(targetPattern)
        endIdx = data.find(endPattern, targetIdx)
        frontIdx = data.rfind(startPattern, 0, targetIdx)

        data = data[frontIdx:endIdx]
        return data

    def remove_html_tag(self, data):
        rule = re.compile(r'<[^>]+>', re.S)
        res = rule.sub('', data)
        return res

    
    