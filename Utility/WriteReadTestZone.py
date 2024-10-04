import ctypes
from EricCorePy.Utility.EricUtility import *
from EricCorePy.Nvme.NvmeCmdObj import byte_per_sec
import random
from EricCorePy.Nvme.ReportZonesObj import *

class WriteReadTestZone:
    def __init__(self, wrcu, zoneSize, nrZone):
        self.wrcu = wrcu
        self.wrcu.write_record = self.add_record
        self.zoneSize = zoneSize
        self.zoneRecord = [[] for _ in range(nrZone)]
        self.seqWrcCnt = 1


    def add_record(self, lba, secCnt):
        #print("record, lba=" + hex(lba) + ", secCnt=" + hex(secCnt))
        zoneNum, _ = self.get_zone_num_offset(lba, self.zoneSize)
        self.zoneRecord[zoneNum].append((lba, secCnt))

    def get_zone_num_offset(self, lba, zoneSize):
        zoneNum = lba // zoneSize
        offset = lba & (zoneSize-1)
        return zoneNum, offset
        
    def gen_write_buffer(self, lba, secCnt):
        writeBuf = (ctypes.c_uint8 * (secCnt * byte_per_sec()))()
        u = EricUtility()
        u.fill_buffer_4b(lba, writeBuf)
        return writeBuf

    # def zns_sequence_write_test(self, lba, endLba, increase, zoneCap, zoneSize):
    #     u = EricUtility()
    #     writeBuf = (ctypes.c_uint8 * (increase * BYTE_PER_SECTOR))()

    #     while lba < endLba:
    #         zoneNum, offset = self.get_zone_num_offset(lba, zoneSize)
    #         secCnt = increase
    #         if offset >= zoneCap:
    #             lba = (zoneNum+1) * zoneSize
    #             continue

    #         # adjust secCnt
    #         if (offset + secCnt) > zoneCap:
    #             secCnt = zoneCap - offset

    #         u.fill_buffer_4b(lba, writeBuf, len(writeBuf))
    #         self.wrcu.write_read_cmp(lba, secCnt, writeBuf, False)

    #         lba += secCnt

    
    def zns_sequence_write_zone(self, lba, endLba, zoneCap, stopStep=NULL_32):
        u = EricUtility()

		#max xfer len must be less 256k
        if byte_per_sec() == 512:
            maxSecCnt = 0xFF
        else:
            maxSecCnt = 0x3F # 256/4 = 64
        
        curStep = 0
        while lba < endLba:
            zoneNum, offset = self.get_zone_num_offset(lba, self.zoneSize)
            secCnt = random.randint(0x1, maxSecCnt)

            if offset >= zoneCap:
                lba = (zoneNum+1) * self.zoneSize
                continue

            # adjust secCnt
            if (offset + secCnt) > zoneCap:
                secCnt = zoneCap - offset

            writeBuf = self.gen_write_buffer(lba, secCnt)
            self.wrcu.write_read_cmp(lba, secCnt, writeBuf, True, self.seqWrcCnt)
            self.seqWrcCnt+=1
            curStep+=1

            if curStep >= stopStep:
                eprint("stop, wrcCnt =" + hex(curStep) + ", stopLba =", hex(lba))
                return lba + secCnt 
            
            lba += secCnt

        eprint("zns_sequence_write_zone done")
        return lba

    
    def clear_zone_record(self, zoneNum):
        self.zoneRecord[zoneNum].clear()

    def clear_zone_record_all(self, totalZoneNum):
        for i in range(totalZoneNum):
            self.clear_zone_record(i)

    def verify_one_lba(self, lba, secCnt):
        eprint("verify lba=" + hex(lba) +", secCnt=" + hex(secCnt))
        u = EricUtility()

        writeBuf = self.gen_write_buffer(lba, secCnt)
        readBuf = self.wrcu.lba_read(lba, secCnt)
        res = u.compare_buffer(writeBuf, readBuf)
        if res == False:
            self.wrcu.compare_two_buffer(lba, secCnt, writeBuf, readBuf)


    def verify_one_zone(self, zoneNum, start, end):
        oneZoneRecord = self.zoneRecord[zoneNum]
        recordCnt = len(oneZoneRecord)
        
        if start > end:
            raise Exception("wrong start, end value, start=", str(start), ", end=", str(end))
        
        if recordCnt < end:
            end = recordCnt

        print(CRLF + "verify_one_zone, zoneNum =", hex(zoneNum))
        for i in range(start, end):
            record = oneZoneRecord[i]
            lba = record[0]
            secCnt = record[1]
            self.verify_one_lba(lba, secCnt)

    def verify_one_zone_full(self, zoneNum):
        oneZoneRecord = self.zoneRecord[zoneNum]
        self.verify_one_zone(zoneNum, 0, len(oneZoneRecord))

    def verify_all_zone(self):
        print(CRLF + "verify_all_zone")
        zoneCnt = len(self.zoneRecord)
        for i in range(zoneCnt):
            self.verify_one_zone_full(i)

    def verify_zone_to_end(self, zoneNum):
        for i in range(zoneNum, len(self.zoneRecord)):
            self.verify_one_zone_full(i)

    def get_record_item(record):
        return record[0], record[1]
    
    # def find_record_idx(self, lba):
    #     zoneNum, _ = self.get_zone_num_offset(lba, self.zoneSize)
    #     writeZoneRecord = self.zoneRecord[zoneNum]
        
    #     for idx in range(len(writeZoneRecord)):
    #         record = writeZoneRecord[idx]
    #         recordLba, _ = self.get_record_item(record)

    #         if recordLba >= lba:
    #             return idx
            
    #     msg = ""
    #     msg += "record not found, lba=" + hex(lba) + ", zoneSize = " + hex(self.zoneSize) + ", zoneNum=" + hex(zoneNum)
    #     raise Exception(msg)

    def verify_zone_head_tail(self):
        checkCnt = 2
        for zoneIdx in range(len(self.zoneRecord)):
            self.verify_one_zone(zoneIdx, 0, checkCnt)

            oneZoneRecord = self.zoneRecord[zoneIdx]
            cnt = len(oneZoneRecord)
            if cnt > checkCnt:
                self.verify_one_zone(zoneIdx, cnt-checkCnt, cnt)


    def verify_lba_to_end(self, lba):
        print(CRLF + "verify_lba_to_end, start verify lba=" + hex(lba))

        startZone, offset = self.get_zone_num_offset(lba, self.zoneSize)

        #adjust offset (max secCnt = 0x100)
        if offset >= 0x100:
            offset -= 0x100
        else:
            offset = 0

        adjustLba = (startZone * self.zoneSize) + offset

        print("adjustLba = " + hex(adjustLba))

        for zoneIdx  in range(startZone, len(self.zoneRecord)):
            oneZoneRecord = self.zoneRecord[zoneIdx]

            cnt = len(oneZoneRecord)

            for recordIdx in range(0, cnt):
                recordLba, secCnt = oneZoneRecord[recordIdx]
                if recordLba < adjustLba:
                    continue
                self.verify_one_lba(recordLba, secCnt)


    def verify_lba(self, lba, porCnt):
        self.verify_lba_to_end(lba)
        if (porCnt % 0x100) == 0:
            self.verify_zone_head_tail()

        