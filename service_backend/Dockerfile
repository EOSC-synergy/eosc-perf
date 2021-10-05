# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS backend

WORKDIR /app

ENV PATH="/home/sid/.local/bin:${PATH}"
ENV FLASK_APP="autoapp.py"

COPY backend backend
COPY autoapp.py ./
COPY requirements requirements

# ================================= PRODUCTION =================================
FROM backend AS production

RUN pip install --no-cache -r requirements/prod.txt
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

ENV FLASK_ENV="production"
EXPOSE 5000
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# ================================= DEVELOPMENT ================================
FROM backend AS development

COPY factories factories
RUN pip install --no-cache -r requirements/prod.txt
RUN pip install --no-cache -r requirements/dev.txt

ENV FLASK_ENV="development"
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

# ================================= TESTING ====================================
FROM backend AS testing

COPY factories factories
COPY tests tests
COPY tox.ini tox.ini
RUN pip install --no-cache tox
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

ENV FLASK_ENV="production"
CMD ["tox"]
