from wmem_system import WinSys
from wmem_structs import MEMORY_BASIC_INFORMATION, MODULEINFO
from wmem_scannable import ProcPage, ProcModule
from wmem_scanner import ProcScanner
import win32api
import win32process
import win32con
import pywintypes
from ctypes import *
from ctypes.wintypes import *


class WinProc:
    """
    Represents a single Windows Process.
    """
    def __init__(self, process_name, process_id = -1):
        filtered_proc_list = self.__filter_processes(process_name, process_id)
        if len(filtered_proc_list) == 1:
            self.proc_id = filtered_proc_list[0][0]
            self.proc_name = filtered_proc_list[0][1]
            try:
                self.handle = win32api.OpenProcess(WinSys.REQUIRED_ACCESS, 0, self.proc_id)
            except pywintypes.error:
                raise Exception('Access denied.', filtered_proc_list)
        elif len(filtered_proc_list) == 0:
            raise Exception('Process not found.')
        else:
            raise Exception('Unable to determine unique process from name.', filtered_proc_list)
        self.scanner = ProcScanner(self)
        self.__post_init__()
        self.gather_info()

    def __post_init__(self):
        ctypes.windll.kernel32.VirtualQueryEx.argtypes = [HANDLE, LPCVOID, c_size_t, c_size_t]
        ctypes.windll.psapi.GetModuleInformation.argtypes = [HANDLE, HMODULE, ctypes.POINTER(MODULEINFO), DWORD]
        ctypes.windll.kernel32.ReadProcessMemory.argtypes = [HANDLE, LPCVOID, LPCVOID, c_size_t, ctypes.POINTER(c_size_t)]

    def __filter_processes(self, process_name, process_id):
        proc_list = WinSys.process_list()
        if process_id == -1:
            filtered_proc_list = [proc for proc in proc_list if proc[1] == process_name]
        else:
            filtered_proc_list = [proc for proc in proc_list if proc[0] == process_id]
        return filtered_proc_list

    def print_process(self):
        print(f'{self.proc_name}')
        print(f'PID: {self.proc_id}')
        print(f'Handle: {self.get_handle()}')

    def print_modules(self):
        print('Module list:')
        for module in self.modules:
            module.print()
            print('^^^^^^^^^^^^')

    def print_pages(self):
        print('Memory page list:')
        for page in self.pages:
            page.print()
        print('------------')

    def print_process_detailed(self):
        self.print_process()
        self.print_modules()
        self.print_pages()

    def gather_info(self):
        if not self.process_valid():
            raise Exception('Process no longer exists.')
        self.get_modules()
        self.get_pages()

    def process_valid(self):
        return self.handle and win32process.GetExitCodeProcess(self.handle) == WinSys.PROCESS_RUNNING

    def get_modules(self):
        self.modules = []
        for module in win32process.EnumProcessModulesEx(self.handle, win32process.LIST_MODULES_ALL):
            self.modules.append(ProcModule(self.handle, module))

    def get_pages(self):
        self.pages = []
        current_base = 0
        mbi = MEMORY_BASIC_INFORMATION()
        while ctypes.windll.kernel32.VirtualQueryEx(self.get_handle(), current_base, ctypes.addressof(mbi), ctypes.sizeof(mbi)) > 0:
            if mbi.State == win32con.MEM_COMMIT and mbi.Protect != win32con.PAGE_NOACCESS and mbi.Protect != win32con.PAGE_GUARD:
                self.pages.append(ProcPage(mbi.BaseAddress, mbi.RegionSize))
            current_base += mbi.RegionSize

    def get_handle(self):
        return self.handle.__int__()