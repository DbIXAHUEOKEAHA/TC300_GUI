import cx_Freeze, sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"
    
py_name = "Transfer_control.py"
   
exe_name = "Transfer"
    
executables = [cx_Freeze.Executable(py_name, base=base, targetName=exe_name, icon="logo.png")]

cx_Freeze.setup(
   name=exe_name,
   options={"build_exe": {"packages": ["tkinter", "os", "time", "pandas", "csv", "matplotlib", "matplotlib.animation", "threading", "datetime", "pyvisa"], "includes": ["TC300", "RotStage", "ZStage"], 
                          "include_files": ["TC300.py", "RotStage.py", "ZStage.py", "logo.png"]}},
   version="1.0",
   description="GUI to control IFIM Transfer station",
   executables=executables
)