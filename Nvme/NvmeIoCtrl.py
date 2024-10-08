from fcntl import ioctl
from ctypes import *
from EricCorePy.Nvme.NvmeCmdObj import *
from EricCorePy.Nvme.NvmeFake import *
from EricCorePy.Utility.EricUtility import CRLF

IO_DIR_NONE = 0
IO_DIR_WRITE = 1
IO_DIR_READ = 2
IO_DIR_RW = (IO_DIR_WRITE | IO_DIR_READ)

NVME_PT_CMD_SIZE = 0x48
NVME_ADMIN_CMD_NUM = 0x41
NVME_IO_CMD_NUM = 0x43

FAKE_DEVICE = False


def ioc(dir, type, nr, size):
    return (dir << 30) | (size << 16) | (type << 8) | nr

def send_nvme_cmd_base(dev, cmd:NvmeCmdObj, ioctlNum):
    with open(dev, 'r') as fd:
	    # max xfer size = 0x200 sector
        res = ioctl(fd, ioctlNum, cmd.to_c_array())
        if res != 0:
            msg = "ioctl error = " + hex(res) + CRLF
            msg += "cmd = " + str(cmd)
            raise Exception(msg)

    
def to_ctype_addr(byteArray):
    ctypeBuf = ctypes.c_char * len(byteArray)

    # from_buffer 方法不會複製資料，它只是建立了一個新的 ctypes object，使得這個 object 可以以 ctypes 支援的方式訪問 byteArray 的底層記憶體。
    newCtypeBuf = ctypeBuf.from_buffer(byteArray)
    return ctypes.addressof(newCtypeBuf)

def send_nvme_cmd(dev, cmd:NvmeCmdObj, writeBuf = None):
    ioctlNum = 0
    
    if cmd.isAdminCmd:
        ioctlNum = ioc(IO_DIR_RW, ord('N'), NVME_ADMIN_CMD_NUM, NVME_PT_CMD_SIZE)   
    else:
        ioctlNum = ioc(IO_DIR_RW, ord('N'), NVME_IO_CMD_NUM, NVME_PT_CMD_SIZE)

    # is read mode
    if writeBuf == None:
        #for read 
        byteArray = bytearray(cmd.dataLen)
    else:
        byteArray = writeBuf
 
    if isinstance(byteArray, bytearray) == False:
        msg = "only support bytearray" + CRLF
        raise Exception(msg)

    cmd.dataAddr = to_ctype_addr(byteArray)

    if FAKE_DEVICE:
        send_nvme_cmd_fake(dev, cmd, ioctlNum, byteArray)
    else:
        send_nvme_cmd_base(dev, cmd, ioctlNum)

    return byteArray


