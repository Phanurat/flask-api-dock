# ใช้ Python เป็น Base Image
FROM python:3.9

# กำหนด working directory
WORKDIR /app

# คัดลอก requirements.txt และติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ด Flask app
COPY . .

# กำหนดคำสั่งรัน
CMD ["python", "app.py"]
