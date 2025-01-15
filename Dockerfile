FROM python:3.13-alpine

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN addgroup -S -g 1001 galette \
    && adduser -S -u 1001 -G galette -h /dev/null -s /sbin/nologin galette \
    && apk update \
    && apk upgrade --no-cache \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/cache/apk/* \
    && chown -R galette:galette /app

EXPOSE 5000

USER galette

CMD [ "uvicorn", "galette:app", "--host", "0.0.0.0", "--port", "5000" ]