
from EricCorePy.ProtocolCmd.Nvme.NvmeCmdObj import *
import struct


def key_value_to_string(dic:dict):
    lines = [f"{k} = {v}" for k, v in dic.items()]
    return "\n".join(lines)


def parser_nvme_id_ns(cmd: NvmeCmdObj, buffer: bytearray):
    
    byteData = bytes(buffer)
    nsStruct = struct.Struct('<'
                            'Q'    # NSZE (Namespace Size)
                            'Q'    # NCAP (Namespace Capacity)
                            'Q'    # NUSE (Namespace Utilization)
                            'B'    # NSFEAT (Namespace Features)
                            'B'    # NLBAF (Number of LBA Formats)
                            'B'    # FLBAS (Formatters LBA Size)
                            'B'    # MC (Metadata Capabilities)
                            
                            'B'    # DPC (0ffset 0x10)
                            'B'    # DPS
                            'B'    # NMIC
                            'B'    # RESCAP

                            )

    # Unpack the bytearray into a tuple of values
    values = nsStruct.unpack_from(byteData, offset=0)

    # Convert the values to strings and store in a dictionary
    namespace_data = {
        'nsze': hex(values[0]),  # Namespace Size
        'ncap': hex(values[1]),  # Namespace Capacity
        'nuse': hex(values[2]),  # Namespace Utilization
        'nsfeat': hex(values[3]),
        'NLBAF': hex(values[4]),
        'FLBAS': hex(values[5]),
        'MC': hex(values[6]),
        'DPC': hex(values[7]),
        'DPS': hex(values[8]),
        'NMIC': hex(values[9]),
        'RESCAP': hex(values[10]),
    }

    return key_value_to_string(namespace_data)

def parser_nvme_id_ctrler(cmd: NvmeCmdObj, data):
    if len(data) != 4096:
        raise ValueError("Invalid data length. Expected 4096 bytes.")
        
    result = {}
    
    # PCI Vendor ID (bytes 0-1)
    result['vid'] = f"0x{data[0] | (data[1] << 8):04x}"
    
    # PCI Subsystem Vendor ID (bytes 2-3)
    result['ssvid'] = f"0x{data[2] | (data[3] << 8):04x}"
    
    # Serial Number (bytes 4-23)
    result['sn'] = bytes(data[4:24]).decode('ascii').strip()
    
    # Model Number (bytes 24-63)
    result['mn'] = bytes(data[24:64]).decode('ascii').strip()
    
    # Firmware Revision (bytes 64-71)
    result['fr'] = bytes(data[64:72]).decode('ascii').strip()
    
    # Recommended Arbitration Burst (byte 72)
    result['rab'] = str(data[72])
    
    # IEEE OUI Identifier (bytes 73-75)
    result['ieee'] = f"{data[73]:02x}:{data[74]:02x}:{data[75]:02x}"
    
    # Controller Multi-Path I/O and Namespace Sharing Capabilities (byte 76)
    result['cmic'] = f"0x{data[76]:02x}"
    
    # Maximum Data Transfer Size (byte 77)
    result['mdts'] = str(data[77])
    
    # Controller ID (bytes 78-79)
    result['cntlid'] = f"0x{data[78] | (data[79] << 8):04x}"
    
    # Version (bytes 80-83)
    result['ver'] = f"{data[80]:d}.{data[81]:d}.{data[82]:d}"
    
    # RTD3 Resume Latency (bytes 84-87)
    result['rtd3r'] = str(struct.unpack('<I', data[84:88])[0])
    
    # RTD3 Entry Latency (bytes 88-91)
    result['rtd3e'] = str(struct.unpack('<I', data[88:92])[0])
    
    # Optional Asynchronous Events Supported (bytes 92-95)
    result['oaes'] = f"0x{struct.unpack('<I', data[92:96])[0]:08x}"
    
    # Controller Attributes (bytes 96-99)
    result['ctratt'] = f"0x{struct.unpack('<I', data[96:100])[0]:08x}"
    
    # Read Recovery Levels Supported (bytes 100-101)
    result['rrls'] = f"0x{data[100] | (data[101] << 8):04x}"
    
    # Total NVM Capacity (bytes 128-143)
    result['tnvmcap'] = str(struct.unpack('<Q', data[128:136])[0])
    
    # Unallocated NVM Capacity (bytes 144-159)
    result['unvmcap'] = str(struct.unpack('<Q', data[144:152])[0])
    
    # Optional Admin Command Support (bytes 256-257)
    result['oacs'] = f"0x{data[256] | (data[257] << 8):04x}"
    
    # Abort Command Limit (byte 258)
    result['acl'] = str(data[258])
    
    # Async Event Request Limit (byte 259)
    result['aerl'] = str(data[259])
    
    # Firmware Updates (byte 260)
    result['frmw'] = f"0x{data[260]:02x}"
    
    # Log Page Attributes (byte 261)
    result['lpa'] = f"0x{data[261]:02x}"
    
    # Error Log Page Entries (byte 262)
    result['elpe'] = str(data[262])
    
    # Power State Descriptors (bytes 2048-3071)
    power_states = []
    for i in range(32):  # 32 power states
        offset = 2048 + (i * 32)
        mp = struct.unpack('<H', data[offset:offset+2])[0]  # Max Power
        if mp > 0:  # Only include non-zero power states
            power_states.append(f"PS{i}: {mp}mW")
    result['power_states'] = ", ".join(power_states)

    return key_value_to_string(result)


def parser_nvme_identify(cmd: NvmeCmdObj, buffer):
    cns = cmd.cdws[10] & 0xFF
    if cns == NVME_ID_CNS_CTRL:
        return parser_nvme_id_ctrler(cmd, buffer)
    elif cns == NVME_ID_CNS_NS:
        return parser_nvme_id_ns(cmd, buffer)
    return None


def parser_get_log_page_smart(cmd: NvmeCmdObj, data):
    result = {}
    
    # Critical Warning
    critical_warning = data[0]
    warning_bits = []
    if critical_warning & 0x01:
        warning_bits.append("Available Spare")
    if critical_warning & 0x02:
        warning_bits.append("Temperature")
    if critical_warning & 0x04:
        warning_bits.append("Media")
    if critical_warning & 0x08:
        warning_bits.append("Read Only")
    if critical_warning & 0x10:
        warning_bits.append("Volatile Memory Backup")
    result['critical_warning'] = f"0x{critical_warning:02x} ({', '.join(warning_bits) if warning_bits else 'No Warnings'})"
    
    # Temperature Values
    composite_temp = struct.unpack('<H', data[1:3])[0]
    result['composite_temp'] = f"{composite_temp - 273 if composite_temp > 0 else 0}°C"
    
    # Available Spare
    result['available_spare'] = f"{data[3]}%"
    
    # Available Spare Threshold
    result['available_spare_threshold'] = f"{data[4]}%"
    
    # Percentage Used
    result['percentage_used'] = f"{data[5]}%"
    
    # Data Units Read
    data_units_read = struct.unpack('<Q', data[32:40])[0]
    result['data_units_read'] = f"{data_units_read} ({data_units_read * 512 // (1024*1024)} MB)"
    
    # Data Units Written
    data_units_written = struct.unpack('<Q', data[48:56])[0]
    result['data_units_written'] = f"{data_units_written} ({data_units_written * 512 // (1024*1024)} MB)"
    
    # Host Read Commands
    result['host_reads'] = str(struct.unpack('<Q', data[64:72])[0])
    
    # Host Write Commands
    result['host_writes'] = str(struct.unpack('<Q', data[80:88])[0])
    
    # Controller Busy Time
    result['controller_busy_time'] = f"{struct.unpack('<Q', data[96:104])[0]} minutes"
    
    # Power Cycles
    result['power_cycles'] = str(struct.unpack('<Q', data[112:120])[0])
    
    # Power On Hours
    result['power_on_hours'] = f"{struct.unpack('<Q', data[128:136])[0]} hours"
    
    # Unsafe Shutdowns
    result['unsafe_shutdowns'] = str(struct.unpack('<Q', data[144:152])[0])
    
    # Media Errors
    result['media_errors'] = str(struct.unpack('<Q', data[160:168])[0])
    
    # Number of Error Information Log Entries
    result['num_err_log_entries'] = str(struct.unpack('<Q', data[176:184])[0])
    
    # Warning Composite Temperature Time
    result['warning_temp_time'] = f"{struct.unpack('<I', data[192:196])[0]} minutes"
    
    # Critical Composite Temperature Time
    result['critical_temp_time'] = f"{struct.unpack('<I', data[196:200])[0]} minutes"
    
    # Temperature Sensors (if available)
    for i in range(8):
        temp = struct.unpack('<H', data[3+i*2:5+i*2])[0]
        if temp > 0:  # Only include non-zero temperature sensors
            result[f'temp_sensor_{i}'] = f"{temp - 273 if temp > 0 else 0}°C"

    return key_value_to_string(result)



def parser_get_log_page(cmd: NvmeCmdObj, buffer):
    lid = cmd.cdws[10] & 0xFF
    if lid == NVME_LOG_SMART:
        return parser_get_log_page_smart(cmd, buffer)
    
def parser_nvme_cmd(cmd: NvmeCmdObj, buffer):

    opc = cmd.cdws[0] & 0xFF
    if opc == NVME_ADMIN_IDENTIFY:
        return parser_nvme_identify(cmd, buffer)
    elif opc == NVME_ADMIN_GET_LOG_PAGE:
        return parser_get_log_page(cmd, buffer)
    

    return None

