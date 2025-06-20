from ctypes import Structure
import ctypes


m_crlf = "\n"

class ZoneDescrArray(Structure):
   _fields_ = [
       ("zoneType", ctypes.c_ubyte),
       ("zoneState", ctypes.c_ubyte),
       ("zoneAttri", ctypes.c_ubyte),
       ("", ctypes.c_uint32),
       ("zoneCap", ctypes.c_uint32),
       ("zoneSlba", ctypes.c_uint64),  #b16~23
       ("zoneWp", ctypes.c_uint64),  #b24~31
    ]
   
class ZoneDescr(Structure):
    def __init__(self, zoneDescrArray):
        self.zoneType = zoneDescrArray.zoneType
        self.zoneState = zoneDescrArray.zoneState
        self.zoneAttri = zoneDescrArray.zoneAttri
        self.zoneCap = zoneDescrArray.zoneCap
        self.zoneSlba = zoneDescrArray.zoneSlba
        self.zoneWp = zoneDescrArray.zoneWp
    def __str__(self):
        return "SLBA: " + hex(self.zoneSlba) + "  WP: " + hex(self.zoneWp) + "  Cap: " + hex(self.zoneCap) + "  State: " + hex(self.zoneState) + "  Type: " + hex(self.zoneType) + "  Attrs: " +hex(self.zoneAttri)
        
   
class ReportZones():
    def __init__(self, byteArray):

        zoneCnt = len(byteArray) // 0x40
        if zoneCnt==0:
            return
        
        self.nrZone = byteArray[1] << 8 | byteArray[0]
        zoneCnt -=1

        self.zones = []
        for i in range(zoneCnt):
            offset = 0x40 + 0x40*i
            byteZone = byteArray[offset:offset+0x40]
            zone = ZoneDescr(ZoneDescrArray.from_buffer_copy(byteZone))
            self.zones.append(zone)

    def __str__(self):
        msg = "nr_zone = " + hex(self.nrZone) + m_crlf
        for i in range(len(self.zones)):
            zone = self.zones[i]
            msg += str(zone) + m_crlf
        return msg