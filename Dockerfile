FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser -D galette
USER galette

ENV PATH="/usr/local/bin:${PATH}"

COPY ./galette LICENSE /app/

COPY ./templates/ /templates/

COPY ./static/ /static/

VOLUME ["/pages", "/assets", "/templates", "/static"]

EXPOSE 5000

CMD [ "uvicorn", "galette.app:app", "--host", "0.0.0.0", "--port", "5000" ]