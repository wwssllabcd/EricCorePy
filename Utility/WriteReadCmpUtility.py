import random

from EricCorePy.Utility.EricUtility import *
from EricCorePy.Utility.EricException import *
from EricCorePy.ProtocolCmd.Nvme.NvmeCmdObj import byte_per_sec



class WriteReadCmpUtility:
    def __init__(self, lba_write, lba_read, recordFunc=None):
        self._lba_write = lba_write 
        self._lba_read = lba_read
        self._testCnt = 0

        self._recordFun = recordFunc
            
    def get_elba(self, endLba, idnsBuf):
        u = EricUtility()
        capacity = u.get_array_value_le(idnsBuf, 0)
        if endLba == None:
            endLba = capacity
        return min(endLba, capacity)

    def throw_exception_spor(self, ie, lba, secCnt):
        eprint(f"Exception: {ie}")
        eprint(f"type: {type(ie)}")
        eprint(f"errno=" + str(ie.errno))
        
        if (ie.errno == 4) or (ie.errno == 5):
            lbaEx = LbaFailException("Lba fail", lba, secCnt)
            lbaEx.exMsg = str(ie)
            raise lbaEx
        
        raise ie

    def lba_write(self, lba, secCnt, writeBuf):
        try:
            self._lba_write(lba, secCnt, writeBuf)
            if self._recordFun != None:
                self._recordFun(lba, secCnt)

        except OSError as ie:
            #for spor test
            self.throw_exception_spor(ie, lba, secCnt)
    
    def lba_read(self, lba, secCnt):
        try:
            return self._lba_read(lba, secCnt)
        except OSError as ie:
            #for spor test
            self.throw_exception_spor(ie, lba, secCnt)
         
    def compare_two_buffer(self, lba, secCnt, writeBuf, readBuf):
        u = EricUtility()
        res = u.compare_buffer(writeBuf, readBuf)
        if res == False:
            eprint("compare fail at lba = " + hex(lba) + ", secCnt = " + hex(secCnt))
            eprint("writeBuf len = " + hex(len(writeBuf)))
            eprint("readBuf len = " + hex(len(readBuf)))

            msg = "fail Write Lba = " + hex(lba) + ", secCnt = " + hex(secCnt) + CRLF + u.make_hex_table(writeBuf)
            u.to_file("failWriteBuf.txt", msg)

            msg = "fail Read Lba = " + hex(lba) + ", secCnt = " + hex(secCnt) + CRLF + u.make_hex_table(readBuf)
            u.to_file("failReadBuf.txt", msg)
            raise Exception("compare_two_buffer fail")
        

    def get_random_lba_len(self, rdm, maxLba, maxSecCnt, step):
        secCnt = rdm.randrange(1, maxSecCnt)
        lba = rdm.randrange(maxLba - secCnt - 1)
        
        # set align 4k
        if (step % 0x10) == 0:
            lba &= 0xFFFFFFF8
        
        return lba, secCnt
    
    def is_overwrite_record_lba(self, curLba, secCnt, recordLba):
        curEndLba = curLba + secCnt
        for (recordLba, _) in recordLba:
            if recordLba >= curLba:
                if curEndLba > recordLba:
                    return True
        return False


    def get_random_lba_len_no_overwrite(self, rdm, maxLba, maxSecCnt, step, recordLba):
        while True:
            lba, secCnt = self.get_random_lba_len(rdm, maxLba, maxSecCnt, step)
            if self.is_overwrite_record_lba(lba, secCnt, recordLba) == False:
                return lba, secCnt
            
            secCnt = 1
            if self.is_overwrite_record_lba(lba, secCnt, recordLba) == False:
                return lba, secCnt
            
    def eprint(*args, **kwargs):
        return " ".join(map(str, args))

    def one_write_read_cmp(self, lba, secCnt, writeBuf, isNoWrite, isNoRead, isShowTime, send_msg):
        strTimes = ""
        if isShowTime:
            self._testCnt+=1
            strTimes = "(" + hex(self._testCnt) +")"

        if isNoWrite == False:
            send_msg(strTimes + "write lba = " + hex(lba) + ", sec = " + hex(secCnt))
            self.lba_write(lba, secCnt, writeBuf)

        if isNoRead:
            return 

        send_msg(strTimes + "read lba = " + hex(lba) + ", sec = " + hex(secCnt), True)
        readBuf = self.lba_read(lba, secCnt)
        self.compare_two_buffer(lba, secCnt, writeBuf, readBuf)

        send_msg(strTimes + "pass", True)
   
        return readBuf
    
    def verify_record(self, writeRecord):
        eprint("== Verify Record, cnt = " + hex( len(writeRecord) ) + " ==")
        u = EricUtility()
        for (lba, secCnt) in writeRecord:
            writeBuf = bytearray(secCnt * byte_per_sec())
            u.fill_buffer_4b(lba, writeBuf)
            self.one_write_read_cmp(lba, secCnt, writeBuf, True, False, None)            

    def sequence_write_test(self, slba, eLba, secCnt, step, isNoWrite, isNoRead):
        u = EricUtility()
        writeBuf = bytearray(secCnt * byte_per_sec())
        for lba in range(slba, eLba, step):
            u.fill_buffer_4b(lba, writeBuf)
            self.one_write_read_cmp(lba, secCnt, writeBuf, isNoWrite, isNoRead, None)
