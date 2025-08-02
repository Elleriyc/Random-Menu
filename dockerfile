FROM python:3.13-bullseye

# Upgrade system packages to fix vulnerabilities
RUN apt-get update

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Changer le répertoire de travail vers src
WORKDIR /app/src

# Utiliser uvicorn au lieu de fastapi run
CMD ["fastapi", "run", "routes.py", "--port", "80"]
