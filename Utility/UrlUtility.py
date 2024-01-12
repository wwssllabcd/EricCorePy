

import urllib.request 


class UrlUtility:
    def get_url_data(self, url, cookies = None):
        req = urllib.request.Request(url)

        if cookies != None:
            req.add_header('Cookie', cookies)

        response = urllib.request.urlopen(req)

        # check is redirect or not?
        if response.url != url:
            return self.get_url_data(response.url, cookies)


        encoding = response.headers.get_content_charset() 
        bytecode = response.read()
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