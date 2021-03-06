import sys
import ctypes
import shutil  # file move
from os import listdir
from os.path import isfile, join
from os import walk
from pathlib import Path

class FileObj:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.isFile = True

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
        
    def insert_one_char(self, str, targetIdx, c):
        if targetIdx >=0:
            return str[:targetIdx] + c + str[targetIdx:]    
        return ""

    def to_file(self, path, data):
        with open(path, 'w', -1, 'utf-8') as f:
            f.write(data)

    def is_file_exist(self, path):
        file = Path(path)
        return file.exists()

    def make_folder(self, path):
        file = Path(path)
        if file.is_dir() == False:
            file.mkdir(parents=True, exist_ok=True)

    def get_file_data(self, path):
        file = Path(path)
        if self.is_file_exist(path) == False:
            return None
        if file.is_dir():
            return None
        data = file.read_text(encoding = 'utf8')
        return data

    def get_file_size(self, path):
        p = Path(path)
        return p.stat().st_size

    def get_file_colls(self, folderPath):
        onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
        return onlyfiles

    def get_fileObj_colls(self, folderPath):
        fColls = []
        files = listdir(folderPath)

        for f in files:
            fullpath = join(folderPath, f)
            fo = FileObj()
            fo.name = f
            fo.isFile = isfile(fullpath)
            fo.size = self.get_file_size(fullpath)
            fColls.append(fo)
        return fColls

    def move_file(self, src, dsc):
        shutil.move(src, dsc)

    def get_file_data_binary(self, filePath, len=0):
        f = open(filePath, "rb") # b is important -> binary, return class 'bytes'
        if len == 0:
        	return f.read()
        return f.read(len)
        
    def get_file_list_by_size(self, fileColls):
        dupFileColls = {}
        for file in fileColls:
            if file.size not in dupFileColls:
                if file.size ==  0:
                    continue
                dupFileColls[file.size] = []
            dupFileColls[file.size].append(file.name)
        return dupFileColls

    def get_duplicate_file_list_by_compare_file_data(self, folderPath):
        fileColls = self.get_fileObj_colls(folderPath)
        fileColls.sort(key=lambda x: x.size)
        dupFileColls = self.get_file_list_by_size(fileColls)
        dupFileList = []
        compareSize = 512*1024
        for item in dupFileColls:
            fileList = dupFileColls[item]
            if len(fileList) > 1:
                cnt=0
                firstData = ''
                for f in fileList:
                    if cnt == 0:
                        firstData = self.get_file_data_binary(folderPath + f, compareSize)
                        cnt+=1
                    else:
                        data = self.get_file_data_binary(folderPath + f, compareSize)
                        if data == firstData:
                            dupFileList.append(f)
        return dupFileList