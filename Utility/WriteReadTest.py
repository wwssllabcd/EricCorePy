import ctypes
from EricCorePy.Utility.EricUtility import *
from EricCorePy.ProtocolCmd.Nvme.NvmeCmdObj import byte_per_sec
import random

class WriteReadTest:
    def __init__(self, wrcu):
        self.wrcu = wrcu 
        
    def get_random_lba_len(self, maxLba, maxSecCnt, step):
        lba = random.randrange(maxLba)
        secCnt = random.randrange(1, maxSecCnt)

        if (step % 0x10) == 0:
            lba &= 0xFFFFFFF8
        
        return lba, secCnt

    def random_write_test(self, seed, maxLba, maxSecCnt):
        # setup random seed( you can setup by 0)
        if seed == None:
            seed = random.randint(0, 0x10000)

        print("random_write_test, seed = ", seed)

        random.seed(seed)

        u = EricUtility()
        step = 0 
        while True:
            step+=1
            lba, secCnt = self.get_random_lba_len(maxLba, maxSecCnt, step)
            writeBuf = (ctypes.c_uint8 * (secCnt * byte_per_sec()))()
            u.fill_buffer_4b(lba, writeBuf)
            self.wrcu.write_read_cmp(lba, secCnt, writeBuf, False)
