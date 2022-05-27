import py_compile, time, os

files_to_be_compiled = [
    "PM.py",
    "PMinstaller.py",
    "PMuninstaller.py"
]

for file in files_to_be_compiled:
    py_compile.compile(os.path.join(os.getcwd(), file))

time.sleep(2)

for file in os.listdir( os.path.join(os.getcwd(), "__pycache__") ):
    current_file = os.path.join(os.getcwd(), "__pycache__", file)
    new_file_name = current_file.replace(".cpython-310", "")
    
    os.rename( current_file, new_file_name )

print(" COMPILED SUCCESSFULLY")
