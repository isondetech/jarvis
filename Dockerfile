FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4" ]