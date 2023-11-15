from EricCorePy.Nvme.NvmeCmdObj import *
from EricCorePy.Utility.EricUtility import *

# ----- zns -------        
ZNS_ZONE_NUM = 0x10
ZNS_ZONE_CAP = 0x800
ZNS_ZONE_SIZE = 0x1000

# ----- Fake Disk -------      
DISK_SECTOR_CNT = 0x100000 # sector cnt = 1MB, total size = 512MB
m_disk = [0] * DISK_SECTOR_CNT

def fake_identify_ctrl(cmd, buffer):
    buffer[0] = 0xFF

def fake_identify(cmd, buffer):
    if(cmd.cdw10 == NVME_ID_CNS_CTRL):
        fake_identify_ctrl()

# ----- zns -------
def set_one_zone(buffer, offset, zoneNum):
    u = EricUtility()
    buffer[offset + 0x00] = 0x02
    buffer[offset + 0x01] = 0x10

    u.set_array_value_le(buffer, offset + 0x08, ZNS_ZONE_CAP)
    u.set_array_value_le(buffer, offset + 0x10, zoneNum * ZNS_ZONE_SIZE)
    u.set_array_value_le(buffer, offset + 0x18, zoneNum * ZNS_ZONE_SIZE)

def fake_report_zones(cmd, buffer):
    buffer[0] = ZNS_ZONE_NUM
    dataLen = cmd.dataLen
    u = EricUtility()
    for zoneNum in range(0, ZNS_ZONE_NUM):
        offset = zoneNum * 0x40 + 0x40
        if( offset>= dataLen ):
            return 
        set_one_zone(buffer, offset, zoneNum)

def fake_lba_write(cmd, buffer):
    slba = cmd.cdw10 + ( cmd.cdw11 << 32)
    secCnt = cmd.cdw12 + 1

    if secCnt == 0:
        raise Exception("secCnt should not be 0")
    
    u = EricUtility()
    value = u.get_array_value_le(buffer, 0)
    for i in range(secCnt):
        m_disk[slba + i] = value

def fake_lba_read(cmd, buffer):
    slba = cmd.cdw10 + ( cmd.cdw11 << 32)
    secCnt = cmd.cdw12 + 1

    u = EricUtility()
    for i in range(secCnt):
        value = m_disk[slba + i]
        u.fill_buffer_4b(value, buffer, i * BYTE_PER_SECTOR, BYTE_PER_SECTOR)

def send_nvme_cmd_fake(dev, cmd, ioctlNum, buffer):
    if(cmd.opcode == NVME_ADMIN_IDENTIFY):
        fake_identify(cmd, buffer)
    elif(cmd.opcode == NVME_OPC_ZONE_MGMT_RECV):
        fake_report_zones(cmd, buffer)
    elif(cmd.opcode == NVME_IO_CMD_WRITE):
        fake_lba_write(cmd, buffer)
    elif(cmd.opcode == NVME_IO_CMD_READ):
        fake_lba_read(cmd, buffer)
    else:
        print(" not support opc=" + hex(cmd.opcode))


