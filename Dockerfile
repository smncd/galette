FROM python:3.13-alpine

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apk update \
    && apk upgrade --no-cache \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN adduser -D galette

RUN chown -R galette /app

USER galette

VOLUME [ "/pages", "/assets" ]

EXPOSE 5000

CMD [ "uvicorn", "galette:app", "--host", "0.0.0.0", "--port", "5000" ]