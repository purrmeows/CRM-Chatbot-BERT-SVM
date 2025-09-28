FROM python:3.11-slim

# 1. ติดตั้ง dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. คัดลอกไฟล์และติดตั้ง requirements
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 3. คัดลอกโค้ดและโมเดล
COPY . .

# 4. รัน Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]
