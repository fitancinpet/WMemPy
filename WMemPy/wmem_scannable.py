import win32process
import ctypes
from wmem_structs import MODULEINFO
import os

class ProcScannable:
    """
    Scannable interface has to be implemented if you want to execute scans on the class.
    """
    def get_bounds(self):
        raise NotImplementedError('Interface ProcScannable not implemented.')

    def read(self):
        raise NotImplementedError('Interface ProcScannable not implemented.')

    def read_dtype(self):
        raise NotImplementedError('Interface ProcScannable not implemented.')

class ProcPage(ProcScannable):
    """
    Represents a single virtual memory page of a process.
    """
    def __init__(self, proc, base, size):
        self.process = proc
        self.base_address = base
        self.size = size

    # Page is represnted by base address and size only, this should never represent physical memory page
    def get_bounds(self):
        return [self.base_address, self.size]

    # Read the entire page
    def read(self):
        return self.process.reader.byte_arr(self.base_address, self.size)

    # Read any data type from the page
    def read_dtype(self, address, dtype):
        return self.process.reader.dtype(self.base_address + address, dtype)

    def print(self):        
        print(f'{hex(self.base_address)} - {hex(self.base_address + self.size)}')


class ProcModule(ProcScannable):
    """
    Represents a single module loaded by process.
    """
    def __init__(self, proc, handle):
        self.process = proc
        self.handle = handle
        self.path = win32process.GetModuleFileNameEx(self.process.handle, self.handle)
        mi = MODULEINFO()
        ctypes.windll.psapi.GetModuleInformation(self.process.get_handle(), self.handle, ctypes.byref(mi), ctypes.sizeof(mi))
        self.base_address = mi.lpBaseOfDll
        self.size = mi.SizeOfImage
        self.entry = mi.EntryPoint

    # Module has path (name), base address, size and entrypoint
    # Entrypoint is what is called when the dll/so is loaded, but it can be obfuscated
    def get_bounds(self):
        return [self.base_address, self.size]

    # Read the entire module
    def read(self):
        return self.process.reader.byte_arr(self.base_address, self.size)

    # Read any data type from the page
    def read_dtype(self, address, dtype):
        return self.process.reader.dtype(self.base_address + address, dtype)

    def get_name(self):
        return os.path.basename(self.path)

    def print(self):        
        print(self.path)
        print(f'{hex(self.base_address)} - {hex(self.base_address + self.size)}')
