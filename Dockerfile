FROM python:3.10-slim

WORKDIR /app

# Copy requirements from root
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app folder into container
COPY app/ .

EXPOSE 5001

CMD ["python", "app.py"]
