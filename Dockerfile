FROM python:3.13

WORKDIR /app

COPY . .

RUN "./build.sh"

CMD ["celery", "-A", "backend", "worker", "--loglevel=info", "--pool=solo"]
