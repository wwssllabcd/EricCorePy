import sys


class EricUtility:
    def make_hex_table(self, dataList):
        str1 = ""
        cnt = 0
        for d in dataList:
            if (cnt % 0x10) == 0:
                str1 += format(cnt, '04X') + "| "

            str1 += format(d, '02X') + " "
            cnt += 1

            if (cnt % 0x10) == 0:
                str1 += "\r\n"
        return str1

    def to_file(self, path, data):
        with open(path, 'w', -1, 'utf-8') as f:
            f.write(data)

    def to_hex_string(self, value):
        return format(value, '02X')
