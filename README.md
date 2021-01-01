WMemPy - WinApi Memory Application
==================================
WMempy allows users to quickly manipulate with memory of other processes using WinApi. The application provides CLI as well as Python modules to work with most processes.

Features
--------
List processes and get process handle
Retrieve modules and memory pages (called Scannables)
Read and analyze Scannables
Run AOB and ASCII scans on Scannables
List ASCII strings of Scannables
Read and Write Process Memory (both Scannables and Process is supported)
View memory blocks in CLI

Examples
--------
### bad_code_detection
Shows how to look for good/bad code in running processes

### config_dump
Example configuration file for CSGO offset dump (using the CLI wmempy --dump)

### cpp_apps
Very simple applications written in C++ to experiment on with the app. Source code included where possible.

### csgo_primitive_wallhack
Shows how to use the tool to read and alter memory of other processes to gain an advantage

### password_grabber
Shows how to use the tool to look for strings that are hardcoded into the app as well as live memory strings

Install
-------
To install the project, download the package:

<pre>
python -m pip install wmempy
</pre>

Documentation
-------------

To check out the sources and documentation, download the source from:

<pre>
https://github.com/fitancinpet/WMemPy
https://pypi.org/project/wmempy/#files
</pre>

Extract the sources if needed and go into the WMemPy folder (main project folder). From there, to build documentations, just do:

cd docs
make html

The HTML pages are in _build/html.

CLI Usage
---------
<pre>
wmempy --help
</pre>