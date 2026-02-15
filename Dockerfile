FROM python:3.14-slim-trixie AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

# ---------

FROM python:3.14-slim-trixie

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y cron &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists

COPY --from=builder /app/.venv /opt/virtualenvs/poepalettedata
COPY poepalettedata poepalettedata
COPY contrib contrib

RUN crontab contrib/docker/poepalettedata-cron

# run cron in background and tail logs to container output
CMD ["sh", "-c", "cron && tail -f /var/log/poepalettedata/*.log"]
