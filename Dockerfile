FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SANDBOX_FACTORY=local_sandbox:create_sandbox

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        dnsutils \
        git \
        iproute2 \
        netcat-openbsd \
        wget \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir openai httpx aiohttp

WORKDIR /opt/mapta
COPY . /opt/mapta

RUN mkdir -p /home/user

ENTRYPOINT ["python", "/opt/mapta/run_single.py"]
