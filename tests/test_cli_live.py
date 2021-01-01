import pytest
import ctypes
from helpers import run_process, get_example_app, hand_example_app
# These tests are running on live memory (utilizing common Windows processes and example exes)
# These tests also test if your system can use the application (if your Windows is compatible)


def test_win_proc_basic_live(request, capsys):
    """Test basic WinProc functionality"""
    proc, live_app = get_example_app(request)
    # Live memory start
    
    # Live memory end
    hand_example_app(proc, live_app)
