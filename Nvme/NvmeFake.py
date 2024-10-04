from EricCorePy.Nvme.NvmeCmdObj import *
from EricCorePy.Nvme.NvmeConst import *
from EricCorePy.Utility.EricUtility import *
from EricCorePy.Utility.EricException import *

# ----- Fake Disk -------      
DISK_SECTOR_CNT = 0x100000 # sector cnt = 1MB, total size = 512MB
DESK_INIT_VALUE = 0
m_disk = [DESK_INIT_VALUE] * DISK_SECTOR_CNT

# ----- config -------      
m_isZnsMode = True
DISK_CAPACITY = DISK_SECTOR_CNT

# ----- zns -------        
ZNS_ZONE_GAP = 0x200
ZNS_ONE_ZONE_CAP = 0x180
ZNS_ZONE_NUM = DISK_CAPACITY // ZNS_ZONE_GAP

m_zoneWp = [i * ZNS_ZONE_GAP for i in range(ZNS_ZONE_NUM)] 



# ---- read/write fail ------
m_rwFailFalg = False


def zns_check_lba_over_write_and_update_wp(lba):
    if m_isZnsMode == False:
        return 
    
    orgValue = m_disk[lba]
    if orgValue != DESK_INIT_VALUE:
        raise Exception("Zns: lba over write, lba=", hex(lba))
    
    zoneNum = lba // ZNS_ZONE_GAP

    #move next wp
    m_zoneWp[zoneNum] = lba+1

def set_disk_value(lba, value):
    zns_check_lba_over_write_and_update_wp(lba)
    m_disk[lba] = value

def set_write_fail(value):
    global m_rwFailFalg
    m_rwFailFalg = value


def fake_identify_ctrl(cmd, buffer):
    buffer[0] = 0xFF

def fake_identify_ns(buffer):
    u = EricUtility()
    u.set_array_value_le(buffer, DISK_CAPACITY)

def fake_identify(cmd, buffer):
    if(cmd.cdw10 == NVME_ID_CNS_NS):
        fake_identify_ns(buffer)

    if(cmd.cdw10 == NVME_ID_CNS_CTRL):
        fake_identify_ctrl(buffer)


def get_lba(cmd :NvmeCmdObj):
    return cmd.cdw10 + (cmd.cdw11 << 32)


# ----- zns -------
def set_one_zone(buffer, offset, zoneNum):
    u = EricUtility()
    buffer[offset + 0x00] = 0x02
    buffer[offset + 0x01] = 0x10

    u.set_array_value_le(buffer, ZNS_ONE_ZONE_CAP, offset + 0x08)
    u.set_array_value_le(buffer, zoneNum * ZNS_ZONE_GAP, offset + 0x10)
    u.set_array_value_le(buffer, m_zoneWp[zoneNum], offset + 0x18)


def clear_disk(slba, elba):
    global m_disk
    for i in range(slba, elba):
        m_disk[i] = DESK_INIT_VALUE

def fake_zns_send(cmd :NvmeCmdObj, buffer):
    global m_zoneWp

    zsa = cmd.cdw13 & 0xFF
    selectAll = (cmd.cdw13>>8) & 0xFF

    if zsa != NVME_ZONE_ACTION_RESET:
        eprint("not suppport zsa !=4")

    if (selectAll & 0x01) == 0:
        lba = get_lba(cmd)
        zoneNum = lba // ZNS_ZONE_GAP
        m_zoneWp[zoneNum] = zoneNum * ZNS_ZONE_GAP

        # clear one zone 
        slba = zoneNum * ZNS_ZONE_GAP
        elba = (zoneNum+1) * ZNS_ZONE_GAP

        clear_disk(slba, elba)
    else:
        m_zoneWp = [i * ZNS_ZONE_GAP for i in range(ZNS_ZONE_NUM)] 
        clear_disk(0, len(m_disk))

def fake_zns_report_zones(cmd, buffer):
    u = EricUtility()
    u.set_array_value_le(buffer, ZNS_ZONE_NUM)
 
    dataLen = cmd.dataLen

    for zoneNum in range(0, ZNS_ZONE_NUM):
        offset = zoneNum * 0x40 + 0x40
        if( offset>= dataLen ):
            return 
        set_one_zone(buffer, offset, zoneNum)

def fake_lba_write(cmd, buffer):
    slba = cmd.cdw10 + ( cmd.cdw11 << 32)
    secCnt = cmd.cdw12 + 1

    if secCnt == 0:
        raise LbaFailException("secCnt should not be 0", slba, secCnt)
    
    u = EricUtility()
    value = u.get_array_value_le(buffer, 0)
    for i in range(secCnt):
        if m_rwFailFalg:
            raise LbaFailException("[fake flag] write fail", slba, secCnt)
        set_disk_value(slba + i, value)


def fake_lba_read(cmd, buffer):
    slba = cmd.cdw10 + ( cmd.cdw11 << 32)
    secCnt = cmd.cdw12 + 1

    if m_rwFailFalg:
        raise LbaFailException("[fake flag] read fail", slba, secCnt)

    u = EricUtility()
    bytePerSec = byte_per_sec()
    for i in range(secCnt):
        value = m_disk[slba + i]
        offset = i * bytePerSec
        u.fill_buffer_4b(value, buffer, bytePerSec, offset)

def send_nvme_cmd_fake(dev, cmd, ioctlNum, buffer):
    if cmd.isAdminCmd:
        if(cmd.opcode == NVME_ADMIN_IDENTIFY):
            fake_identify(cmd, buffer)
        else:
            print(" not support admin, opc=" + hex(cmd.opcode))
    else:
        if(cmd.opcode == NVME_IO_CMD_WRITE):
            fake_lba_write(cmd, buffer)
        elif(cmd.opcode == NVME_IO_CMD_READ):
            fake_lba_read(cmd, buffer)
        elif(cmd.opcode == NVME_OPC_ZONE_MGMT_RECV):
            fake_zns_report_zones(cmd, buffer)
        elif(cmd.opcode == NVME_OPC_ZONE_MGMT_SEND):
            fake_zns_send(cmd, buffer)
        else:   
            print(" not support io-opc=" + hex(cmd.opcode))


