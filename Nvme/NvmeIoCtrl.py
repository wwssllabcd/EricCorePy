from fcntl import ioctl

from EricCorePy.Nvme.NvmeCmdObj import *
from EricCorePy.Nvme.NvmeFake import *
from EricCorePy.Nvme.NvmeIoCtrlLinux import *

from EricCorePy.Utility.EricUtility import CRLF
from EricCorePy.Utility.CtypeUtility import *

IO_DIR_NONE = 0
IO_DIR_WRITE = 1
IO_DIR_READ = 2
IO_DIR_RW = (IO_DIR_WRITE | IO_DIR_READ)

NVME_PT_CMD_SIZE = 0x48
NVME_ADMIN_CMD_NUM = 0x41
NVME_IO_CMD_NUM = 0x43

FAKE_DEVICE = False

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

    cmd.dataAddr = get_ctype_addr(byteArray)

    if FAKE_DEVICE:
        send_nvme_cmd_fake(dev, cmd, ioctlNum, byteArray)
    else:
        send_nvme_cmd_base(dev, cmd, ioctlNum)

    return byteArray


