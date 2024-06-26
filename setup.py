# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/icone.ico") ]
cx_Freeze.setup(
    name = "GTA",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["recursos"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
