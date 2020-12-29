import ctypes
import numpy as np

class ProcReader:
    """
    Allows to read the memory of a process
    """
    def __init__(self, proc):
        self.process = proc

    # Read a byte array of the process
    def byte_arr(self, address, size):
        # Allocate buffer for single ReadProcessMemory operation
        buffer = ctypes.create_string_buffer(size)
        # How many bytes were read by the syscall
        bytes_read = ctypes.c_size_t()
        # RPM has to be called in a single call because it is extremely inefficient syscall
        # In regular WinApi, if the call fails, it returns 0 (you use GetLastError to get the problem)
        # In ctypes version, it can throw exception as well as fail with 0 and also partially fail, what a fun!
        try:
            if not ctypes.windll.kernel32.ReadProcessMemory(self.process.get_handle(), address, buffer, size, ctypes.byref(bytes_read)):
                # Regular fail (for example called on null handle)
                return None
        except Exception:
            # Exception fail I haven't been able to produce
            return None
        if bytes_read.value != size:
            # Partial RMP fail, only some data are read, this should not happen normally, only in the kernel call versions (Zw)
            return None
        # Convert the char buffer to numpy array
        return np.ctypeslib.as_array(buffer).view(np.uint8)

    # Read any ctypes data type of the process
    def dtype(self, address, dtype):
        # Get reference for ReadProcessMemory operation
        buffer = ctypes.byref(dtype)
        # Get the amount of bytes to be read
        size = ctypes.sizeof(dtype)
        # How many bytes were read by the syscall
        bytes_read = ctypes.c_size_t()
        # RPM has to be called in a single call because it is extremely inefficient syscall
        # In regular WinApi, if the call fails, it returns 0 (you use GetLastError to get the problem)
        # In ctypes version, it can throw exception as well as fail with 0 and also partially fail, what a fun!
        try:
            if not ctypes.windll.kernel32.ReadProcessMemory(self.process.get_handle(), address, buffer, size, ctypes.byref(bytes_read)):
                # Regular fail (for example called on null handle)
                return None
        except Exception:
            # Exception fail I haven't been able to produce
            return None
        if bytes_read.value != size:
            # Partial RMP fail, only some data are read, this should not happen normally, only in the kernel call versions (Zw)
            return None
        # Return the value
        return dtype.value

        

class ProcWriter:
    """
    Allows to write the memory of a process
    """
    def __init__(self, proc):
        self.process = proc

    # Write any ctypes data type into the process
    def dtype(self, address, dtype):
        # Get reference for WriteProcessMemory operation
        buffer = ctypes.byref(dtype)
        # Get the amount of bytes to be written
        size = ctypes.sizeof(dtype)
        # How many bytes were written by the syscall
        bytes_read = ctypes.c_size_t()
        # WPM has to be called in a single call because it is extremely inefficient syscall
        # In regular WinApi, if the call fails, it returns 0 (you use GetLastError to get the problem)
        # In ctypes version, it can throw exception as well as fail with 0 and also partially fail, what a fun!
        try:
            if not ctypes.windll.kernel32.WriteProcessMemory(self.process.get_handle(), address, buffer, size, ctypes.byref(bytes_read)):
                # Regular fail (for example called on null handle)
                return None
        except Exception:
            # Exception fail I haven't been able to produce
            return None
        if bytes_read.value != size:
            # Partial WPM fail, only some data are written, this should not happen normally, only in the kernel call versions (Zw)
            return None
        # On successful write, return the value written
        return dtype.value
    