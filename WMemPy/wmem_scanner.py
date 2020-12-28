import ctypes
import numpy as np
import sys


class ProcScanner:
    """
    Allows to run scans above Scannables
    """
    def __init__(self, proc):
        self.process = proc

    # Creates a numpy array from string, wildcard can be either * or ?
    # Supports any base and any separator for use across all pattern styles
    def array_from_pattern(self, pattern, base, separator):
        pattern = pattern.replace('?', '-1')
        pattern = pattern.replace('*', '-1')
        return np.array([int(x, base) for x in pattern.split(separator)])

    # Creates a numpy array from ASCII string
    def array_from_ascii(self, ascii):
        return np.array([ord(c) for c in ascii])

    # Sequence contains subsequence problem, linear solution
    def is_subsequence(self, memory, pattern):
        i = 0
        j = 0
        n = len(memory)
        m = len(pattern)

        # While not at the end of memory and not at the end of pattern
        while (i < n and j < m):
            # If wildcard or chars match, move both iterators
            if (pattern[j] == -1 or memory[i] == pattern[j]):    
                i += 1
                j += 1
                # If whole pattern was iterated over, success
                if (j == m):
                    return i - m
            # If chars don't match, return back where match was first found
            else:
                i = i - j + 1
                j = 0

        # If we went through the whole thing without success, fail
        return -1

    def byte_scan(self, scannable, byte_arr):
        # Memory bounds to scan (either module or valid memory page)
        bounds = scannable.get_bounds()
        # Allocate buffer for single ReadProcessMemory operation
        buffer = ctypes.create_string_buffer(bounds[1])
        # How many bytes were read by the syscall
        bytes_read = ctypes.c_size_t()
        # RPM has to be called in a single call because it is extremely inefficient syscall
        # In regular WinApi, if the call fails, it returns 0 (you use GetLastError to get the problem)
        # In ctypes version, it can throw exception as well as fail with 0 and also partially fail, what a fun!
        try:
            if not ctypes.windll.kernel32.ReadProcessMemory(self.process.get_handle(), bounds[0], buffer, bounds[1], ctypes.byref(bytes_read)):
                # Regular fail (for example called on null handle)
                return -1
        except Exception:
            # Exception fail I haven't been able to produce
            return -1
        if bytes_read.value != bounds[1]:
            # Partial RMP fail, only some data are read, this should not happen normally, only in the kernel call versions (Zw)
            return -1
        # Convert the char buffer to numpy array
        memory = np.ctypeslib.as_array(buffer).view(np.uint8)
        # Check if pattern is in memory
        return self.is_subsequence(memory, byte_arr)

    # Looks for a pattern inside an array of Scannables of the current process
    def AOB_scan_arr(self, scannable_array, pattern, base=16, separator=' '):
        for scannable in scannable_array:
            result = self.AOB_scan(scannable, pattern, base, separator)
            if result >= 0:
                return result
        return -1

    # Checks if memory range contains given pattern
    def AOB_scan(self, scannable, pattern, base=16, separator=' '):
        # Generate numpy array from pattern string
        to_find = self.array_from_pattern(pattern, base, separator)
        return self.byte_scan(scannable, to_find)
        

    # Looks for an ASCII string inside an array of Scannables of the current process
    def ASCII_scan_arr(self, scannable_array, ascii):
        for scannable in scannable_array:
            result = self.ASCII_scan(scannable, ascii)
            if result >= 0:
                return result
        return -1

    # Checks if memory range contains given ASCII string
    def ASCII_scan(self, scannable, ascii):
        # Generate numpy array from ASCII string
        to_find = self.array_from_ascii(ascii)
        return self.byte_scan(scannable, to_find)
