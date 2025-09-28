# ใช้ Python slim image
FROM python:3.11-slim

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ requirements.txt
COPY requirements.txt .

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# ตั้งค่า port สำหรับ Cloud Run
ENV PORT 8080

# รัน Flask app ด้วย gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
