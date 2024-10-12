
import ctypes

def get_ctype_addr(byteArray: bytearray):
    # make ctype buffer 
    ctypeBuf = ctypes.c_char * len(byteArray)

    # from_buffer 方法不會複製資料，它只是建立了一個新的 ctypes object，使得這個 object 可以以 ctypes 支援的方式訪問 byteArray 的底層記憶體
    # 直接訪問底層資料: from_buffer 允許你在不修改資料結構的情況下，直接將低層緩衝區暴
    newCtypeBuf = ctypeBuf.from_buffer(byteArray)
    return ctypes.addressof(newCtypeBuf)


def ctype_struct_to_bytearray(ctypeObj, byteArrSize=None):
    objLen = ctypes.sizeof(ctypeObj)

    if byteArrSize == None:
        byteArrSize = objLen

    if objLen > byteArrSize:
        raise "objLen ofb"
    
    byteArr = bytearray(byteArrSize)

    # get real mem addr
    byteArrRef = (ctypes.c_uint8 * byteArrSize).from_buffer(byteArr)

    # copy ctypeObj to bytearray
    ctypes.memmove(byteArrRef, ctypes.byref(ctypeObj), objLen)
    return byteArr

