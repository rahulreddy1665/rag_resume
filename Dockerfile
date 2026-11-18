FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

EXPOSE 7860
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT:-7860}