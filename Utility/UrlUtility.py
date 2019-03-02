

import urllib.request


class UrlUtility:
    def get_url_data(self, url):
        req = urllib.request.urlopen(url)
        encoding = req.headers.get_content_charset() 
        print(encoding)
        bytecode = req.read()
        data = bytecode.decode(encoding, errors='ignore')
        return data