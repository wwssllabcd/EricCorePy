
from .ScsiCmdDefine import *
from EricCorePy.Utility.EricUtility import *

class ScsiCmdBase:
    def __init__(self):
        self.cdb = [0]*16
        self.dataLen = 0
        self.desc = ""
        self.direct = SCSI_IOCTL_DATA_IN
    
    def __str__(self):
        u = EricUtility()
        res = []
        res.append(u.make_hex_table(self.cdb, 1, True))
        res.append(f"direct = {hex(self.direct)}")
        res.append(f"dataLen = {hex(self.dataLen)}")
        return CRLF.join(res)

class UfiCmdSet:
    def get_read_10(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_READ_10
        cmd.cdb[8] = 0x01
        cmd.dataLen = cmd.cdb[8]*BYTE_PER_SECTOR

        cmd.direct = SCSI_IOCTL_DATA_IN
        cmd.desc = "UFI: Read10"
        return cmd

    def get_write_10(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_WRITE_10
        cmd.cdb[8] = 0x01
        cmd.dataLen = cmd.cdb[8]*BYTE_PER_SECTOR
        cmd.desc = "UFI: Write10"
        cmd.direct = SCSI_IOCTL_DATA_OUT
        return cmd

    def inquiry(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_INQUIRY
        cmd.cdb[4] = 0x24
        cmd.dataLen = 0x24
        cmd.desc = "UFI: Inquiry"
        cmd.direct = SCSI_IOCTL_DATA_IN
        return cmd
    
    def ata_pass_through_12(self):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = SCSI_OP_SAT12
        cmd.desc = "SCSI: ata_pass_through_12"
        cmd.direct = SCSI_IOCTL_NON_DATA
        return cmd
    
    def get_sat_protocol(self, isDataIn, secCnt):
        if secCnt == 0:
            return 0x03
        if isDataIn:
            return 0x04 # PIO Data-in 
        return 0x05 # PIO Data-out        

    def get_byteblock_length_type(self, secCnt):
         # sector mode
        t_byteBlock = 1

        # if BYTE_PER_SECTOR == 512:
        #     t_type = 0
        # else:
        #     t_type = 1

        # if secCnt == 0:
        #     t_Length = 0 # set 0, when No data to be transferred
        # else:
        #     t_Length = 1

        t_Length = 2 # need fixed 2, i don't know why
        t_type = 1   # need fixed 1, i don't know why
        
        return t_byteBlock, t_type, t_Length


    def sat_12_cmd(self, sataOpc, deviceReg, isDataIn, secCnt):
        cmd = ScsiCmdBase()
        if isDataIn:
            t_dir = 1 # data-in
        else:
            t_dir = 0 # data-out

        t_byteBlock, t_type, t_Length = self.get_byteblock_length_type(secCnt)

        cmd.cdb[0] = SCSI_OP_SAT12
        cmd.cdb[1] = (self.get_sat_protocol(isDataIn, secCnt) << 1)             
        cmd.cdb[2] = (t_type << 4) | (t_dir << 3) | (t_byteBlock << 2) | t_Length   
        cmd.cdb[4] = secCnt    
        cmd.cdb[8] = deviceReg        # Device Register, usually 0x40 (bit[6] = 1 for LBA mode)
        cmd.cdb[9] = sataOpc    

        cmd.desc = "SCSI: sat_12"
        cmd.dataLen = secCnt * BYTE_PER_SECTOR
        
        if isDataIn:
            cmd.direct = SCSI_IOCTL_DATA_IN
        else:
            cmd.direct = SCSI_IOCTL_DATA_OUT
        return cmd
    

    def get_cmd_colls(self):
        cmdColl = [self.inquiry(), self.get_write_10(), self.get_read_10(),  self.ata_pass_through_12(), self.sat_12_cmd(0xEC, 0x40, True, 1)]
        return cmdColl
