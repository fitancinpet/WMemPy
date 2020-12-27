import win32process
import ctypes
from wmem_structs import MODULEINFO

class Scannable:
    def get_bounds(self):
        raise NotImplementedError('Interface Scannable not implemented.')

class ProcPage(Scannable):
    """
    Represents a single memory page of a process.
    """
    def __init__(self, base, size):
        self.base_address = base
        self.size = size

    def get_bounds(self):
        return [self.base_address, self.size]

    def print(self):        
        print(f'{hex(self.base_address)} - {hex(self.base_address + self.size)}')


class ProcModule(Scannable):
    """
    Represents a single memory page of a process.
    """
    def __init__(self, proc_handle, handle):
        self.handle = handle
        self.path = win32process.GetModuleFileNameEx(proc_handle, self.handle)
        mi = MODULEINFO()
        ctypes.windll.psapi.GetModuleInformation(proc_handle.__int__(), self.handle, ctypes.byref(mi), ctypes.sizeof(mi))
        self.base_address = mi.lpBaseOfDll
        self.size = mi.SizeOfImage
        self.entry = mi.EntryPoint

    def get_bounds(self):
        return [self.base_address, self.size]

    def print(self):        
        print(self.path)
        print(f'{hex(self.base_address)} - {hex(self.base_address + self.size)}')
