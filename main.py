import sys
sys.path.insert(1, 'WMemPy')
from wmem_process import WinProc

test = WinProc('dwm.exe')
test.print_process_detailed()
