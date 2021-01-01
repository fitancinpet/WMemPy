import ctypes
from flexmock import flexmock
import numpy as np
import os
import pytest
import subprocess
from wmempy.wmem_scannable import ProcScannable, ProcPage, ProcModule
from wmempy.wmem_process import WinProc
# Tests not covered here are covered by live memory tests


def test_winsys_proc_scannable():
    """Test that interface is abstract"""
    scannable = ProcScannable()
    with pytest.raises(NotImplementedError):
        scannable.get_bounds()
    with pytest.raises(NotImplementedError):
        scannable.read()
    with pytest.raises(NotImplementedError):
        scannable.read_from(0)
    with pytest.raises(NotImplementedError):
        scannable.read_dtype(0, ctypes.c_int())
    with pytest.raises(NotImplementedError):
        scannable.write_dtype(0, ctypes.c_int())

def get_mock_proc():
    memory_op = flexmock(byte_arr=lambda a, s: np.ctypeslib.as_array([a, s]).view(np.uint8),
                         dtype=lambda a, t: np.ctypeslib.as_array([a, ctypes.sizeof(t)]).view(np.uint8))
    proc = flexmock(reader=memory_op,writer=memory_op)
    return proc

def test_winsys_proc_page_mocked(capsys):
    """Test that ProcPage delegates calls correctly"""
    proc = get_mock_proc()
    scannable = ProcPage(proc, 10, 60)
    scannable.print()
    captured = capsys.readouterr().out
    assert hex(10) in captured
    assert hex(10 + 60) in captured
    data = scannable.read()
    assert 10 in data
    assert 60 in data
    data = scannable.read_from(20)
    assert (10 + 20) in data
    assert (60 - 20) in data
    dtype = ctypes.c_int()
    data = scannable.read_dtype(30, dtype)
    assert (10 + 30) in data
    assert ctypes.sizeof(dtype) in data
    dtype = ctypes.c_int()
    data = scannable.write_dtype(30, dtype)
    assert (10 + 30) in data
    assert ctypes.sizeof(dtype) in data

def test_winsys_proc_page_live(request):
    """Test that ProcPage works with live memory"""
    exe_name = 'WMemPy_test_app.exe'
    exe_path = os.path.join(request.fspath.dirname, 'exes', exe_name)
    process = subprocess.Popen([exe_path])
    proc = WinProc(exe_name)
    assert proc.process_valid()
    # Live memory start

    # Live memory end
    process.terminate()
    assert not proc.process_valid()
