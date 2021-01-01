import pytest
from flexmock import flexmock
from wmempy.wmem_cli import *
# Tests not covered here are covered by live memory tests


def test_array_from_where():
    """Test that array can be extracted from process"""
    moduleA = flexmock(get_name=lambda: 'dwm.exe')
    moduleB = flexmock(get_name=lambda: 'kernel32.dll')
    moduleC = flexmock(get_name=lambda: 'ntdll.dll')
    proc = flexmock(pages=[0,1,2],modules=[moduleA, moduleB, moduleC])
    result = array_from_where(proc, 'all')
    assert result == [0,1,2]
    result = array_from_where(proc, 'pages')
    assert result == [0,1,2]
    result = array_from_where(proc, None)
    assert result == [0,1,2]
    result = array_from_where(proc, 'modules')
    assert moduleA in result
    assert moduleB in result
    assert moduleC in result
    result = array_from_where(proc, 'dwm.exe')
    assert moduleA in result
    result = array_from_where(proc, 'kernel32.dll')
    assert moduleB in result
    result = array_from_where(proc, 'ntdll.dll')
    assert moduleC in result
    result = array_from_where(proc, '')
    assert result == []
    result = array_from_where(proc, 'nonsense')
    assert result == []
    result = array_from_where(proc, 'fake.dll')
    assert result == []

def test_readable():
    """Test that array can be converted to readable ASCII"""
    message = np.array([97,98,99,100,69,70,71,72])
    read_version = readable(message)
    assert read_version == 'abcdEFGH'

def test_memory_view_print(capsys):
    """Test that memory prints nicely"""
    memory = np.array([97,98,99,100,69,70,71,72,97,98,99,100,69,70,71,72])
    memory_view_print(memory, 0)
    captured = capsys.readouterr().out
    assert '0x0' in captured
    assert '[61 62 63 64 45 46 47 48 61 62 63 64 45 46 47 48]' in captured
    assert 'abcdEFGHabcdEFGH' in captured
    memory_view_print(memory, 4)
    captured = capsys.readouterr().out
    assert '0x0' in captured
    assert '[61 62 63 64 45 46 47 48 61 62 63 64 45 46 47 48]' in captured
    assert 'abcdEFGHabcdEFGH' in captured
    memory = np.array([97,98,99,100,69,70,71,72,97,98,99,100,69,70,71,72,98,99,100,101,70,71,72,73,98,99,100,101,70,71,72,73])
    memory_view_print(memory, 0)
    captured = capsys.readouterr().out
    assert '0x0' in captured
    assert '[61 62 63 64 45 46 47 48 61 62 63 64 45 46 47 48]' in captured
    assert 'abcdEFGHabcdEFGH' in captured
    assert '0x10' in captured
    assert '[62 63 64 65 46 47 48 49 62 63 64 65 46 47 48 49]' in captured
    assert 'bcdeFGHIbcdeFGHI' in captured
