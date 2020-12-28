import ctypes
import numpy as np
import sys
np.set_printoptions(threshold=np.inf)


class ProcScanner:
    """
    Allows to run scans above Scannables
    """
    def __init__(self, proc):
        self.process = proc

    def array_from_pattern(self, pattern, base, separator):
        pattern = pattern.replace('?', '-1')
        return np.array([int(x, base) for x in pattern.split(separator)])

    def is_subsequence(self, memory, pattern):
        i = 0
        j = 0
        n = len(memory)
        m = len(pattern)

        while (i < n and j < m):
            if (pattern[j] == -1 or memory[i] == pattern[j]):    
                i += 1
                j += 1
                if (j == m):
                    return i - m
            else:
                i = i - j + 1
                j = 0

        return -1

    def AOB_scan_arr(self, scannable_array, pattern, base=16, separator=' '):
        for scannable in scannable_array:
            result = self.AOB_scan(scannable, pattern, base, separator)
            if result >= 0:
                return result
        return -1

    def AOB_scan(self, scannable, pattern, base=16, separator=' '):
        to_find = self.array_from_pattern(pattern, base, separator)
        bounds = scannable.get_bounds()
        buffer = ctypes.create_string_buffer(bounds[1])
        bytes_read = ctypes.c_size_t()
        try:
            ctypes.windll.kernel32.ReadProcessMemory(self.process.get_handle(), bounds[0], buffer, bounds[1], ctypes.byref(bytes_read))
        except Exception:
            return -1
        if bytes_read.value != bounds[1]:
            return -1
        memory = np.ctypeslib.as_array(buffer).view(np.uint8)
        return self.is_subsequence(memory, to_find)
