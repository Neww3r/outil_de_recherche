@echo "Création de l'éxécutable"
python "%~dp0\setup.py" build

@echo "Création de l'installeur"
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "%~dp0\setup_script.iss"

@echo "L'installeur a bien été généré"
pause