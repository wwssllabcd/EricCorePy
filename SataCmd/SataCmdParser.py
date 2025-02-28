from .SataCmdObj import *
import struct

class SataCmdParser():
    def parser_ec_cmd(self, data):
        result = {}
        
        # General Configuration (Word 0)
        word0 = struct.unpack("<H", data[0:2])[0]
        result["is_ata"] = bool(word0 & 0x8000)
        result["response_incomplete"] = bool(word0 & 0x0004)
        
        # Model Number (Words 27-46)
        model = data[54:94].decode('ascii').strip()
        result["model_number"] = ''.join(char for char in model if char.isprintable())
        
        # Serial Number (Words 10-19)
        serial = data[20:40].decode('ascii').strip()
        result["serial_number"] = ''.join(char for char in serial if char.isprintable())
        
        # Firmware Revision (Words 23-26)
        firmware = data[46:54].decode('ascii').strip()
        result["firmware_revision"] = ''.join(char for char in firmware if char.isprintable())
        
        # Command Sets Supported (Words 82-83)
        supported_commands = struct.unpack("<HH", data[164:168])
        result["command_sets"] = {
            "smart": bool(supported_commands[0] & 0x0001),
            "security": bool(supported_commands[0] & 0x0002),
            "removable_media": bool(supported_commands[0] & 0x0004),
            "power_management": bool(supported_commands[0] & 0x0008),
            "packet": bool(supported_commands[0] & 0x0010),
            "write_cache": bool(supported_commands[0] & 0x0020),
            "look_ahead": bool(supported_commands[0] & 0x0040),
        }
        
        # Total Number of User Addressable Sectors (Words 60-61)
        lba_sectors = struct.unpack("<I", data[120:124])[0]
        result["total_sectors_28bit"] = lba_sectors
        
        # 48-bit Address Feature Set Supported Sectors (Words 100-103)
        lba_sectors_48 = struct.unpack("<Q", data[200:208])[0]
        result["total_sectors_48bit"] = lba_sectors_48
        
        # Physical/Logical Sector Size (Word 106)
        word106 = struct.unpack("<H", data[212:214])[0]
        result["sector_info"] = {
            "logical_sector_longer_than_256_words": bool(word106 & 0x1000),
            "multiple_logical_sectors_per_physical": bool(word106 & 0x2000),
            "logical_sector_size_implemented": bool(word106 & 0x4000),
        }
        
        # Transport Version (Word 222)
        transport = struct.unpack("<H", data[444:446])[0]
        result["transport_type"] = {
            0x0000: "Parallel ATA",
            0x0001: "Serial ATA 1.0a",
            0x0002: "Serial ATA II",
            0x0003: "Serial ATA 2.5",
            0x0004: "Serial ATA 2.6",
            0x0005: "Serial ATA 3.0",
            0x0006: "Serial ATA 3.1",
            0x0007: "Serial ATA 3.2",
        }.get(transport & 0x000F, "Unknown")
        
        # SMART Status (Word 87)
        word87 = struct.unpack("<H", data[174:176])[0]
        result["smart_supported"] = bool(word87 & 0x0001)
        result["smart_enabled"] = bool(word87 & 0x0002)
        
        # Security Status (Word 128)
        word128 = struct.unpack("<H", data[256:258])[0]
        result["security_status"] = {
            "supported": bool(word128 & 0x0001),
            "enabled": bool(word128 & 0x0002),
            "locked": bool(word128 & 0x0004),
            "frozen": bool(word128 & 0x0008),
            "count_expired": bool(word128 & 0x0010),
            "enhanced_erase_supported": bool(word128 & 0x0020),
        }
        
        lines = [f"{k}={v}" for k, v in result.items()]
        return "\n".join(lines)

    def parser_cmd(self, cmd: SataCmdObj, buffer):
        msg = None
        if cmd.fis[2] == SATA_OPC_IDENTIFY:
            msg = self.parser_ec_cmd(buffer)
        return msg
                        

