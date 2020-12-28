import sys
sys.path.insert(1, 'WMemPy')
from wmem_process import WinProc

csgo = WinProc('csgo.exe')
client = [module for module in csgo.modules if module.get_name() == 'client.dll']
print('result is:')
print(csgo.scanner.AOB_scan(client[0], 'A1 ? ? ? ? A8 01 75 4B', 16, ' '))
