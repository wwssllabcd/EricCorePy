import ctypes
from EricCorePy.Utility.EricUtility import *

#----- Config -----
BYTE_PER_SECTOR = 512
NVME_ADMIN_IDENTIFY = 0x06
NVME_ADMIN_GET_LOG_PAGE = 0x02

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

class NvmeCmd_64B(ctypes.Structure):
    _fields_ = [
        ('opcode', ctypes.c_uint32),
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
    ]

class NvmePtCmd(ctypes.Structure):
    _fields_ = [
        ('cmd', NvmeCmd_64B),  
        ('timeout_ms', ctypes.c_uint32),
        ('result', ctypes.c_uint32)    
    ]

class NvmeCmdObj():
    def __init__(self):
        self.opcode = 0 # cdw0
        self.nsid = 0   # cdw1
        self.cdw2 = 0
        self.cdw3 = 0
        self.dataAddr = 0
        self.cdw10 = 0
        self.cdw11 = 0
        self.cdw12 = 0
        self.cdw13 = 0
        self.cdw14 = 0
        self.cdw15 = 0
        self.isAdminCmd = True
        self.dataLen = 0
        self.desc = ""

    def to_nvme_pt_cmd(self) -> NvmePtCmd:
        cmd_64b = NvmeCmd_64B(
            opcode=self.opcode,
            nsid=self.nsid,
            cdw2=self.cdw2,
            cdw3=self.cdw3,
            metaAddr=0,
            dataAddr=self.dataAddr,
            metaLen=0,
            dataLen=self.dataLen,
            cdw10=self.cdw10,
            cdw11=self.cdw11,
            cdw12=self.cdw12,
            cdw13=self.cdw13,
            cdw14=self.cdw14,
            cdw15=self.cdw15,
        )
        return NvmePtCmd(cmd=cmd_64b, timeout_ms=0, result=0)
    
    
    def to_c_array(self) -> NvmePtCmd:
        return self.to_nvme_pt_cmd()
    
    def to_64b(self) -> NvmeCmd_64B:
        return self.to_nvme_pt_cmd().cmd
    
    def __str__(self) -> str:
        # buf = bytearray(self.to_c_array()) 
        msg = "NvmeCmd" + CRLF
        # msg = ''.join('{:02X}, '.format(x) for x in buf)
        # msg += CRLF
        msg += "opcode = " + hex(self.opcode) + CRLF
        msg += "nsid = " + hex(self.nsid) + CRLF
        msg += "cdw2 = " + hex(self.cdw2) + CRLF
        msg += "cdw3 = " + hex(self.cdw3) + CRLF
        msg += "dataAddr = " + hex(self.dataAddr) + CRLF
        msg += "cdw10 = " + hex(self.cdw10) + CRLF
        msg += "cdw11 = " + hex(self.cdw11) + CRLF
        msg += "cdw12 = " + hex(self.cdw12) + CRLF
        msg += "cdw13 = " + hex(self.cdw13) + CRLF
        msg += "cdw14 = " + hex(self.cdw14) + CRLF
        msg += "cdw15 = " + hex(self.cdw15) + CRLF
        msg += "isAdminCmd = " + hex(self.isAdminCmd) + CRLF
        msg += "dataLen = " + hex(self.dataLen) + CRLF
        msg += "desc = " + self.desc + CRLF
        return msg

def byte_per_sec():
    return BYTE_PER_SECTOR

# ----------- not class --------
def get_normal_nvme_cmd():
    cmds = []
    cmds.append(nvme_cmd_id_ctrler())
    cmds.append(nvme_cmd_id_ns(0))
    cmds.append(nvme_cmd_get_log_page(0, 0, 1))

    # io cmd
    cmds.append(nvme_cmd_lba_read(0, 0, 1))
    cmds.append(nvme_cmd_lba_write(0, 0, 1))
    return cmds

def get_zns_nvme_cmd():
    cmds = []
    cmds.append(nvme_cmd_id_cns_zns(0))
    cmds.append(nvme_cmd_set_zone(0, 0, 0, 0))
    cmds.append(nvme_cmd_zone_append(0, 0, 1))
    cmds.append(nvme_cmd_report_zone(0, 0, 0x3F, 0, 0, True)) 
    return cmds

def nvme_cmd_id_ctrler():
    cmd = NvmeCmdObj()
    cmd.desc = "Admin: Identify Controller"
    cmd.opcode = NVME_ADMIN_IDENTIFY
    cmd.dataLen = 0x1000
    cmd.cdw10 = NVME_ID_CNS_CTRL
    cmd.nsid = 0 # NSID fixed 0
    return cmd

def nvme_cmd_id_ns(nsid):
    cmd = NvmeCmdObj()
    cmd.desc = "Admin: Identify Namespace"
    cmd.opcode = NVME_ADMIN_IDENTIFY
    cmd.dataLen = 0x1000
    cmd.cdw10 = NVME_ID_CNS_NS
    cmd.nsid = nsid
    return cmd

def nvme_cmd_get_log_page(nsid, logId, dwLen):
    if dwLen == 0:
        print("dwLen should not be 0", hex(dwLen))
    
    cmd = NvmeCmdObj()
    cmd.desc = "Admin: Get Log Page"
    cmd.opcode = NVME_ADMIN_GET_LOG_PAGE
    cmd.nsid = nsid
    cmd.dataLen = dwLen * 4

    dwNum = dwLen - 1 # start from 0
    cmd.cdw10 = (logId & 0xFF) + ((dwNum & 0xFFFF) << 16)
    cmd.cdw11 = (dwNum>>16) & 0xFFFF
    return cmd

def nvme_cmd_lba_read(nsid, slba, secCnt):
    cmd = NvmeCmdObj()
    cmd.desc = "IO: Read"
    cmd.isAdminCmd = False
    cmd.opcode = NVME_IO_CMD_READ
    cmd.nsid = nsid
    cmd.dataLen = secCnt * BYTE_PER_SECTOR

    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = secCnt - 1
    return cmd

def nvme_cmd_lba_write(nsid, slba, secCnt):
    cmd = NvmeCmdObj()
    cmd.desc = "IO: Write"
    cmd.isAdminCmd = False
    cmd.opcode = NVME_IO_CMD_WRITE
    cmd.nsid = nsid
    cmd.dataLen = secCnt * BYTE_PER_SECTOR

    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = secCnt - 1
    return cmd

##-------- ZNS --------
def nvme_cmd_id_cns_zns(nsid):
    cmd = NvmeCmdObj()
    cmd.desc = "Admin-ZNS: Identify"
    cmd.opcode = NVME_ADMIN_IDENTIFY
    cmd.dataLen = 0x1000
    cmd.cdw10 = 0x05
    cmd.nsid = nsid
    return cmd

def nvme_cmd_set_zone(nsid, slba, zoneSetAction, selectionAll):
    cmd = NvmeCmdObj()
    cmd.desc = "IO-ZNS: Set Zone"

    cmd.opcode = NVME_OPC_ZONE_MGMT_SEND
    cmd.nsid = nsid
    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw13 = zoneSetAction | selectionAll << 8
    cmd.isAdminCmd = False
    return cmd

def nvme_cmd_zone_append(nsid, slba, secCnt):
    cmd = NvmeCmdObj()
    cmd.desc = "IO-ZNS: Append"
    cmd.isAdminCmd = False
    cmd.opcode = NVME_OPC_ZONE_APPEND
    cmd.nsid = nsid
    cmd.dataLen = secCnt * BYTE_PER_SECTOR

    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = secCnt - 1
    return cmd

def nvme_cmd_report_zone(nsid, slba, dataLen, zra, zrasf, isPartial):
    cmd = NvmeCmdObj()
    cmd.desc = "IO-ZNS: Report Zones"

    cmd.opcode = NVME_OPC_ZONE_MGMT_RECV
    cmd.nsid = nsid
    cmd.dataLen = dataLen
    cmd.cdw10 = slba & 0xffffffff
    cmd.cdw11 = slba >> 32
    cmd.cdw12 = (dataLen >> 2) - 1
    cmd.cdw13 = zra | zrasf << 8 | isPartial << 16
    cmd.isAdminCmd = False
    return cmd