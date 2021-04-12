# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS backend

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid

ENV PATH="/home/sid/.local/bin:${PATH}"
ENV FLASK_APP="autoapp.py"

COPY eosc_perf eosc_perf
COPY autoapp.py ./
COPY setup.cfg ./

# ================================= PRODUCTION =================================
FROM backend as production

COPY requirements requirements
RUN pip install --no-cache --user -r requirements/prod.txt

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

EXPOSE 5000
ENTRYPOINT ["/bin/bash", "shell_scripts/supervisord_entrypoint.sh"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]

# ================================= DEVELOPMENT ================================
FROM backend AS development

COPY requirements requirements
RUN pip install --no-cache -r requirements/dev.txt

EXPOSE 2992
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
