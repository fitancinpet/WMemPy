import sys
import click
import numpy as np
from wmem_process import WinProc
from wmem_system import WinSys


# Get array of scannables from provided parameter
def array_from_where(process, where):
    if where == 'all':
        return process.pages
    elif where == 'pages':
        return process.pages
    elif where == 'modules':
        return process.modules
    elif not (where is None):
        return [module for module in process.modules if module.get_name().lower() == where.lower()]
    else:
        return process.pages

# Convert byte array to readable string representation, that
# means filter out unreadable symbols and replace others with dot
def readable(line):
    condition = (line <= 32) | (line >= 127)
    line = np.where(condition, 46, line)
    return line.tobytes().decode('ASCII')

# Print raw memory to console in a nice and readable format
# 16 bytes per line like any other memory viewer
def memory_view_print(memory, address):
    # Reshape memory to 16 bytes long arrays
    reshaped = np.reshape(memory,(-1,16))
    # Make sure numpy prints the entire array and doesn't short it
    # Also convert the hex to nice format (remove 0x in front)
    np.set_printoptions(formatter={'int':lambda x:'{:02x}'.format(x)}, threshold=sys.maxsize)
    # Print and also keep up with the address
    for line in reshaped:
        print(hex(address), line, readable(line))
        address += 16

# Allows to print out memory of process based on parameters
def memory_view(process, view):
    # Convert hint (supports both hex and decimals) if it exists
    base = 16 if view[1] and view[1][:2] else 10
    try:        
        hint = int(view[1], base)
    except Exception:
        hint = 0
    # Get scannables that will be printed
    scannable_array = array_from_where(process, view[0])
    # Each scannable gets printed and is separated by line of Vs
    # to mimic the empty address space in between
    for scannable in scannable_array:
        hint_relative = hint
        # Hint can be either relative to the memory page or absolute
        # Here is decided what the user meant
        if hint >= scannable.size and hint >= scannable.base_address:
            hint_relative -= scannable.base_address
        # Always round down to 16 bytes so the memory is alligned properly
        hint_relative = (hint_relative // 16) * 16
        # Read the memory starting from the hint or 0
        memory = scannable.read_from(hint_relative)
        # If we were able to read some memory, print it
        # We don't get memory if the range was wrong or the page is protected
        if (not memory is None) and len(memory) > 1:
            memory_view_print(memory, scannable.base_address + hint_relative)
            print('vvvvvvvvvvvvvvvvvvv')

# List all strings of given process based on parameters
def text_list(process, list_text):
    params = list_text[0]
    # Hint here is used to only show words that contain it
    hint = list_text[2]
    # Params are in format 'x<number>' where x specifies if symbols should be used
    # (s = use, anything else means don't use them), number sets the minimum length
    # of the string
    if len(params) == 0:
        symbols = True
        min_length = 5
    else:
        symbols = params[0] == 's'
        try:            
            min_length = int(params[1:])
        except Exception:
            min_length = 5
    # Get scannables that will be checked for strings
    scannable_array = array_from_where(process, list_text[1])
    try:
        result = process.scanner.ASCII_list_arr(scannable_array, symbols, min_length)
    except Exception:
        raise click.BadParameter('Invalid text list parameters.')
    # Print all strings
    print(f'Listing ASCII strings {"with" if symbols else "without"} symbols, minimum length is {min_length}, hint is {hint}:')
    print('-------------------')
    if not (hint is None):
        result = [word for word in result if hint in word]
    for word in result:
        print(word)
    print('-------------------')

# Scan process for given text
def text_scan(process, text):
    # Get scannables that will be checked for the text
    scannable_array = array_from_where(process, text[1])
    try:
        result, scannable = process.scanner.ASCII_scan_arr(scannable_array, text[0])
    except Exception:
        raise click.BadParameter('Invalid ASCII scan parameters.')
    # If the text exists in the process, show it along with address for further inspection
    if result is None:
        print('Text does not exist.')
    else:
        print(f'Text found at: {hex(scannable.base_address)} + {hex(result)} = {hex(scannable.base_address + result)}')

# Same as text scan except with bytes
def aob_scan(process, aob):
    scannable_array = array_from_where(process, aob[1])
    # Parameters can specify pattern and it's separator and base
    try:
        result, scannable = process.scanner.AOB_scan_arr(scannable_array, aob[0], aob[2], aob[3])
    except Exception:
        raise click.BadParameter('Invalid AOB scan parameters.')
    if result is None:
        print('Pattern does not exist.')
    else:
        print(f'Pattern found at: {hex(scannable.base_address)} + {hex(result)} = {hex(scannable.base_address + result)}')

# Processes all the parameters given, also makes sure to only do one task
# if multiple parameters are provided, also sets the order of actions
def process_app(process, modules, pages, aob, text, list_text, view):
    # Modules can be listed on top of other commands
    if modules:
        process.print_modules()
    # Pages can be listed on top of other commands
    if pages:
        process.print_pages()
    # Other commands cannot be processed if previous one was already done
    if not (aob[0] is None):
        return aob_scan(process, aob)
    if not (text[0] is None):
        return text_scan(process, text)
    if not (list_text[0] is None):
        return text_list(process, list_text)
    if not (view[0] is None):
        return memory_view(process, view)

# Retrieves process from identifier (whether it is name or PID)
def get_proc(identifier):
    try:
        pid = int(identifier)
    except Exception:
        pid = -1
    return WinProc(identifier, pid)

# Compares two processes given as string of pid or name
def compare_procs(first, second):
    try:
        first_proc = get_proc(first)
        second_proc = get_proc(second)
    except Exception as e:
        raise click.BadParameter(e)
    first_proc.compare(second_proc)
    
# Helper to run the app from parameters
def run_app(name, id, list, modules, pages, aob, text, list_text, view, compare):
    # If we want to list processes, do it and stop
    if list:
        return WinSys.process_list_print()
    # If we want to compare processes, do it and stop
    if compare:
        return compare_procs(compare[0], compare[1])
    # Otherwise, name or pid of process has to be provided for the other commands to work
    if (name is None) and id == -1:
        raise click.BadParameter('Please specify process to work with.')
    # Try creating the process
    try:
        process = WinProc(name, id)
    except Exception as e:
        raise click.BadParameter(e)
    process_app(process, modules, pages, aob, text, list_text, view)

@click.command()
@click.version_option(version='1.0')
@click.option('-n', '--name', help='Name of the process to work with.')
@click.option('-i', '--id', default=-1, help='PID of the process to work with.')
@click.option('-l', '--list', is_flag=True, default=False, help='List all processes running.')
@click.option('-m', '--modules', is_flag=True, default=False, help='List all modules of given process.')
@click.option('-p', '--pages', is_flag=True, default=False, help='List all valid pages of given process.')
@click.option('-a', '--aob', help='List all valid pages of given process.')
@click.option('-w', '--where', help='List all valid pages of given process.')
@click.option('-b', '--base', default=16, show_default=True, help='List all valid pages of given process.')
@click.option('-s', '--separator', default=',', show_default=True, help='List all valid pages of given process.')
@click.option('-t', '--text', help='List all valid pages of given process.')
@click.option('-lt', '--list-text', help='List all valid pages of given process.')
@click.option('-h', '--hint', help='List all valid pages of given process.')
@click.option('-v', '--view', help='List all valid pages of given process.')
@click.option('-c', '--compare', nargs=2, help='List all valid pages of given process.')
def main_app(name, id, list, modules, pages, aob, where, base, separator, text, list_text, hint, view, compare):
    """
    CLI click wrapper for the application.
    Everything is forwarded into the main entry point.
    """
    run_app(name, id, list, modules, pages, [aob, where, base, separator], [text, where], [list_text, where, hint], [view, hint], compare)

def main():
    """
    Helper for WMemPy.
    """
    main_app(prog_name='wmempy')

if __name__ == '__main__':
    main_app(prog_name='wmempy')