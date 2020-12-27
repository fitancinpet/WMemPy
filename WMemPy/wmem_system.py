from win32com.client import GetObject
import win32con

class WinSys:
    """
    Helper class for common WinApi functionalities.
    """

    REQUIRED_ACCESS = win32con.PROCESS_VM_OPERATION | win32con.PROCESS_VM_READ | win32con.PROCESS_VM_WRITE | win32con.PROCESS_QUERY_INFORMATION
    PROCESS_RUNNING = win32con.STILL_ACTIVE

    @classmethod
    def process_list(cls):
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        process_list = [(p.Properties_("ProcessID").Value, p.Properties_("Name").Value) for p in processes]
        return process_list