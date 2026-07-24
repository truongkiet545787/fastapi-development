FROM python:3.12-slim

# Cài đặt các gói hệ thống cần thiết để biên dịch thư viện psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc bên trong container
WORKDIR /code

# Copy file requirements.txt vào trước để tận dụng cache của Docker
COPY ./requirements.txt /code/requirements.txt

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy toàn bộ mã nguồn của dự án vào container
COPY . /code

# Lệnh khởi chạy ứng dụng FastAPI bằng Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
