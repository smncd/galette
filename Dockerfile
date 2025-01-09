FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000" ]