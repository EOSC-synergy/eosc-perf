# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS backend

WORKDIR /app

ENV PATH="/home/sid/.local/bin:${PATH}"
ENV FLASK_APP="autoapp.py"

COPY eosc_perf eosc_perf
COPY autoapp.py ./
COPY setup.cfg ./
COPY requirements requirements

RUN pip install --no-cache -r requirements/prod.txt

# ================================= PRODUCTION =================================
FROM backend AS production

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

ENV FLASK_ENV="production"
EXPOSE 5000
ENTRYPOINT ["supervisord"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]

# ================================= DEVELOPMENT ================================
FROM backend AS development

RUN pip install --no-cache -r requirements/dev.txt
ENV FLASK_ENV="development"

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]

# ================================= TESTING ====================================
FROM backend AS testing

RUN pip install --no-cache -r requirements/dev.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY tests tests

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

ENV FLASK_ENV="testing"
ENTRYPOINT ["pytest"]
