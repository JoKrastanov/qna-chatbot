# 1. Run Activate.ps1 script
.\.venv\Scripts\Activate.ps1

# 2. Run pip install -r ./SupportAI/requirements.txt
pip install -r .\SupportAI\requirements.txt

# 3. Run streamlit run ./SupportAI/main.py
streamlit run .\SupportAI\main.py