
import sys

class EricUtility:
    def make_hex_table(self, dataList):
        str1 = ""
        cnt=0
        for d in dataList:
            if (cnt%0x10) == 0:
                str1 +=  format(cnt, '04X') + "| "

            str1 += format(d, '02X') + " "
            cnt+=1

            if (cnt%0x10) == 0:
                str1 += "\r\n"
                
                
        return str1