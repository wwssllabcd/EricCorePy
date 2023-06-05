

import urllib.request 


class UrlUtility:
    def get_url_data(self, url):
        #header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'}
   
        req = urllib.request.Request(url)
        #req.add_header('user-agent','Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
        req.add_header('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0')

        req = urllib.request.urlopen(url)

        if req.url != url:
           return self.get_url_data(req.url)
            

        print(req.url)
        print(req.status)
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