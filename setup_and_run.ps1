# 1. Check Python version and install if not 3.10
$pythonVersion = (python --version 2>&1) -match '(\d+\.\d+)' | Out-Null; $matches[1]
if ($null -eq $pythonVersion -or $matches[1] -ne '3.10') {
    # Download and install Python 3.10
    Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe' -OutFile 'python_installer.exe'
    Start-Process -Wait -FilePath '.\python_installer.exe' -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1'
    Remove-Item -Path 'python_installer.exe'
}

# 2. Check if pip is installed, if not install it
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    # Install pip
    (Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -UseBasicParsing).Content | python -
}

# 3. Run Activate.ps1 script
.\.venv\Scripts\Activate.ps1

# 4. Run pip install -r ./SupportAI/requirements.txt
pip install -r .\SupportAI\requirements.txt

# 5. Run streamlit run ./SupportAI/main.py
streamlit run .\SupportAI\main.py
