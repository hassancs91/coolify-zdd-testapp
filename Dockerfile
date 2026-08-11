# E3: HEALTHCHECK with start-period tuned to cover the app's real boot time.
# Paired with matching Coolify UI health check settings.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app.py .
ENV PYTHONUNBUFFERED=1
EXPOSE 3000
HEALTHCHECK --interval=2s --timeout=3s --retries=3 --start-period=20s \
  CMD curl -f http://127.0.0.1:3000/health || exit 1
CMD ["python", "app.py"]
