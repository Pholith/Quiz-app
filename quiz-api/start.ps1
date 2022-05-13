python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt 

# pip freeze --local > requirements.txt