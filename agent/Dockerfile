# ── Smart Robot Monitor ── Dockerfile ──
# Multi-stage: build + runtime mínimo

FROM python:3.11-slim-bookworm AS builder

WORKDIR /app
COPY pyproject.toml .
COPY agent/ agent/
COPY robot/ robot/
COPY web/ web/

RUN pip install --no-cache-dir --user . && \
    find /root/.local -name "*.pyc" -delete

# ── Runtime ──
FROM python:3.11-slim-bookworm

RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
WORKDIR /app
COPY .env.example .

ENV PATH=/root/.local/bin:$PATH
ENV ROBOT_IP=192.168.4.1
ENV HOST=0.0.0.0
ENV PORT=8080

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/status')" || exit 1

CMD ["sh", "-c", "python -m web.main --host ${HOST} --port ${PORT}"]
