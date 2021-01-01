import ctypes
from flexmock import flexmock
import numpy as np
import os
import pytest
import subprocess
from wmempy.wmem_scannable import ProcScannable, ProcPage, ProcModule
from wmempy.wmem_process import WinProc

def test_winsys_proc_scannable():
    """Test that interface is abstract"""
