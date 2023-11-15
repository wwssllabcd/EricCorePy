
from EricCorePy.Utility.EricUtility import *

class LbaFailException(Exception):
    def __init__(self, desc, lba, secCnt):
        super().__init__(desc)
        self.lba = lba
        self.secCnt = secCnt



class WriteReadCmpUtility:
    def __init__(self, lba_write, lba_read):
        self._lba_write = lba_write 
        self.lba_read = lba_read
        self.write_record = None

    def lba_write(self, lba, secCnt, writeBuf):
        self._lba_write(lba, secCnt, writeBuf)
        if self.write_record != None:
            self.write_record(lba, secCnt)

    def write_read_cmp(self, lba, secCnt, writeBuf, isNoRead):
        u = EricUtility()
        print("write lba = " + hex(lba) + ", sec = " + hex(secCnt) + CRLF)
        self.lba_write(lba, secCnt, writeBuf)

        if lba == 0x2000:
            raise LbaFailException("cmp fail", lba, secCnt)

        if isNoRead:
            return 

        print("read  lba = " + hex(lba) + ", sec = " + hex(secCnt) + CRLF)
        readBuf = self.lba_read(lba, secCnt)
        res = u.compare_buffer(writeBuf, readBuf)
        if res == False:
            print("compare fail, lba = " + hex(lba) +", secCnt=" + hex(secCnt))
            raise LbaFailException("cmp fail", lba, secCnt)
        return readBuf


