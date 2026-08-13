# Build stage - clone and prepare dependencies
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Henrik-BL/hcnb-stock-data /opt/hcnb-stock-data

# Final stage - minimal production image
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /opt/hcnb-stock-data /opt/hcnb-stock-data
RUN if [ -f /opt/hcnb-stock-data/setup.py ] || [ -f /opt/hcnb-stock-data/pyproject.toml ]; then \
        pip install --no-cache-dir -e /opt/hcnb-stock-data; \
    fi

COPY app.py ./
COPY src/ ./src/
COPY portfolio_data/ ./portfolio_data/


ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app
ENV MONGODB_URI=mongodb://host.docker.internal:27017

EXPOSE 5010

CMD ["gunicorn", "--bind", "0.0.0.0:5010", "app:app", "--workers", "4", "--threads", "2"]
