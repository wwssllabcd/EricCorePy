
from EricCorePy.DriveCtrl.ScsiCmd.ScsiCmdBase import *
from EricCorePy.Utility.EricUtility import *

class UfiCmdSet:
    def __init__(self):
        self.m_u = EricUtility()

    def read_10(self, lba=0, secCnt=0x01):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_READ_10
        self.m_u.set_array_value_be(cmd.cdb, 2, lba)
        cmd.cdb[8] = secCnt
        cmd.dataLen = cmd.cdb[8] * BYTE_PER_SECTOR

        cmd.direct = SCSI_IOCTL_DATA_IN
        cmd.desc = "UFI: Read10"
        return cmd

    def write_10(self, lba=0, secCnt=0x01):
        cmd = ScsiCmdBase()
        cmd.cdb[0] = UFI_OP_WRITE_10
        self.m_u.set_array_value_be(cmd.cdb, 2, lba)
        cmd.cdb[8] = secCnt
        cmd.dataLen = cmd.cdb[8] * BYTE_PER_SECTOR
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

    def get_byteblock_length_type(self):
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


    def sat_12_cmd(self, comand, device, feature, lba, isDataIn, secCnt):
        cmd = ScsiCmdBase()
        if isDataIn:
            t_dir = 1 # data-in
        else:
            t_dir = 0 # data-out

        t_byteBlock, t_type, t_Length = self.get_byteblock_length_type()

        cmd.cdb[0] = SCSI_OP_SAT12
        cmd.cdb[1] = (self.get_sat_protocol(isDataIn, secCnt) << 1)             
        cmd.cdb[2] = (t_type << 4) | (t_dir << 3) | (t_byteBlock << 2) | t_Length   

        cmd.cdb[3] = feature 
        cmd.cdb[4] = secCnt 

        # only xfer 3 byte for lba
        cmd.cdb[5] = lba & 0xFF
        cmd.cdb[6] = (lba >> 8) &0xFF
        cmd.cdb[7] = (lba >> 16) &0xFF
        

        cmd.cdb[8] = device & 0xFF       # Device Register, usually 0x40 (bit[6] = 1 for LBA mode)
        cmd.cdb[9] = comand & 0xFF   

        cmd.desc = "SCSI: sat_12"
        cmd.dataLen = secCnt * BYTE_PER_SECTOR
        
        if isDataIn:
            cmd.direct = SCSI_IOCTL_DATA_IN
        else:
            cmd.direct = SCSI_IOCTL_DATA_OUT
        return cmd

    def sat_16_cmd(self, fis, isDataIn):
        cmd = ScsiCmdBase()
        if isDataIn:
            t_dir = 1 # data-in
        else:
            t_dir = 0 # data-out


        secCnt = self.m_u.get_value(fis[0xC:], 2)

        t_byteBlock, t_type, t_Length = self.get_byteblock_length_type()
        enableExtend = 1

        comand = fis[2]
        device = fis[7]


        cmd.cdb[0] = SCSI_OP_SAT16
        cmd.cdb[1] = (self.get_sat_protocol(isDataIn, secCnt) << 1) | enableExtend         
        cmd.cdb[2] = (t_type << 4) | (t_dir << 3) | (t_byteBlock << 2) | t_Length   

        cmd.cdb[3] = fis[0xB]
        cmd.cdb[4] = fis[0x3] 

        cmd.cdb[5] = (secCnt >> 8) & 0xFF
        cmd.cdb[6] = secCnt & 0xFF

        cmd.cdb[7] = fis[0x8] 
        cmd.cdb[8] = fis[0x4] 
        
        cmd.cdb[9] = fis[0x9] 

        cmd.cdb[10] = fis[0x5] 
        cmd.cdb[11] = fis[0xA] 
        cmd.cdb[12] = fis[0x6] 

        cmd.cdb[13] = device & 0xFF       # Device Register, usually 0x40 (bit[6] = 1 for LBA mode)
        cmd.cdb[14] = comand & 0xFF   
        cmd.cdb[15] = fis[0xF]  

        cmd.desc = "SCSI: sat_16"
        cmd.dataLen = secCnt * BYTE_PER_SECTOR
        
        if isDataIn:
            cmd.direct = SCSI_IOCTL_DATA_IN
        else:
            cmd.direct = SCSI_IOCTL_DATA_OUT
        return cmd
    

    def get_cmd_colls(self):
        cmdColl = [self.inquiry(), self.write_10(), self.read_10(),  self.ata_pass_through_12(), self.sat_12_cmd(0xEC, 0x40, 0, 0, True, 1)]
        return cmdColl
