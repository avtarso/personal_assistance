# personal.assistant.project

python3 -m venv paenv
source paenv/bin/activate.

pip install -r requirements.txt

pre-commit install
pre-commit autoupdate
pre-commit run --all-files
