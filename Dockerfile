# E2: HEALTHCHECK added with naive defaults (no start-period tuning).
# curl must be installed - python:slim ships without it, and a HEALTHCHECK that
# calls a missing curl marks the container unhealthy forever (docs list this as
# the most common cause of "no available server").
FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app.py .
ENV PYTHONUNBUFFERED=1
EXPOSE 3000
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD curl -f http://127.0.0.1:3000/health || exit 1
CMD ["python", "app.py"]
