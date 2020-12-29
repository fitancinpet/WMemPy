from win32com.client import GetObject
import win32con

class WinSys:
    """
    Helper class for common WinApi functionalities.
    """
    # Read memory | Write memory | Write memory again (both required) | Query memory pages (technically not required since we have Read memory)
    REQUIRED_ACCESS = win32con.PROCESS_VM_READ | win32con.PROCESS_VM_WRITE | win32con.PROCESS_VM_OPERATION | win32con.PROCESS_QUERY_INFORMATION
    PROCESS_RUNNING = win32con.STILL_ACTIVE

    # Retrieve all running processes (PID, name)
    @classmethod
    def process_list(cls):
        # https://docs.microsoft.com/en-us/windows/win32/wmisdk/calling-a-wmi-method
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        process_list = [(p.Properties_("ProcessID").Value, p.Properties_("Name").Value) for p in processes]
        return process_list

    # Print all running processes (PID, name)
    @classmethod
    def process_list_print(cls):
        print('Process list:')
        print('-------------------')
        for x in cls.process_list():
            print(f'{x[1]} ({x[0]})')
        print('-------------------')