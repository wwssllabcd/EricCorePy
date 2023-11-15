from fcntl import ioctl
from ctypes import *
from EricCorePy.Nvme.NvmeCmdObj import *
from EricCorePy.Nvme.NvmeFake import *

IO_DIR_NONE = 0
IO_DIR_WRITE = 1
IO_DIR_READ = 2
IO_DIR_RW = (IO_DIR_WRITE | IO_DIR_READ)

NVME_PT_CMD_SIZE = 0x48
NVME_ADMIN_CMD_NUM = 0x41
NVME_IO_CMD_NUM = 0x43

NVME_ZONE_ACTION_RSD = 0x00
NVME_ZONE_ACTION_CLOSE = 0x01
NVME_ZONE_ACTION_FINISH = 0x02
NVME_ZONE_ACTION_OPEN = 0x03
NVME_ZONE_ACTION_RESET = 0x04
NVME_ZONE_ACTION_OFFLINE = 0x05
NVME_ZONE_ACTION_READONLY = 0x06 
NVME_ZONE_ACTION_EMPTY = 0x07
NVME_ZONE_ACTION_SET_ZD_EXT = 0x10

NVME_ZONE_STATE_RESERVED = 0x00
NVME_ZONE_STATE_EMPTY = 0x10
NVME_ZONE_STATE_IMPLICITLY_OPEN = 0x20
NVME_ZONE_STATE_EXPLICITLY_OPEN = 0x30
NVME_ZONE_STATE_CLOSED = 0x40
NVME_ZONE_STATE_READ_ONLY = 0xd0
NVME_ZONE_STATE_FULL = 0xe0
NVME_ZONE_STATE_OFFLINE = 0xf0

FAKE_DEVICE = True


def ioc(dir, type, nr, size):
    return dir <<30 | size << 16 | type << 8 | nr

def send_nvme_cmd_base(dev, cmd, ioctlNum):
    fd = open(dev, 'r')

    # max xfer size = 0x200 sector
    res = ioctl(fd, ioctlNum, cmd.to_c_array())
    if res != 0:
        print("ioctl error =", format(res, 'X'))
        print("cmd =" + str(cmd))
        raise RuntimeError(hex(res))

def send_nvme_cmd(dev, cmd, writeBuf = None):
    ioctlNum = 0
    
    if cmd.isAdminCmd:
        ioctlNum = ioc(IO_DIR_RW, ord('N'), NVME_ADMIN_CMD_NUM, NVME_PT_CMD_SIZE)   
    else:
        ioctlNum = ioc(IO_DIR_RW, ord('N'), NVME_IO_CMD_NUM, NVME_PT_CMD_SIZE)

    if writeBuf == None:
        # minimax data len for read restrict
        # if cmd.dataLen < 1024:
        #     cmd.dataLen = 1024
        byte_array = ctypes.create_string_buffer(cmd.dataLen)
    else:
        byte_array = writeBuf

    cmd.dataAddr = ctypes.addressof(byte_array)

    if FAKE_DEVICE:
        send_nvme_cmd_fake(dev, cmd, ioctlNum, byte_array)
    else:
        send_nvme_cmd_base(dev, cmd, ioctlNum)

    return bytearray(byte_array) 

