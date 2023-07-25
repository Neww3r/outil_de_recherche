# commande à taper en ligne de commande après la sauvegarde de ce fichier:
# python setup.py build
from cx_Freeze import setup, Executable
  
executables = [
        Executable(script = "main.py",icon = "icon.ico", base = "Win32GUI" )
]
# ne pas mettre "base = ..." si le programme n'est pas en mode graphique, comme c'est le cas pour chiffrement.py.
  
buildOptions = dict( 
        includes = ["os","subprocess","tkinter","re"],
        include_files = ["icon.ico"]
)
  
setup(
    name = "Outil de recherche",
    version = "1.0",
    description = "Recherche de chaîne de caractères dans des fichiers de code",
    author = "Erwan LE GRAND",
    options = dict(build_exe = buildOptions),
    executables = executables
)