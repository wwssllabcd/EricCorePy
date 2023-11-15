import ctypes
from EricCorePy.Utility.EricUtility import *
from EricCorePy.Nvme.NvmeCmdObj import BYTE_PER_SECTOR
import random
from EricCorePy.Nvme.ReportZonesObj import *

class WriteReadTestZone:
    def __init__(self, wrcu, zoneSize, nrZone):
        self.wrcu = wrcu
        self.wrcu.write_record = self.add_record
        self.zoneSize = zoneSize
        self.zoneRecord = [[] for _ in range(nrZone)]


    def add_record(self, lba, secCnt):
        #print("record, lba=" + hex(lba) + ", secCnt=" + hex(secCnt))
        zoneNum, offset = self.get_zone_num_offset(lba, self.zoneSize)
        self.zoneRecord[zoneNum].append((lba, secCnt))

    def get_zone_num_offset(self, lba, zoneSize):
        zoneNum = lba // zoneSize
        offset = lba & (zoneSize-1)
        return zoneNum, offset
        
    def zns_sequence_write_test(self, lba, endLba, increase, zoneCap, zoneSize):
        u = EricUtility()
        writeBuf = (ctypes.c_uint8 * (increase * BYTE_PER_SECTOR))()

        while lba < endLba:
            zoneNum, offset = self.get_zone_num_offset(lba, zoneSize)
            secCnt = increase
            if offset >= zoneCap:
                lba = (zoneNum+1) * zoneSize
                continue

            # adjust secCnt
            if (offset + secCnt) > zoneCap:
                secCnt = zoneCap - offset

            u.fill_buffer_4b(lba, writeBuf, 0, len(writeBuf))
            self.wrcu.write_read_cmp(lba, secCnt, writeBuf, False)

            lba += secCnt

    
    def zns_sequence_write_zone(self, lba, endLba, zoneCap, zoneSize):
        u = EricUtility()
        maxSecCnt = 0x80
        
        while lba < endLba:
            zoneNum, offset = self.get_zone_num_offset(lba, zoneSize)
            secCnt = random.randint(1, maxSecCnt)

            if offset >= zoneCap:
                lba = (zoneNum+1) * zoneSize
                continue

            # adjust secCnt
            if (offset + secCnt) > zoneCap:
                secCnt = zoneCap - offset

            writeBuf = (ctypes.c_uint8 * (secCnt * BYTE_PER_SECTOR))()
            u.fill_buffer_4b(lba, writeBuf, 0, len(writeBuf))
            self.wrcu.write_read_cmp(lba, secCnt, writeBuf, False)

            lba += secCnt


    def verify_one_full_zone(self, zoneNum):
        print("verify_one_full_zone")

    def verify_zone_data(self):
        for zoneRcd in self.zoneRecord:
            for item in zoneRcd:
                print("lba=" + hex(item[0]) + ", len=" + hex(item[1]))
        self.verify_one_full_zone(0)



        