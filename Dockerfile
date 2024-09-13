FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

COPY --chown=user datalia/ $HOME/app/datalia/
COPY --chown=user dbt/ $HOME/app/dbt/
COPY --chown=user Makefile pyproject.toml uv.lock $HOME/app/

WORKDIR $HOME/app

RUN [ "uv", "sync" ]

CMD [ "uv", "run", "dagster", "dev", "-h", "0.0.0.0", "-p", "7860" ]
