# E1 baseline: NO health check. This is what most first deploys look like.
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
ENV PYTHONUNBUFFERED=1
EXPOSE 3000
CMD ["python", "app.py"]
