FROM ghcr.io/astral-sh/uv:python3.13-alpine

RUN apk update

ADD . /app

WORKDIR /app

RUN uv sync --frozen

ENTRYPOINT [ "uv", "run", "file-sorter" ]
