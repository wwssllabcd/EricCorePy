import ctypes
from EricCorePy.Utility.EricUtility import *
from EricCorePy.Utility.CtypeUtility import *

#----- Config -----
BYTE_PER_SECTOR = 512
NVME_ADMIN_IDENTIFY = 0x06
NVME_ADMIN_GET_LOG_PAGE = 0x02

#get_log_page.lid
NVME_LOG_SMART = 0x02  


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

def byte_per_sec():
    return BYTE_PER_SECTOR

class NvmeCmdObj():
    def __init__(self):
        self.cdws = [0] * 16
        self.isAdminCmd = True
        self.isDataIn = True
        self.dataLen = 0
        self.desc = ""

    def __str__(self) -> str:
        msg = "NvmeCmd" + CRLF
        return msg
    
    def to_64b(self):
        u = EricUtility()
        return u.list_to_bytearray(self.cdws)
    
    def to_ioctl_ary(self) -> bytearray:
        bAry = self.to_64b()
        
        timeout_ms = 0
        bAry.extend(timeout_ms.to_bytes(4, byteorder='little'))

        result = 0
        bAry.extend(result.to_bytes(4, byteorder='little'))
        return bAry



# ----------- not class --------
def nvme_cmd_id_ctrler():
    cmd = NvmeCmdObj()
    cmd.desc = "Admin: Identify Controller"
    cmd.cdws[0] = NVME_ADMIN_IDENTIFY
    cmd.cdws[1] = 0 # NSID fixed 0
    cmd.cdws[10] = NVME_ID_CNS_CTRL
    
    cmd.dataLen = 0x1000
    return cmd

def nvme_cmd_id_ns(nsid):
    cmd = NvmeCmdObj()
    cmd.desc = "Admin: Identify Namespace"
    cmd.cdws[0] = NVME_ADMIN_IDENTIFY
    cmd.cdws[1] = nsid
    cmd.cdws[10] = NVME_ID_CNS_NS
    
    cmd.dataLen = 0x1000
    return cmd

def nvme_cmd_get_log_page(nsid, logId, dwLen):
    if dwLen == 0:
        print("dwLen should not be 0", hex(dwLen))
    
    cmd = NvmeCmdObj()
    cmd.desc = "Admin: Get Log Page"
    cmd.cdws[0] = NVME_ADMIN_GET_LOG_PAGE
    cmd.cdws[1] = nsid
    dwNum = dwLen - 1 # start from 0
    cmd.cdws[10] = (logId & 0xFF) + ((dwNum & 0xFFFF) << 16)
    cmd.cdws[11] = (dwNum>>16) & 0xFFFF

    cmd.dataLen = dwLen * 4
    return cmd

def nvme_cmd_lba_read(nsid, slba, secCnt):
    cmd = NvmeCmdObj()
    cmd.desc = "IO: Read"
    
    cmd.cdws[0] = NVME_IO_CMD_READ
    cmd.cdws[1] = nsid
    cmd.cdws[10] = slba & 0xffffffff
    cmd.cdws[11] = slba >> 32
    cmd.cdws[12] = secCnt - 1

    cmd.dataLen = secCnt * BYTE_PER_SECTOR
    return cmd

def nvme_cmd_lba_write(nsid, slba, secCnt):
    cmd = NvmeCmdObj()
    cmd.desc = "IO: Write"
    
    cmd.cdws[0] = NVME_IO_CMD_WRITE
    cmd.cdws[1] = nsid
    cmd.cdws[10] = slba & 0xffffffff
    cmd.cdws[10] = slba >> 32
    cmd.cdws[12] = secCnt - 1

    cmd.isAdminCmd = False
    cmd.dataLen = secCnt * BYTE_PER_SECTOR
    cmd.isDataIn = False
    return cmd

##-------- ZNS --------
def nvme_cmd_id_cns_zns(nsid):
    cmd = NvmeCmdObj()
    cmd.desc = "Admin-ZNS: Identify"
    cmd.cdws[0] = NVME_ADMIN_IDENTIFY
    cmd.cdws[1] = nsid
    cmd.cdws[10] = 0x05

    cmd.dataLen = 0x1000
    return cmd

def nvme_cmd_set_zone(nsid, slba, zoneSetAction, selectionAll):
    cmd = NvmeCmdObj()
    cmd.desc = "IO-ZNS: Set Zone"

    cmd.cdws[0] = NVME_OPC_ZONE_MGMT_SEND
    cmd.cdws[1] = nsid
    cmd.cdws[10] = slba & 0xffffffff
    cmd.cdws[10] = slba >> 32
    cmd.cdws[12] = zoneSetAction | selectionAll << 8

    cmd.isAdminCmd = False
    return cmd

def nvme_cmd_zone_append(nsid, slba, secCnt):
    cmd = NvmeCmdObj()
    cmd.desc = "IO-ZNS: Append"
    
    cmd.cdws[0] = NVME_OPC_ZONE_APPEND
    cmd.cdws[1] = nsid
    cmd.cdws[10] = slba & 0xffffffff
    cmd.cdws[11] = slba >> 32
    cmd.cdws[12] = secCnt - 1

    cmd.isAdminCmd = False
    cmd.dataLen = secCnt * BYTE_PER_SECTOR
    return cmd

def nvme_cmd_report_zone(nsid, slba, dataLen, zra, zrasf, isPartial):
    cmd = NvmeCmdObj()
    cmd.desc = "IO-ZNS: Report Zones"

    cmd.cdws[0] = NVME_OPC_ZONE_MGMT_RECV
    cmd.cdws[1] = nsid
    cmd.cdws[10] = slba & 0xffffffff
    cmd.cdws[11] = slba >> 32
    cmd.cdws[12] = (dataLen >> 2) - 1
    cmd.cdws[13] = zra | zrasf << 8 | isPartial << 16
    
    cmd.isAdminCmd = False
    cmd.dataLen = dataLen
    return cmd

def get_normal_nvme_cmd():
    cmds = []
    cmds.append(nvme_cmd_id_ctrler())
    cmds.append(nvme_cmd_id_ns(1))
    cmds.append(nvme_cmd_get_log_page(0, NVME_LOG_SMART, 1024))

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