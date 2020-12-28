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

class ProcPage(ProcScannable):
    """
    Represents a single virtual memory page of a process.
    """
    def __init__(self, base, size):
        self.base_address = base
        self.size = size

    # Page is represnted by base address and size only, this should never represent physical memory page
    def get_bounds(self):
        return [self.base_address, self.size]

    def print(self):        
        print(f'{hex(self.base_address)} - {hex(self.base_address + self.size)}')


class ProcModule(ProcScannable):
    """
    Represents a single module loaded by process.
    """
    def __init__(self, proc_handle, handle):
        self.handle = handle
        self.path = win32process.GetModuleFileNameEx(proc_handle, self.handle)
        mi = MODULEINFO()
        ctypes.windll.psapi.GetModuleInformation(proc_handle.__int__(), self.handle, ctypes.byref(mi), ctypes.sizeof(mi))
        self.base_address = mi.lpBaseOfDll
        self.size = mi.SizeOfImage
        self.entry = mi.EntryPoint

    # Module has path (name), base address, size and entrypoint
    # Entrypoint is what is called when the dll/so is loaded, but it can be obfuscated
    def get_bounds(self):
        return [self.base_address, self.size]

    def get_name(self):
        return os.path.basename(self.path)

    def print(self):        
        print(self.path)
        print(f'{hex(self.base_address)} - {hex(self.base_address + self.size)}')
