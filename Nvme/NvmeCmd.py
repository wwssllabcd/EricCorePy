from EricCorePy.Nvme.NvmeCmdObj import *
from EricCorePy.Nvme.NvmeIoCtrl import *

def get_nvme_cmd_obj(devNvmeXnY):
    nsid = int(devNvmeXnY[11])
    return NvmeCmd(devNvmeXnY, nsid)

class NvmeCmd():
    def __init__(self, dev, nsid):
        self.dev = dev
        self.nsid = nsid

    def lba_write(self, lba, secCnt, buffer):
        return send_nvme_cmd(self.dev, nvme_cmd_lba_write(self.nsid, lba, secCnt), buffer)

    def lba_read(self, lba, secCnt):
        return send_nvme_cmd(self.dev, nvme_cmd_lba_read(self.nsid, lba, secCnt))

    def identify_ns(self):
        return send_nvme_cmd(self.dev, nvme_cmd_id_ns(self.nsid))

    def zns_report_zones(self, slba, dataLen, zra, zrasf, isPartial):
        return send_nvme_cmd(self.dev, nvme_cmd_report_zone(self.nsid, slba, dataLen, zra, zrasf, isPartial))
        
    def zns_reset_zone(self):
        send_nvme_cmd(self.dev, nvme_cmd_set_zone(self.nsid, 0, NVME_ZONE_ACTION_RESET, True))