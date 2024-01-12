import sys
import ctypes
import shutil  # file move
from os import listdir
from os.path import isfile, join
from os import walk
from pathlib import Path
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

CRLF = "\r\n"
NULL_32 = 0xFFFFFFFF


m_logger = None

def eprint(*args, **kwargs):
    print(*args, **kwargs)
    if m_logger != None:
        m_logger.debug(*args, **kwargs)

def init_logger(fileName):
    u = EricUtility()
    u.make_folder("./log")
    fileName = "log/log-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"

    global m_logger
    m_logger = logging.getLogger("mylog")
    m_logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(fileName, maxBytes=10*1024*1024, backupCount=10000)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    m_logger.addHandler(handler)



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
                res += CRLF
            if (cnt % 0x200) == 0:
                res += CRLF
        return res

    def make_table_header(self, cnt):
        res = ""
        if (cnt % 0x10) == 0:
            res += format(cnt, '04X') + "| "
        return res

    def make_hex_table(self, dataList, maxCnt=0):
        str1 = ""
        cnt = 0
        for d in dataList:
            str1 += self.make_table_crlf(cnt)
            str1 += self.make_table_header(cnt)

            str1 += format(d, '02X') + " "
            cnt += 1
            if(cnt == maxCnt):
                break
        return str1

    def make_ascii_table(self, dataList, maxCnt=0):
        str1 = ""
        cnt = 0
        for d in dataList:
            str1 += chr(d)
            cnt += 1
            if (cnt % 0x10) == 0:
                str1 += CRLF

            if(cnt == maxCnt):
                break
        return str1


    def to_hex_string(self, value):
        return format(value, '02X')

    def hex_string_to_int(self, value):
        return int(value, 16)

    def to_int(self, string):
        if string[:2] == "0x":
            return int(string, 16)
        return int(string)

    def is_admin_in_windows(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            return False

    def set_array_value_le(self, bufList, offset, value):
        bufList[offset+3] = (value >> 0x18) & 0xFF
        bufList[offset+2] = (value >> 0x10) & 0xFF
        bufList[offset+1] = (value >> 0x08) & 0xFF
        bufList[offset+0] = (value >> 0x00) & 0xFF
        return bufList
    
    def get_array_value_le(self, bufList, offset):
        value = bufList[offset+3] << 24
        value += bufList[offset+2] << 16
        value += bufList[offset+1] << 8
        value += bufList[offset+0]
        return value
    
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
        return CRLF

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

    def is_dir(self, path):
        file = Path(path)
        return file.is_dir()

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
        onlyFiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
        return onlyFiles

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

    def get_file_data_binary(self, filePath, length=0):
        with open(filePath, "rb") as f:
            if length == 0:
                return f.read()
            return f.read(length)
        
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
    
    def fill_buffer(self, value, u32Cnt):
        buf = [value] * u32Cnt
        writeBuf = (ctypes.c_uint32 * u32Cnt)(*buf)
        return writeBuf
        
    def fill_buffer_4b(self, value, buffer, offset, length):
        for i in range(0, length, 4):
            self.set_array_value_le(buffer, offset + i, value)

        return buffer
    
    def compare_buffer(self, buffer1, buffer2):
        return buffer1 == buffer2
    
    def get_time_now(self):
        curTime = datetime.now()
        return curTime.strftime("%Y-%m-%d %H:%M:%S")

