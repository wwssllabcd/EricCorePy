import ctypes
from ctypes import wintypes

# 定义常量
INVALID_HANDLE_VALUE = -1
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x00000001  
FILE_SHARE_WRITE = 0x00000002  

OPEN_EXISTING = 3
IOCTL_STORAGE_QUERY_PROPERTY = 0x002D1400  # 控制代码，用于查询设备属性

WinBusTypeUsb = 0x07

CRLF = "\r\n"

# 定义 STORAGE_PROPERTY_QUERY 结构
class STORAGE_PROPERTY_QUERY(ctypes.Structure):
    _fields_ = [
        ("PropertyId", wintypes.DWORD),  # 查询的属性ID
        ("QueryType", wintypes.DWORD),   # 查询类型（如 StandardQuery）
        ("AdditionalParameters", wintypes.BYTE * 1)  # 其他参数（未使用）
    ]

# 定义 STORAGE_DEVICE_DESCRIPTOR 结构
class STORAGE_DEVICE_DESCRIPTOR(ctypes.Structure):
    _fields_ = [
        ("Version", wintypes.DWORD),         # 版本号
        ("Size", wintypes.DWORD),            # 结构体大小
        ("DeviceType", wintypes.BYTE),       # 设备类型
        ("DeviceTypeModifier", wintypes.BYTE),  # 设备类型修饰符
        ("RemovableMedia", wintypes.BYTE),   # 是否可移动设备
        ("CommandQueueing", wintypes.BYTE),  # 是否支持命令排队
        ("VendorIdOffset", wintypes.DWORD),  # 供应商ID的偏移
        ("ProductIdOffset", wintypes.DWORD), # 产品ID的偏移
        ("ProductRevisionOffset", wintypes.DWORD),  # 产品版本偏移
        ("SerialNumberOffset", wintypes.DWORD),     # 序列号偏移
        ("BusType", wintypes.BYTE),           # 总线类型（如 USB、SCSI 等）
        ("RawPropertiesLength", wintypes.DWORD),  # 原始属性数据长度
        ("RawDeviceProperties", wintypes.BYTE * 1)  # 原始设备属性
    ]

class DeviceInfo:
    def __init__(self):
        self.devicePath = ""
        self.deviceHandle = None

        self.productId = ""
        self.SerialNumber = ""
        self.busType = 0xFF

    def __str__(self) -> str:
        msg = "DeviceInfo: " + CRLF
        msg += "productId = " + self.productId + CRLF
        msg += "SerialNumber = " + self.SerialNumber + CRLF
        msg += "busType = " + str(self.busType) + CRLF
        return msg

def _gen_physical_Drive_string():
    paths = []
    for i in range(32):
        paths.append(r"\\.\PhysicalDrive" + str(i))
    return paths


def open_device(device_path):
    return ctypes.windll.kernel32.CreateFileW(
        device_path,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,  # 共享模式
        None,  # 安全属性
        OPEN_EXISTING,
        0,  # 文件属性和标志
        None  # 模板文件句柄
    )

def close_device(handle):
    if handle is not None and handle != INVALID_HANDLE_VALUE:
        if not ctypes.windll.kernel32.CloseHandle(handle):
            print("CloseHandle error")

def get_storage_device_descriptor(device):
    # 设置 STORAGE_PROPERTY_QUERY 结构
    query = STORAGE_PROPERTY_QUERY()
    query.PropertyId = 0  # 查询 DeviceProperty
    query.QueryType = 0   # 标准查询

    # 准备输出缓冲区，用于存储返回的 STORAGE_DEVICE_DESCRIPTOR
    output_buffer_size = 1024
    output_buffer = ctypes.create_string_buffer(output_buffer_size)

    # 调用 DeviceIoControl 发送 IOCTL_STORAGE_QUERY_PROPERTY 命令
    bytes_returned = wintypes.DWORD()
    success = ctypes.windll.kernel32.DeviceIoControl(
        device,
        IOCTL_STORAGE_QUERY_PROPERTY,
        ctypes.byref(query),  # 输入缓冲区（查询结构）
        ctypes.sizeof(query),  # 输入缓冲区大小
        output_buffer,  # 输出缓冲区（存储描述符）
        output_buffer_size,  # 输出缓冲区大小
        ctypes.byref(bytes_returned),  # 返回的字节数
        None  # 重叠结构
    )

    if not success:
        return None

    # 解析返回的 STORAGE_DEVICE_DESCRIPTOR 结构
    device_descriptor = STORAGE_DEVICE_DESCRIPTOR.from_buffer_copy(output_buffer)
    return (device_descriptor, output_buffer)

def extract_string(offset, output_buffer):
    if offset != 0 and offset < len(output_buffer):
        return ctypes.string_at(output_buffer[offset:]).split(b'\x00', 1)[0].decode()
    return None

def get_device_desc(device):
    res = get_storage_device_descriptor(device)
    if res == None:
        return None
    
    desc: STORAGE_DEVICE_DESCRIPTOR
    buffer: ctypes.Array
    desc, buffer = res

    d = DeviceInfo()

    d.productId = extract_string(desc.ProductIdOffset, buffer)
    d.SerialNumber = extract_string(desc.SerialNumberOffset, buffer)
    d.busType = desc.BusType
    return d

def get_device_handle(filterFun = None):
    deviceStrs = _gen_physical_Drive_string()
    devices = []
    for devStr in deviceStrs:
        deviceHandle = open_device(devStr)
        if deviceHandle == -1:
            continue

        deviceInfo = DeviceInfo()
        deviceInfo = get_device_desc(deviceHandle)
        if filterFun != None:
            if filterFun(deviceInfo) == False:
                close_device(deviceHandle)
                continue
        
        deviceInfo.devicePath = devStr
        deviceInfo.deviceHandle = deviceHandle

        devices.append(deviceInfo)
    return devices
