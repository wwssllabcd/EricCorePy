from fcntl import ioctl
from EricCorePy.ProtocolCmd.Nvme.NvmeCmdObj import *

def ioc(dir, type, nr, size):
    return (dir << 30) | (size << 16) | (type << 8) | nr

def send_nvme_cmd_base(dev, cmd:NvmeCmdObj, ioctlNum):
    with open(dev, 'r') as fd:
	    # max xfer size = 0x200 sector
        res = ioctl(fd, ioctlNum, cmd.to_ioctl_ary())
        if res != 0:
            msg = "ioctl error = " + hex(res) + CRLF
            msg += "cmd = " + str(cmd)
            raise Exception(msg)