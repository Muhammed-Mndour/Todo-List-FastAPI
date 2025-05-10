FROM python:3.13-slim AS builder

WORKDIR /src

RUN apt-get update  \
    && apt-get install -y curl make default-libmysqlclient-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv==0.6.14

COPY uv.lock /src/
COPY pyproject.toml /src/

RUN uv sync

FROM python:3.13-slim AS runtime
WORKDIR /src
EXPOSE 8080

RUN apt-get update  \
    && apt-get install -y curl make default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv==0.6.14

COPY --from=builder /src/.venv /src/.venv

COPY . /src
RUN chmod +x /src/bin/run.sh

ENV PYTHONPATH="${PYTHONPATH}:/src/src"
ENV PATH="/src/.venv/bin:${PATH}"
CMD ["/src/bin/run.sh"]
