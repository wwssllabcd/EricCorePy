

import urllib.request


class UrlUtility:
    def get_url_data(self, url):
        req = urllib.request.urlopen(url)
        encoding = req.headers.get_content_charset() 
        bytecode = req.read()
        data = bytecode.decode(encoding, errors='ignore')
        return data

    def set_utf8(self, data):
        str = "charset="
        endstr = " "
        startIdx = data.find(str)
        endIdx = data.find(endstr, startIdx, len(data))
        replace = data[startIdx:endIdx]
        str.replace(replace, "charset=UTF-8")
        return data