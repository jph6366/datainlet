FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY datalia/ /app/datalia/
COPY dbt/ /app/dbt/
COPY Makefile pyproject.toml uv.lock /app/

WORKDIR /app

RUN [ "uv", "sync" ]

CMD [ "uv", "run", "dagster", "dev", "-h", "0.0.0.0", "-p", "3000" ]
# CMD [ "bash" ]
