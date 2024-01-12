
from EricCorePy.Utility.EricUtility import *


class WriteReadCmpUtility:
    def __init__(self, lba_write, lba_read):
        self._lba_write = lba_write 
        self.lba_read = lba_read
        self.write_record = None

    def lba_write(self, lba, secCnt, writeBuf):
            
        try:
            self._lba_write(lba, secCnt, writeBuf)
            if self.write_record != None:
                self.write_record(lba, secCnt)
        except InterruptedError as ie:
            #for spor test 
            eprint(f"InterruptedError: {ie}")
            eprint(f"errno=" + str(ie.errno))

            if ie.errno == 4:
                lbaEx = LbaFailException("Lba write fail", lba, secCnt)
                lbaEx.exMsg = str(ie)
                raise lbaEx

            raise ie
         
    def compare_two_buffer(self, lba, secCnt, writeBuf, readBuf):
        u = EricUtility()
        res = u.compare_buffer(writeBuf, readBuf)
        if res == False:
            eprint("compare fail, lba = " + hex(lba) + ", secCnt = " + hex(secCnt))
            eprint("writeBuf len = " + hex(len(writeBuf)))
            eprint("readBuf len = " + hex(len(readBuf)))

            msg = "fail Write Lba = " + hex(lba) + ", secCnt = " + hex(secCnt) + CRLF + u.make_hex_table(writeBuf)
            u.to_file("failWriteBuf.txt", msg)

            msg = "fail Read Lba = " + hex(lba) + ", secCnt = " + hex(secCnt) + CRLF + u.make_hex_table(readBuf)
            u.to_file("failReadBuf.txt", msg)
        
            raise Exception("compare_two_buffer fail")
            

    def write_read_cmp(self, lba, secCnt, writeBuf, isNoRead, curCnt=None):
        u = EricUtility()

        if curCnt !=None:
            msg = "(" + hex(curCnt) + ")"

        eprint(msg + "write lba = " + hex(lba) + ", sec = " + hex(secCnt))
        self.lba_write(lba, secCnt, writeBuf)

        if isNoRead:
            return 

        eprint(msg + "read  lba = " + hex(lba) + ", sec = " + hex(secCnt))
        readBuf = self.lba_read(lba, secCnt)
        res = u.compare_buffer(writeBuf, readBuf)
        if res == False:
            self.compare_two_buffer(lba, secCnt, writeBuf, readBuf)
        return readBuf


