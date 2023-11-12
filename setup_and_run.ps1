# 1. Check Python version and install if not 3.10
$pythonVersion = python --version
if ($null -eq $pythonVersion -or $pythonVersion -notlike 'Python 3.10*') {
    Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe' -OutFile 'python_installer.exe'
    Start-Process -Wait -FilePath '.\python_installer.exe' -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1'
    Remove-Item -Path 'python_installer.exe'
}

# 2. Check if pip is installed, if not install it
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    (Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -UseBasicParsing).Content | python -
}

#Setup Python venv(virtual environment)
python -m venv .\.venv

# 3. Activate Python venv
.\.venv\Scripts\Activate.ps1

# 4. Install app requirements
pip install -r .\requirements.txt

# 5. Run application
streamlit run .\main.py
