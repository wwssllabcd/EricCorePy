import ctypes
from EricCorePy.Utility.EricUtility import *
from EricCorePy.Nvme.NvmeCmdObj import BYTE_PER_SECTOR

class WriteReadTest:
    def __init__(self, wrc):
        self.wrc = wrc 

    def sequence_write_test(self, slba, eLba, secCnt, step):
        u = EricUtility()
        writeBuf = (ctypes.c_uint8 * (secCnt * BYTE_PER_SECTOR))()
        for lba in range(slba, eLba, step):
            u.fill_buffer_4b(lba, writeBuf, 0, len(writeBuf))
            self.wrc.write_read_cmp(lba, secCnt, writeBuf)


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
            self.write_read_cmp(lba, secCnt, writeBuf)

            lba += secCnt
        