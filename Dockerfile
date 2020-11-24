FROM ubuntu:16.04

# Install requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libmysqlclient-dev \
    python \
    python-dev \
    python-virtualenv \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    libssl-dev \
    libxslt1-dev \
    libxml2-dev

# Setup application
COPY requirements.txt /var/app/
RUN virtualenv /var/django-venv && /var/django-venv/bin/pip install -r /var/app/requirements.txt
COPY . /var/app/
# COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY config/docker-entry.sh /docker-entry.sh
RUN mkdir -p /var/lib/celery && useradd app && chown app:app /var/lib/celery/ && chown -R app:app /var/app

ENV DATABASE_URL="sqlite:////var/app/db.sqlite3" \
    BROKER_URL="amqp://guest:guest@rabbitmq//" \
    ADMIN_EMAIL="" \
    SECRET_KEY="" \
    EMAIL_HOST="" \
    EMAIL_HOST_USER="" \
    EMAIL_HOST_PASSWORD="" \
    DEFAULT_FROM_EMAIL="" \
    SERVER_EMAIL=""

EXPOSE 8000

VOLUME /var/static/
VOLUME /var/media/

ENTRYPOINT ["/docker-entry.sh"]

CMD ["/var/django-venv/bin/gunicorn", "operations.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=1", "--chdir", "/var/app/operations/"]
