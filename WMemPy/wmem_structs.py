import ctypes
import win32process
from ctypes.wintypes import *

PVOID = LPVOID
SIZE_T = ctypes.c_size_t


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    """https://msdn.microsoft.com/en-us/library/aa366775"""
    _fields_ = (('BaseAddress', PVOID),
                ('AllocationBase',    PVOID),
                ('AllocationProtect', DWORD),
                ('RegionSize', SIZE_T),
                ('State',   DWORD),
                ('Protect', DWORD),
                ('Type',    DWORD))


class MODULEINFO(ctypes.Structure):
    _fields_ = (("lpBaseOfDll",     LPVOID),
                ("SizeOfImage",     DWORD),
                ("EntryPoint",      LPVOID))
LPMODULEINFO = ctypes.POINTER(MODULEINFO)
ctypes.windll.psapi.GetModuleInformation.argtypes = [HANDLE, HMODULE, ctypes.POINTER(MODULEINFO), DWORD]


class ProcPage:
    """
    Represents a single memory page of a process.
    """
    def __init__(self, base, size):
        self.base_address = base
        self.size = size


class ProcModule:
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
