import sys
sys.path.insert(1, 'WMemPy')
from wmem_process import WinProc


app_name = 'WMemPy_test_app.exe'
myapp = WinProc(app_name)

main_entry = [module for module in myapp.modules if module.get_name() == app_name][0]

data = myapp.scanner.ASCII_list(main_entry, False, 5)
memory = myapp.scanner.ASCII_list_arr(myapp.pages, True, 5)