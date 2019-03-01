import sys
import ctypes

class EricUtility:
    def make_table_crlf(self, cnt):
        res = ""
        if cnt != 0:
            if (cnt % 0x10) == 0:
                res += "\r\n"
            if (cnt % 0x200) == 0:
                res += "\r\n"
        return res

    def make_table_header(self, cnt):
        res = ""
        if (cnt % 0x10) == 0:
            res += format(cnt, '04X') + "| "
        return res

    def make_hex_table(self, dataList):
        str1 = ""
        cnt = 0
        for d in dataList:
            str1 += self.make_table_crlf(cnt)
            str1 += self.make_table_header(cnt)

            str1 += format(d, '02X') + " "
            cnt += 1
        return str1

    def make_ascii_table(self, dataList):
        str1 = ""
        cnt = 0
        for d in dataList:
            str1 += chr(d)
            cnt += 1
            if (cnt % 0x10) == 0:
                str1 += "\r\n"
        return str1

    def to_file(self, path, data):
        with open(path, 'w', -1, 'utf-8') as f:
            f.write(data)

    def to_hex_string(self, value):
        return format(value, '02X')

    def hex_string_to_int(self, value):
        return int(value, 16)

    def is_admin_in_windows(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def set_array_value_be(self, bufList, offset, value):
        bufList[offset+0] = (value >> 0x18) & 0xFF
        bufList[offset+1] = (value >> 0x10) & 0xFF
        bufList[offset+2] = (value >> 0x08) & 0xFF
        bufList[offset+3] = (value >> 0x00) & 0xFF
        return bufList

    def get_array_value_be(self, bufList, offset):
        value = bufList[offset+0] << 24
        value += bufList[offset+1] << 16
        value += bufList[offset+2] << 8
        value += bufList[offset+3]
        return value

    def crlf(self):
        return "\r\n"

    def replace_one_char(self, str, idx, c):
        strList = list(str)
        strList[idx] = c
        return "".join(strList)
        
    def insert_one_char(self, str, idx, c):
        if idx >=0:
            return str[:idx] + c + str[idx:]    
        return ""



        
