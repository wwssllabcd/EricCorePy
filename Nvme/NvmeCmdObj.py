import ctypes


NVME_ADMIN_IDENTIFY = 0x06

# ------ identify CNS -----
NVME_ID_CNS_NS = 0x00
NVME_ID_CNS_CTRL = 0x01
NVME_ID_CNS_CS_NS = 0x05

# ------ Report Zone -----
NVME_RP_ZONE_ZRASF_ALL = 0
NVME_RP_ZONE_ZRASF_EMPTY = 1
NVME_RP_ZONE_ZRASF_IOPEN = 2
NVME_RP_ZONE_ZRASF_EOPEN = 3

NVME_RP_ZONE_ZRASF_TRANS_FULLY = 0x10000
NVME_RP_ZONE_ZRASF_TRANS_PARTIAL = 0

NVME_RP_ZONE_ZRA_NORMAL = 0
NVME_RP_ZONE_ZRA_EXT_RPZ = 1

NVME_IO_CMD_WRITE = 1
NVME_IO_CMD_READ = 2

NVME_OPC_ZONE_MGMT_SEND = 0x79
NVME_OPC_ZONE_MGMT_RECV = 0x7A
NVME_OPC_ZONE_APPEND = 0x7D

BYTE_PER_SECTOR = 512


class NvmePtCmd(ctypes.Structure):
    _fields_ = [
        ('opcode', ctypes.c_ubyte),
        ('flags', ctypes.c_ubyte),
        ('rsvd1', ctypes.c_ushort),
        ('nsid', ctypes.c_uint32),
        ('cdw2', ctypes.c_uint32),
        ('cdw3', ctypes.c_uint32),
        ('metaAddr', ctypes.c_uint64),
        ('dataAddr', ctypes.c_uint64),
        ('metaLen', ctypes.c_uint32),
        ('dataLen', ctypes.c_uint32),
        ('cdw10', ctypes.c_uint32),
        ('cdw11', ctypes.c_uint32),
        ('cdw12', ctypes.c_uint32),
        ('cdw13', ctypes.c_uint32),
        ('cdw14', ctypes.c_uint32),
        ('cdw15', ctypes.c_uint32),
        ('timeout_ms', ctypes.c_uint32),
        ('result', ctypes.c_uint32)    
    ]

class NvmeCmd():
    def __init__(self):
        self.opcode = 0    
        self.nsid = 0
        self.cdw2 = 0
        self.cdw3 = 0
        self.dataAddr = 0
        self.dataLen = 0
        self.cdw10 = 0
        self.cdw11 = 0
        self.cdw12 = 0
        self.cdw13 = 0
        self.cdw14 = 0
        self.cdw15 = 0
        self.isAdminCmd = True
    
    def to_c_array(self) -> NvmePtCmd:
        return NvmePtCmd(
            opcode = self.opcode,
            nsid = self.nsid,
            dataAddr = self.dataAddr,
            dataLen = self.dataLen,
            cdw10 = self.cdw10,
            cdw11 = self.cdw11,
            cdw12 = self.cdw12,
            cdw13 = self.cdw13,
            cdw14 = self.cdw14,
            cdw15 = self.cdw15,
        )
    
    def __str__(self) -> str:
        # buf = bytearray(self.to_c_array()) 
        msg = "NvmeCmd" + CRLF
        # msg = ''.join('{:02X}, '.format(x) for x in buf)
        # msg += CRLF
        msg += "opcode=" + hex(self.opcode) + CRLF
        msg += "cdw10=" + hex(self.cdw10) + CRLF
        msg += "cdw11=" + hex(self.cdw11) + CRLF
        msg += "cdw12=" + hex(self.cdw12) + CRLF
        msg += "cdw13=" + hex(self.cdw13) + CRLF
        msg += "cdw14=" + hex(self.cdw14) + CRLF
        msg += "cdw15=" + hex(self.cdw15) + CRLF

        return msg
        

# ----------- not class --------
def nvme_cmd_id_ctrler():
    cmd = NvmeCmd()
    cmd.opcode = NVME_ADMIN_IDENTIFY
    cmd.dataLen = 0x1000
    cmd.cdw10 = NVME_ID_CNS_CTRL
    cmd.nsid = 0 # NSID fixed 0
    return cmd

def nvme_cmd_id_ns(nsid):
    cmd = NvmeCmd()
    cmd.opcode = NVME_ADMIN_IDENTIFY
    cmd.dataLen = 0x1000
    cmd.cdw10 = NVME_ID_CNS_NS
    cmd.nsid = nsid
    return cmd


def nvme_cmd_id_cns_zns(nsid):
    cmd = NvmeCmd()
    cmd.opcode = NVME_ADMIN_IDENTIFY
    cmd.dataLen = 0x1000
    cmd.cdw10 = 0x05
    cmd.nsid = nsid
    return cmd

def nvme_cmd_report_zone(nsid, slba, dataLen, zra, zrasf, isPartial):
    cmd = NvmeCmd()
    cmd.opcode = NVME_OPC_ZONE_MGMT_RECV
    cmd.nsid = nsid
    cmd.dataLen = dataLen
    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = (dataLen >> 2) - 1
    cmd.cdw13 = zra | zrasf << 8 | isPartial << 16
    cmd.isAdminCmd = False
    return cmd

def nvme_cmd_lba_read(nsid, slba, secCnt):
    cmd = NvmeCmd()
    cmd.isAdminCmd = False
    cmd.opcode = NVME_IO_CMD_READ
    cmd.nsid = nsid
    cmd.dataLen = secCnt * BYTE_PER_SECTOR

    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = secCnt - 1
    return cmd

def nvme_cmd_lba_write(nsid, slba, secCnt):
    cmd = NvmeCmd()
    cmd.isAdminCmd = False
    cmd.opcode = NVME_IO_CMD_WRITE
    cmd.nsid = nsid
    cmd.dataLen = secCnt * BYTE_PER_SECTOR

    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = secCnt - 1
    return cmd

def nvme_cmd_set_zone(nsid, slba, zoneSetAction, selectionAll):
    cmd = NvmeCmd()
    cmd.opcode = NVME_OPC_ZONE_MGMT_SEND
    cmd.nsid = nsid
    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw13 = zoneSetAction | selectionAll << 8
    cmd.isAdminCmd = False
    return cmd

def nvme_cmd_zone_append(nsid, slba, secCnt):
    cmd = NvmeCmd()
    cmd.isAdminCmd = False
    cmd.opcode = NVME_OPC_ZONE_APPEND
    cmd.nsid = nsid
    cmd.dataLen = secCnt * BYTE_PER_SECTOR

    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = secCnt - 1
    return cmd
