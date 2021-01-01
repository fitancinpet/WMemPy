import pytest
from wmempy.wmem_system import WinSys

@pytest.mark.parametrize('process', ('System Idle Process', 'System', 'dwm.exe', 'explorer.exe'))
def test_winsys_process_list(process):
    """Test whether there are common processes in process list"""
    plist = WinSys.process_list()
    process_in_plist = [proc for proc in plist if proc[1] == process]
    assert len(process_in_plist) > 0
    assert len(plist) > 3

@pytest.mark.parametrize('process', ('System Idle Process', 'System', 'dwm.exe', 'explorer.exe'))
def test_winsys_process_list_print(capsys, process):
    """Test whether there are common processes in process list print"""
    WinSys.process_list_print()
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert 'Process list:' in lines[0]
    assert '-------------------' in lines[1]
    assert process in captured.out