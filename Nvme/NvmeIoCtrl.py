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



FAKE_DEVICE = True


def ioc(dir, type, nr, size):
    return dir <<30 | size << 16 | type << 8 | nr

def send_nvme_cmd_base(dev, cmd, ioctlNum):
    with open(dev, 'r') as fd:
	    # max xfer size = 0x200 sector
	    res = ioctl(fd, ioctlNum, cmd.to_c_array())
	    if res != 0:
	        msg = "ioctl error = " + hex(res) + CRLF
	        msg += "cmd = " + str(cmd)
	        raise Exception(msg)

    
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
        byteArray = ctypes.create_string_buffer(cmd.dataLen)
    else:
        byteArray = writeBuf

    cmd.dataAddr = ctypes.addressof(byteArray)

    if FAKE_DEVICE:
        send_nvme_cmd_fake(dev, cmd, ioctlNum, byteArray)
    else:
        send_nvme_cmd_base(dev, cmd, ioctlNum)

    return bytearray(byteArray) 

