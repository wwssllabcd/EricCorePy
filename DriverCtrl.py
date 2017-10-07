

from ctypes import *
import ctypes

from ScsiCmd import SCS_DATA_IN, SCS_DATA_OUT

class DriverCtrl:
    m_winDll = windll.LoadLibrary(r'E:\GitHub\CPP_Project\UsbCommander\Debug\DriveCtrl.dll')
    def get_driver_list(self):
        lib = self.m_winDll
        nameColls = []
        handles = []

        ds = lib.ds_get_ds()
        cnt = lib.ds_get_cnt(ds)

        for i in range(cnt):
            handle = lib.ds_get_handle(ds, i)
            lib.ds_get_name.restype = ctypes.c_char_p
            name = lib.ds_get_name(ds, 0, ctypes.c_char_p(b''))
            
            nameColls.append(chr(name[0]))
            handles.append(handle)

        driverList = [nameColls, handles]
        return driverList

    def release_driver_list(self):
        lib = self.m_winDll
        ds = lib.ds_get_ds()
        lib.ds_release(ds)
 
    def send_cmd(self, handle, cmd, rwData):
        lib = self.m_winDll

        cbuf_cdb = (c_ubyte*12)()
        cBuf     = (c_ubyte*65536)()
        # setup cdb
        for i in range(12):
            cbuf_cdb[i] = cmd.cdb[i]

        # setup write data
        if cmd.direct == SCS_DATA_OUT:
            for i in range(cmd.len):
                cBuf[i] = rwData[i]

        lib.usbcmd_sendCommand(handle, cbuf_cdb, cBuf, cmd.len, cmd.direct)
        
        if cmd.direct == SCS_DATA_IN:
            for i in range(cmd.len):
                rwData.append( cBuf[i])
