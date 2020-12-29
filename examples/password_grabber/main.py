import sys
sys.path.insert(1, 'WMemPy')
from wmem_process import WinProc


def print_sensitive_region(arr, index):
    print('--------------')
    for i in range(index - 10, index + 10):
        print(arr[i])

# Password grabber - checks the strings around the word password, email, username
# Name of application to target
app_name = 'WMemPy_test_app.exe'
myapp = WinProc(app_name)
# Check what the app loads
myapp.print_modules()
# Get data
main_entry = [module for module in myapp.modules if module.get_name() == app_name][0]

# Check data for any hardcoded values
print(f'Checking stack of {main_entry.get_name()} for strings:')
data = myapp.scanner.ASCII_list(main_entry, False, 5)
print(data)
print('')
print(f'\'password\' in {main_entry.get_name()}? ', 'password' in data)
print(f'\'email\' in {main_entry.get_name()}? ', 'email' in data)
print(f'\'login\' in {main_entry.get_name()}? ', 'login' in data)
print('')

# Check full memory (including heap)
print('Checking memory for sensitive words:')
memory = myapp.scanner.ASCII_list_arr(myapp.pages, True, 5)
sensitive_index = 0
for word in memory:
    sensitive_index += 1
    # If sensitive word is found, print everything around it
    if ('password' in word) or ('email' in word) or ('login' in word):
        print_sensitive_region(memory, sensitive_index)
