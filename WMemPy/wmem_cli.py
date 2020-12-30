import sys
import click
import numpy as np
from wmem_process import WinProc
from wmem_system import WinSys


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

def readable(line):
    condition = (line <= 32) | (line >= 127)
    line = np.where(condition, 46, line)
    return line.tobytes().decode('ASCII')

def memory_view_print(memory, address):
    reshaped = np.reshape(memory,(-1,16))
    np.set_printoptions(formatter={'int':lambda x:'{:02x}'.format(x)}, threshold=sys.maxsize)
    for line in reshaped:
        print(hex(address), line, readable(line))
        address += 16

def memory_view(process, view):
    base = 16 if view[1] and view[1][:2] else 10
    try:        
        hint = int(view[1], base)
    except Exception:
        hint = 0
    scannable_array = array_from_where(process, view[0])
    for scannable in scannable_array:
        hint_relative = hint
        if hint >= scannable.size and hint >= scannable.base_address:
            hint_relative -= scannable.base_address
        hint_relative = (hint_relative // 16) * 16
        memory = scannable.read_from(hint_relative)
        if (not memory is None) and len(memory) > 1:
            memory_view_print(memory, scannable.base_address + hint_relative)
            print('vvvvvvvvvvvvvvvvvvv')


def text_list(process, list_text):
    params = list_text[0]
    hint = list_text[2]
    if len(params) == 0:
        symbols = True
        min_length = 5
    else:
        symbols = params[0] == 's'
        try:            
            min_length = int(params[1:])
        except Exception:
            min_length = 5
    scannable_array = array_from_where(process, list_text[1])
    try:
        result = process.scanner.ASCII_list_arr(scannable_array, symbols, min_length)
    except Exception:
        raise click.BadParameter('Invalid text list parameters.')
    print(f'Listing ASCII strings {"with" if symbols else "without"} symbols, minimum length is {min_length}, hint is {hint}:')
    print('-------------------')
    if not (hint is None):
        result = [word for word in result if hint in word]
    for word in result:
        print(word)
    print('-------------------')

def text_scan(process, text):
    scannable_array = array_from_where(process, text[1])
    try:
        result, scannable = process.scanner.ASCII_scan_arr(scannable_array, text[0])
    except Exception:
        raise click.BadParameter('Invalid ASCII scan parameters.')
    if result is None:
        print('Text does not exist.')
    else:
        print(f'Text found at: {hex(scannable.base_address)} + {hex(result)} = {hex(scannable.base_address + result)}')

def aob_scan(process, aob):
    scannable_array = array_from_where(process, aob[1])
    try:
        result, scannable = process.scanner.AOB_scan_arr(scannable_array, aob[0], aob[2], aob[3])
    except Exception:
        raise click.BadParameter('Invalid AOB scan parameters.')
    if result is None:
        print('Pattern does not exist.')
    else:
        print(f'Pattern found at: {hex(scannable.base_address)} + {hex(result)} = {hex(scannable.base_address + result)}')

def process_app(process, modules, pages, aob, text, list_text, view):
    if modules:
        process.print_modules()
    if pages:
        process.print_pages()
    if not (aob[0] is None):
        return aob_scan(process, aob)
    if not (text[0] is None):
        return text_scan(process, text)
    if not (list_text[0] is None):
        return text_list(process, list_text)
    if not (view[0] is None):
        return memory_view(process, view)

def get_proc(identifier):
    try:
        pid = int(identifier)
    except Exception:
        pid = -1
    return WinProc(identifier, pid)

def compare_procs(first, second):
    try:
        first_proc = get_proc(first)
        second_proc = get_proc(second)
    except Exception as e:
        raise click.BadParameter(e)
    first_proc.compare(second_proc)
    

def run_app(name, id, list, modules, pages, aob, text, list_text, view, compare):
    if list:
        return WinSys.process_list_print()
    if compare:
        return compare_procs(compare[0], compare[1])
    if (name is None) and id == -1:
        raise click.BadParameter('Please specify process to work with.')
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