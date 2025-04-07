FROM python:3.13

WORKDIR /src
EXPOSE 8080

RUN apt-get update && apt-get install -y curl make && rm -rf /var/lib/apt/lists/*

RUN pip install uv==0.5.9

COPY uv.lock /src/
COPY pyproject.toml /src/

RUN uv sync

COPY . /src
RUN chmod +x /src/bin/run.sh

ENV PYTHONPATH="${PYTHONPATH}:/src/src"
ENV PATH="/src/.venv/bin:${PATH}"
CMD ["/src/bin/run.sh"]
