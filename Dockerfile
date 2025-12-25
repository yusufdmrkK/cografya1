FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Dosyaları tek tek değil, her şeyi kopyaladığından emin olalım
COPY . .
EXPOSE 5000
# Flask'ın Docker içinde dışarıya sinyal vermesi için host ayarı şart
CMD ["python", "app.py"]
