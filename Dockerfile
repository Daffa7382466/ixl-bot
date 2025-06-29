FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy # <-- UPDATE VERSI

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
