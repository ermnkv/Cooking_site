FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup -g 1001 -S flaskgroup && \
    adduser -u 1001 -S -G flaskgroup flaskuser

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
