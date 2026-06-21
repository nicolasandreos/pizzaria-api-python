FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./scripts/entrypoint.sh

CMD ["./scripts/entrypoint.sh"]