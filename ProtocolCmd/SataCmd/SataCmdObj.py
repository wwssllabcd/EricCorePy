SATA_FIS_H2D = 0x27


SATA_OPC_SMART = 0xB0
SMART_READ_DATA = 0xD0

SATA_OPC_IDENTIFY = 0xEC


SATA_BYET_PER_SECTOR = 512

# struct h2d_reg_fis {
#     uint8_t fis_type;      // FIS Type = 0x27(H2D)
#     uint8_t flags;         // Command Control Bits, bit[7] = 1 (Command), 其他設為 0, 通常設為 0x80
#     uint8_t command;       // EX: 0xEC (IDENTIFY DEVICE)
#     uint8_t features_l; 
#  
#     uint8_t lba_low;     
#     uint8_t lba_mid;     
#     uint8_t lba_high;    
#     uint8_t device;        // Device/Head Register, 通常設為 0x40 (bit[6] = 1 for LBA mode)

#     uint8_t lba_24; 
#     uint8_t lba_32; 
#     uint8_t lba_40; 
#     uint8_t features_h;

#     uint8_t count_l;
#     uint8_t count_h;
#     uint8_t icc;           // Isochronous Command Completion
#     uint8_t control;       // Control Register

#     uint8_t reserved[4];   // all 0
# };

class SataCmdObj():
    def __init__(self):
        self.fis = bytearray(16)  # sata fis 16 byte, bytearray default value is 0
        self.isDataIn = True
        self.dataLen = 0
        self.desc = ""

        self.fis[0] = SATA_FIS_H2D
        self.fis[1] = 0x80 # Command Register


class SataCmdSet():
    def identify(self):
        cmd = SataCmdObj()

        cmd.fis[2] = SATA_OPC_IDENTIFY
        cmd.fis[7] = 0x40 # for LBA mode 
        cmd.fis[0xC] = 1  # count

        cmd.desc = "Identify"
        cmd.isDataIn = True
        cmd.dataLen = cmd.fis[0xC] * SATA_BYET_PER_SECTOR

        return cmd
    
    def smart(self, feature):
        cmd = SataCmdObj()


        cmd.fis[2] = SATA_OPC_SMART
        cmd.fis[3] = feature 

        cmd.fis[5] = 0x4F
        cmd.fis[6] = 0xC2

        # cmd.fis[4] = 0x4F
        # cmd.fis[5] = 0xC2
        # cmd.fis[6] = 0xC2

        cmd.fis[7] = 0x40 # for LBA mode 

        cmd.fis[0xC] = 1  # count

        cmd.desc = "Smart"
        cmd.isDataIn = True
        cmd.dataLen = cmd.fis[0xC] * SATA_BYET_PER_SECTOR

        return cmd
    
    def get_cmd_colls(self):
        cmdSet = []
        cmdSet.append(self.identify())
        cmdSet.append(self.smart(SMART_READ_DATA))
        return cmdSet
    
