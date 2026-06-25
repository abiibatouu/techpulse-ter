# Image de l'application TechPulse.
# Sert a la fois au dashboard Streamlit (service par defaut) et a
# l'execution du pipeline (ingestion / LLM / taxonomie) via `docker compose run`.

FROM python:3.11-slim

WORKDIR /app

# Installer les dependances d'abord (cache Docker : ne reinstalle que si
# requirements.txt change).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code (data/, .git, .env sont exclus via .dockerignore).
COPY . .

# Port du dashboard Streamlit.
EXPOSE 8501

# Lancement par defaut : le dashboard.
# server.address=0.0.0.0 est indispensable pour que le port soit joignable
# depuis l'hote ; headless=true evite l'invite interactive au demarrage.
CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
