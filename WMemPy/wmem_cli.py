import click
from wmem_process import WinProc
from wmem_system import WinSys


def process_app(process, modules):
    if modules:
        process.print_modules()

def run_app(name, id, list, modules):
    if list:
        return WinSys.process_list_print()
    if name is None and id == -1:
        raise click.BadParameter('Please specify process to work with.')
    try:
        process = WinProc(name, id)
    except Exception as e:
        raise click.BadParameter(e)
    process_app(process, modules)

@click.command()
@click.version_option(version='1.0')
@click.option('-n', '--name', help='Name of the process to work with.')
@click.option('-i', '--id', default=-1, help='PID of the process to work with.')
@click.option('-l', '--list', is_flag=True, help='List all processes running.')
@click.option('-m', '--modules', is_flag=True, default=False, help='List all modules of given process.')
def main_app(name, id, list, modules):
    """
    CLI click wrapper for the application.
    Everything is forwarded into the main entry point.
    """
    run_app(name, id, list, modules)

def main():
    """
    Helper for WMemPy.
    """
    main_app(prog_name='wmempy')

if __name__ == '__main__':
    main_app(prog_name='wmempy')