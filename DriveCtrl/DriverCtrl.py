from ctypes import *
import ctypes
import os
from ..ProtocolCmd.ufi.UfiCmd import *

CDB_SIZE = 16


class DriverCtrl:
    dllPath = os.path.dirname(__file__) + "\\DriveCtrl_w32.dll"

    m_winDll = windll.LoadLibrary(dllPath)

    def get_driver_name_list(self):
        return self.get_driver_list()[0]

    def get_driver_handle_list(self):
        return self.get_driver_list()[1]

    def get_ds(self):
        lib = self.m_winDll
        ds = lib.ds_get_ds(3, ctypes.c_char_p(b'usbstor'))
        return ds

    def get_driver_list(self):
        lib = self.m_winDll
        nameColls = []
        handles = []

        # ds = lib.ds_get_ds()
        ds = self.get_ds()
        cnt = lib.ds_get_cnt(ds)

        for i in range(cnt):
            handle = lib.ds_get_handle(ds, i)
            lib.ds_get_name.restype = ctypes.c_char_p
            name = lib.ds_get_name(ds, 0, ctypes.c_char_p(b''))
            nameColls.append(str(name))
            handles.append(handle)

        driverList = [nameColls, handles]
        return driverList

    def release_driver_list(self):
        lib = self.m_winDll
        ds = self.get_ds()
        lib.ds_release(ds)

    def send_cmd(self, handle, cmd, wDataBuf):
        lib = self.m_winDll
        cbuf_cdb = (c_ubyte*CDB_SIZE)()
        cBuf = (c_ubyte*65536)()
        # setup cdb
        for i in range(CDB_SIZE):
            cbuf_cdb[i] = cmd.cdb[i]

        # setup write data
        if cmd.direct == SCS_DATA_OUT:
            for i in range(cmd.len):
                cBuf[i] = wDataBuf[i]

        lib.usbcmd_sendCommand(handle, cbuf_cdb, cBuf, cmd.len, cmd.direct)

        res = []
        if cmd.direct == SCS_DATA_IN:
            for i in range(cmd.len):
                res.append(cBuf[i])

        return res
