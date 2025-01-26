FROM python:3.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get upgrade -y

# setup py
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY poepalettedata /app/poepalettedata

# setup cron
RUN apt-get install -y cron && apt-get clean
COPY contrib /app/contrib
RUN crontab contrib/docker/poepalettedata-cron

# run cron in background and tail logs to container output
CMD ["sh", "-c", "cron && tail -f /var/log/poepalettedata/*.log"]
