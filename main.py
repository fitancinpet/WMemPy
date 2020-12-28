import sys
sys.path.insert(1, 'WMemPy')
from wmem_process import WinProc

csgo = WinProc('csgo.exe')
client = [module for module in csgo.modules if module.get_name() == 'client.dll']
print('result is:')
res = csgo.scanner.ASCII_list(client[0], False, 5)
print(res)
