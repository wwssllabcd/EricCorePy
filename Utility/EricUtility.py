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

import traceback

CRLF = "\r\n"
NULL_32 = 0xFFFFFFFF


m_logger = None

def eprint(*args, **kwargs):
    print(*args, **kwargs)
    if m_logger != None:
        m_logger.debug(*args, **kwargs)

def init_logger():
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
    def make_table_crlf(self, parts, cnt):
        if cnt !=0:
            if (cnt % 0x10) == 0:
                parts.append(CRLF)
            if (cnt % 0x200) == 0:
                parts.append(CRLF)

    def make_table_header(self, parts, cnt):
        if (cnt % 0x10) == 0:
            parts.append(format(cnt, '04X') + "| ")
        
    def make_hex_table(self, dataList, byteCnt=1):
        parts = []
        cnt = 0
        dataLen = len(dataList)

        formatStr = '02X'
        if byteCnt==2:
            formatStr = '04X'
        elif byteCnt==4:
            formatStr = '08X'

        if dataLen % byteCnt != 0:
            raise ValueError("dataList length must be a multiple of " + str(byteCnt))
        
        for i in range(0, dataLen, byteCnt):
   
            self.make_table_crlf(parts, cnt)
            self.make_table_header(parts, cnt)

            value = 0
            for j in range(byteCnt):
                offset = i+j
                if offset < dataLen:
                    value |= dataList[offset] << (8 * j)

            parts.append(format(value, formatStr) + " ")
            cnt += byteCnt
        return ''.join(parts)

    def make_ascii_table(self, dataList, byteCnt = 1, isBigEndian = True, makeLine=0xF):
        parts = []  
        cnt = 0
        dataLen = len(dataList)
        for i in range(0, dataLen, byteCnt): 

            value = []
            for j in range(byteCnt):
                offset = i+j
                if offset < dataLen:
                    d = dataList[offset]
                    c = chr(d) if chr(d).isprintable() else "."
                    value.append(c)


            # Append the two characters together
            if isBigEndian:
                value = reversed(value)
            
            parts.append(''.join(value))
            cnt += byteCnt

            if (cnt & makeLine) == 0:
                parts.append(CRLF)

        return ''.join(parts)
    
    def make_ascii_string(self, dataList, byteCnt = 1, isBigEndian = True):
        return self.make_ascii_table(dataList, byteCnt, isBigEndian, NULL_32)


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

    def set_array_value_le(self, buffer, value, offset=0):
        buffer[offset+3] = (value >> 0x18) & 0xFF
        buffer[offset+2] = (value >> 0x10) & 0xFF
        buffer[offset+1] = (value >> 0x08) & 0xFF
        buffer[offset+0] = (value >> 0x00) & 0xFF
    
    def get_array_value_le(self, bufList, offset):
        value = (bufList[3] << 24) + (bufList[2] << 16) + (bufList[1] << 8) + bufList[0]
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
        
    def fill_buffer_over_512b(self, value, buffer, length=0, offset=0):
        if length==0:
            length = len(buffer)

        # 將 value 轉換為位元組表示
        valueBytes = value.to_bytes(4, byteorder='little')
        
        # 計算初始填充塊大小
        chunkSize = 512
        fillChunk = valueBytes * (chunkSize // 4)

        # 計算要填充的次數
        numOfChunks = length // chunkSize
        remainBytes = length % chunkSize

        # 先填充一個較大的塊，以減少後續填充次數
        for _ in range(numOfChunks):
            buffer[offset:offset + chunkSize] = fillChunk
            offset += chunkSize
       
        if remainBytes > 0:
            buffer[offset : offset + remainBytes] = fillChunk[:remainBytes]


    def fill_buffer_4b(self, value, buffer, length=0, offset=0):
        if length==0:
            length = len(buffer)
            if length==0:
                raise Exception("length should not be 0")


     
        if (length >= 512):
            self.fill_buffer_over_512b(value, buffer, length, offset)
            return

        valueBytes = value.to_bytes(4, byteorder='little')

        for i in range(0, length, 4):
            buffer[offset+i : offset+i+4] = valueBytes

        return buffer
    
    def compare_buffer(self, buffer1, buffer2):
        return buffer1 == buffer2
    
    def get_time_now(self):
        return datetime.now()

    def show_exception(self, e):
        eprint(f"Exception: {e}")
        eprint(traceback.format_exc())
        exc_type, exc_value, exc_traceback = sys.exc_info()
        eprint(f"exception type: {exc_type}")
        eprint(f"exception value: {exc_value}")
        eprint(f"exception trace: {exc_traceback}")

    def list_to_bytearray(self, list) -> bytearray:
        array = bytearray()
        for item in list:
            array.extend(item.to_bytes(4, byteorder='little'))
        return array
    
    def bytearray_to_wordList(self, byteArray: bytearray):
        if len(byteArray) % 2 != 0:
            raise ValueError("Input bytearray length must be even.")
        
        # 使用 list comprehension 每次取兩個 bytes 組成一個 word
        words = []
        for i in range(0, len(byteArray), 2):
            # 小端序 (little-endian) 組合
            word = byteArray[i] | (byteArray[i + 1] << 8)
            words.append(word)
    
        return words
    
    def u32_to_u8_list(self, u32list, isLSB = True):
        u8list = []
        for num in u32list:
            if isLSB:
                u8list.append(num & 0xFF) 
                u8list.append((num >> 8) & 0xFF)  
                u8list.append((num >> 16) & 0xFF) 
                u8list.append((num >> 24) & 0xFF)  
            else:
                u8list.append((num >> 24) & 0xFF)  
                u8list.append((num >> 16) & 0xFF) 
                u8list.append((num >> 8) & 0xFF)  
                u8list.append(num & 0xFF) 
        return u8list