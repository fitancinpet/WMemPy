import ctypes
import numpy as np
import sys


class ProcScanner:
    """
    Allows to run scans on Scannables
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
        return None

    def byte_scan(self, scannable, byte_arr):
        # Read the scannable's memory
        memory = scannable.read()
        if memory is None:
            return None
        # Check if pattern is in memory
        return self.is_subsequence(memory, byte_arr)

    # Looks for a pattern inside an array of Scannables of the current process
    def AOB_scan_arr(self, scannable_array, pattern, base=16, separator=' '):
        for scannable in scannable_array:
            result = self.AOB_scan(scannable, pattern, base, separator)
            if not (result is None):
                return result, scannable
        return None, None

    # Checks if memory range contains given pattern
    def AOB_scan(self, scannable, pattern, base=16, separator=' '):
        # Generate numpy array from pattern string
        to_find = self.array_from_pattern(pattern, base, separator)
        return self.byte_scan(scannable, to_find)
        

    # Looks for an ASCII string inside an array of Scannables of the current process
    def ASCII_scan_arr(self, scannable_array, ascii):
        for scannable in scannable_array:
            result = self.ASCII_scan(scannable, ascii)
            if not (result is None):
                return result, scannable
        return None, None

    # Checks if memory range contains given ASCII string
    def ASCII_scan(self, scannable, ascii):
        # Generate numpy array from ASCII string
        to_find = self.array_from_ascii(ascii)
        return self.byte_scan(scannable, to_find)

    # Creates a list of all ASCII strings in an array of scannables
    def ASCII_list_arr(self, scannable_arr, symbols=False, min_length=3):
        result = []
        for scannable in scannable_arr:
            tmp = self.ASCII_list(scannable, symbols, min_length)
            if not (tmp is None) and len(tmp) > 0:
                result.append(tmp)
        return [item for sublist in result for item in sublist]

    # Creates a list of all ASCII strings in a scannable
    def ASCII_list(self, scannable, symbols=False, min_length=3):
        result = []        
        # Read the scannable's memory
        memory = scannable.read()
        if memory is None:
            return None
        # For symbols, only remove special symbols like line endings and reserved bytes
        if symbols:
            condition = (memory <= 32) | (memory >= 127)
        # Otherwise, only allow a-z A-Z 0-9
        else:
            condition = (memory <= 47) | ((memory >= 58) & (memory <= 64)) | ((memory >= 91) & (memory <= 96)) | (memory >= 123)
        # Apply condition
        memory = np.where(condition, 0, memory)

        # Get bitmap for zero elements
        iszero = np.concatenate(([0], np.greater(memory, 0).view(np.int8), [0]))
        # Diff gets us boundaries
        absdiff = np.abs(np.diff(iszero))
        # Split boundaries into separate array for each word
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        
        # Iterate over all potential words
        for word in ranges:
            # Filter by length
            if word[1] - word[0] >= min_length:
                # Get the ASCII byte array
                ascii_word = memory[word[0]:word[1]]
                # Convert it to string and append it to results
                result.append("".join([chr(item) for item in ascii_word]))

        return result
