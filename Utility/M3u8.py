
m_crlf = "\n"

class M3u8:
    def get_m3u8_head_string(self):
        return "#EXTM3U" + m_crlf

    def get_m3u8_item_string(self, title, url):
        res = '#EXTINF:-1  group-title="liveNews" tvg-logo="N/A", ' + title + m_crlf
        res += url + m_crlf
        return res
