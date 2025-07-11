

import urllib.request 
import zstd
import requests

class UrlUtility:

    def make_header(self, cookie = None, userAgent = None):
        header = {}
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'
        if userAgent != None:
            header['User-Agent'] = userAgent

        header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header['Accept-Language'] = 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        header['Accept-Encoding'] = 'gzip, deflate, br, zstd'
        header['Connection'] = 'keep-alive'

        if cookie != None:
            header['Cookie'] = cookie

        header['Sec-Fetch-Dest'] = 'document'
        header['Sec-Fetch-Mode'] = 'navigate'
        header['Sec-Fetch-Site'] = 'none'
        header['Sec-Fetch-User'] = '?1'
        header['Priority'] = ' u=0, i'
        header['TE'] = 'trailers'
        return header
    
    def get_decode_data(self, response, raw_data):
        content_encoding = response.headers.get('Content-Encoding')
        if content_encoding == 'zstd':
            decompressed_data = zstd.decompress(raw_data)
        else:
            decompressed_data = raw_data
        encoding = response.headers.get_content_charset() or 'utf-8'
        data = decompressed_data.decode(encoding, errors='ignore')
        return data

    def get_url_data_by_header(self, url, headers = None):
        req = urllib.request.Request(url, headers=headers, method='GET')
        
        with urllib.request.urlopen(req) as response:
            raw_data = response.read()
            data = self.get_decode_data(response, raw_data)
        return data

    def get_url_data(self, url, cookies = None):
        req = urllib.request.Request(url)

        if cookies != None:
            req.add_header('Cookie', cookies)

        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print(e)
            print(url)
            error_page_content = e.read().decode('utf-8', errors='ignore')
            print(error_page_content)
            return None


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
    
    def get_content_stream_lazy(self, url, headers=None, chunk_size=131072):
        try:
            with requests.get(url, headers=headers, stream=True) as response:
                response.raise_for_status() # 檢查 HTTP 狀態碼
                total_size = int(response.headers.get('content-length', 0))
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk: # 過濾掉空的 chunk
                        yield chunk, total_size
        except requests.exceptions.RequestException as e:
            print(f"下載失敗: {e}")
            yield None, 0