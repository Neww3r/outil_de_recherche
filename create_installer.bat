echo Création de l'éxécutable
python "%~dp0\setup.py" build

echo Création de l'installeur
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "%~dp0\setup_script.iss"

echo L'installeur a bien été généré

if exist \\dsa3\Partage\Services_Techniques\Informatique\Projets_Info\Outil_de_recherche\ (
	xcopy /y "%~dp0\setup_outil_de_recherche.exe" "\\dsa3\Partage\Services_Techniques\Informatique\Projets_Info\Outil_de_recherche\"
	echo L'installeur a été copié dans Projets_Info
)

pause