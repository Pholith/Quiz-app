# A faire pour lancer le projet (l'envionnement virtuel)
python -m venv venv

# A faire la première fois qu'on lance le script Activage
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# A faire pour installer tous les packets utilisés par le projet
pip install -r requirements.txt 

# A faire après avoir installé des nouveaux packets
pip freeze --local > requirements.txt

# Installation de vue dans le projet pour celui qui installe seulement
npm init vue@latest


cd quiz-ui
npm run dev